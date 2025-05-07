# SPDX-License-Identifier: Apache-2.0
# Standard
from typing import Any, Dict, List
from typing import Optional
import json
import re

# Third Party
from datasets import Dataset
from jinja2 import Template
import openai

# Local
from .block import Block
from ..logger_config import setup_logger
from ..registry import BlockRegistry, PromptRegistry

logger = setup_logger(__name__)


def server_supports_batched(client, model_id: str) -> bool:
    supported = getattr(client, "server_supports_batched", None)
    if supported is not None:
        return supported
    try:
        # Make a test call to the server to determine whether it supports
        # multiple input prompts per request and also the n parameter
        response = client.completions.create(
            model=model_id, prompt=["test1", "test2"], max_tokens=1, n=3
        )
        # Number outputs should be 2 * 3 = 6
        supported = len(response.choices) == 6
    except openai.InternalServerError:
        supported = False
    client.server_supports_batched = supported
    logger.info(f"LLM server supports batched inputs: {client.server_supports_batched}")
    return supported


@BlockRegistry.register("LLMBlock")
# pylint: disable=dangerous-default-value
class LLMBlock(Block):
    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        block_name,
        config_path,
        client,
        output_cols,
        parser_kwargs={},
        model_prompt="{prompt}",
        model_id=None,
        **batch_kwargs,
    ) -> None:
        super().__init__(block_name)
        self.block_config = self._load_config(config_path)
        self.prompt_struct = (
            """{system}\n{introduction}\n{principles}\n{examples}\n{generation}"""
        )
        filtered_config = {
            k: (v if v is not None else "") for k, v in self.block_config.items()
        }
        self.prompt_template = Template(self.prompt_struct.format(**filtered_config))
        self.client = client
        if model_id:
            self.model = model_id
        else:
            # get the default model id from client
            self.model = self.client.models.list().data[0].id

        self.model_prompt = model_prompt
        self.output_cols = output_cols
        self.batch_params = batch_kwargs.get("batch_kwargs", {})
        self.parser_name = parser_kwargs.get("parser_name", None)
        self.parsing_pattern = parser_kwargs.get("parsing_pattern", None)
        self.parser_cleanup_tags = parser_kwargs.get("parser_cleanup_tags", None)
        self.defaults = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 4096,
        }

        # Whether the LLM server supports a list of input prompts
        # and supports the n parameter to generate n outputs per input
        self.server_supports_batched = server_supports_batched(client, self.model)


    def _extract_matches(
        self, text: str, start_tag: Optional[str], end_tag: Optional[str]
    ) -> List[str]:
        if not text:
            return []
        if not start_tag and not end_tag:
            return [text.strip()]

        pattern = ""
        if start_tag:
            pattern += re.escape(start_tag)
        pattern += r"(.*?)"
        if end_tag:
            pattern += re.escape(end_tag)
        elif start_tag:
            # Enforce matching till end of string when only start_tag is provided.
            pattern += "$"

        return [match.strip() for match in re.findall(pattern, text, re.DOTALL)]

    def _parse(self, generated_string) -> dict:
        matches = {}

        if self.parser_name is not None and self.parser_name == "custom":
            pattern = re.compile(self.parsing_pattern, re.DOTALL)
            all_matches = pattern.findall(generated_string)
            matches = {column_name: [] for column_name in self.output_cols}
            if all_matches and isinstance(all_matches[0], tuple):
                for match in all_matches:
                    for column_name, value in zip(self.output_cols, match):
                        value = value.strip()
                        for clean_tag in self.parser_cleanup_tags:
                            value = value.replace(clean_tag, "")
                        matches[column_name].append(value)
            else:
                matches[self.output_cols[0]] = (
                    [match.strip() for match in all_matches] if all_matches else []
                )
        else:
            for start_tag, end_tag, output_col in zip(
                self.block_config.get("start_tags", []),
                self.block_config.get("end_tags", []),
                self.output_cols,
            ):
                matches[output_col] = self._extract_matches(
                    generated_string, start_tag, end_tag
                )

        return matches

    def _format_prompt(self, sample: Dict) -> str:
        prompt_templated_str = self.prompt_template.render(sample).strip()
        return PromptRegistry.render_template(
            self.model_prompt, prompt_templated_str, add_generation_prompt=True
        ).strip()

    def _generate(self, samples, **gen_kwargs) -> list:
        prompts = [self._format_prompt(sample) for sample in samples]
        logger.debug("Prompt: %s", prompts[0])
        generate_args = {**self.defaults, **gen_kwargs}

        if self.server_supports_batched:
            response = self.client.completions.create(prompt=prompts, **generate_args)
            # if stop is provided, then we need to add the stop token to the generated text,
            # this is because the stop token is not included in the generated text - this is a limitation of the openai api
            # we need to add the stop token to the generated text to make it consistent for the parser
            if "stop" in generate_args:
                return [
                    choice.text.strip() + "".join(generate_args["stop"])
                    for choice in response.choices
                ]
            return [choice.text.strip() for choice in response.choices]

        n = gen_kwargs.get("n", 1)
        results = []
        for prompt in prompts:
            for _ in range(n):
                response = self.client.completions.create(
                    prompt=prompt, **generate_args
                )
                if "stop" in generate_args:
                    results.append(
                        response.choices[0].text.strip()
                        + "".join(generate_args["stop"])
                    )
                results.append(response.choices[0].text.strip())
        return results

    def generate(self, samples: Dataset, **gen_kwargs) -> Dataset:
        """
        Generate the output from the block. This method should first validate the input data,
        then generate the output, and finally parse the generated output before returning it.

        :return: The parsed output after generation.
        """
        num_samples = self.block_config.get("num_samples", None)
        logger.debug("Generating outputs for {} samples".format(len(samples)))

        if (num_samples is not None) and ("num_samples" not in samples.column_names):
            samples = samples.add_column("num_samples", [num_samples] * len(samples))

        # validate each sample
        # Log errors and remove invalid samples
        valid_samples = []

        for sample in samples:
            if self._validate(self.prompt_template, sample):
                valid_samples.append(sample)
            else:
                logger.warning(
                    f"Sample failed validation: {sample}"
                )  # Log details of the failed sample

        samples = valid_samples

        if len(samples) == 0:
            logger.warning(
                "No valid samples to generate outputs for, returning empty dataset"
            )
            return Dataset.from_list([])

        # generate the output

        outputs = self._generate(samples, **gen_kwargs)

        logger.debug("Generated outputs: %s", outputs)

        num_parallel_samples = gen_kwargs.get("n", 1)
        extended_samples = []

        # Duplicate each input sample n times, where n is the number
        # of output sequences generated per input, so that we can
        # pair up the inputs and outputs.
        for item in samples:
            extended_samples.extend([item] * num_parallel_samples)

        new_data = []
        for sample, output in zip(extended_samples, outputs):
            parsed_outputs = self._parse(output)
            max_length = max(len(value) for value in parsed_outputs.values())
            for values in zip(*(lst[:max_length] for lst in parsed_outputs.values())):
                new_data.append({**sample, **dict(zip(parsed_outputs.keys(), values))})

        return Dataset.from_list(new_data)


@BlockRegistry.register("ConditionalLLMBlock")
class ConditionalLLMBlock(LLMBlock):
    def __init__(
        self,
        block_name,
        config_paths,
        client,
        model_id,
        output_cols,
        selector_column_name,
        model_prompt="{prompt}",
        **batch_kwargs,
    ) -> None:
        super().__init__(
            block_name=block_name,
            config_path=list(config_paths.values())[0],
            client=client,
            model_id=model_id,
            output_cols=output_cols,
            model_prompt=model_prompt,
            **batch_kwargs,
        )
        self.selector_column_name = selector_column_name
        self.prompt_template = {}
        if "All" in config_paths:
            self.prompt_template = self.prompt_struct.format(**self.block_config)
        else:
            for config_key, config in config_paths.items():
                # Template(self.prompt_struct.format(**filtered_config))
                filtered_config = {
                    k: (v if v is not None else "")
                    for k, v in self.block_config.items()
                }
                self.prompt_template[config_key] = Template(
                    self.prompt_struct.format(**self._load_config(config))
                )

    def _format_prompt(self, sample: Dict) -> str:
        if isinstance(self.prompt_template, dict):
            return (
                self.prompt_template[sample[self.selector_column_name]]
                .render(**sample)
                .strip()
            )

        return self.prompt_template.render(**sample).strip()

    def _validate(self, prompt_template: str, input_dict: Dict[str, Any]) -> bool:
        if isinstance(prompt_template, dict):
            prompt_template = prompt_template[input_dict[self.selector_column_name]]
        return super()._validate(prompt_template, input_dict)


@BlockRegistry.register("LLMLogProbBlock")
class LLMLogProbBlock(LLMBlock):
    # init with init of the parent class
    def __init__(
        self,
        block_name,
        config_path,
        client,
        output_cols,
        parser_kwargs={},
        model_prompt="{prompt}",
        model_id=None,
        **batch_kwargs,
    ) -> None:
        super().__init__(
            block_name=block_name,
            config_path=config_path,
            client=client,
            output_cols=output_cols,
            parser_kwargs=parser_kwargs,
            model_prompt=model_prompt,
            model_id=model_id,
            **batch_kwargs,
        )

    def _generate_logprobs(self, samples, **gen_kwargs):
        prompts = [
            self.model_prompt.format(prompt=self._format_prompt(sample))
            for sample in samples
        ]
        generate_args = {**self.defaults, **gen_kwargs}

        # verify if logprobs is mentioned in the generate_args, if not add it and return top10 logprobs
        if "logprobs" not in generate_args:
            generate_args["logprobs"] = 10

        if self.server_supports_batched:
            response = self.client.completions.create(prompt=prompts, **generate_args)
            return [choice.logprobs.top_logprobs for choice in response.choices]

        n = gen_kwargs.get("n", 1)
        results = []
        for prompt in prompts:
            for _ in range(n):
                response = self.client.completions.create(
                    prompt=prompt, **generate_args
                )
                results.append(response.choices[0].logprobs.top_logprobs)
        return results

    def _parse(self, generations: List[List[Dict]]) -> List[List[str]]:
        # override the parse method to convert the generations to json string
        # convert the generations to json string to save as dataset
        # this is because the dataset can only store key value pairs which are consistent
        return [[json.dumps(item) for item in sublist] for sublist in generations]

    def generate(self, samples: Dataset, **gen_kwargs) -> Dataset:
        """
        Generate the output from the block. This method should first validate the input data,
        then generate the output, and finally parse the generated output before returning it.

        :return: The parsed output after generation.
        """
        num_samples = self.block_config.get("num_samples", None)
        logger.debug("Generating outputs for {} samples".format(len(samples)))

        if (num_samples is not None) and ("num_samples" not in samples.column_names):
            samples = samples.add_column("num_samples", [num_samples] * len(samples))

        # validate each sample
        # Log errors and remove invalid samples
        valid_samples = []

        for sample in samples:
            if self._validate(self.prompt_template, sample):
                valid_samples.append(sample)
            else:
                logger.warning(
                    f"Sample failed validation: {sample}"
                )  # Log details of the failed sample

        samples = valid_samples

        if len(samples) == 0:
            logger.warning(
                "No valid samples to generate outputs for, returning empty dataset"
            )
            return Dataset.from_list([])

        # generate the output

        outputs = self._generate_logprobs(samples, **gen_kwargs)
        logger.debug("Generated outputs: %s", outputs)

        output_dataset = Dataset.from_list(samples)
        output_dataset = output_dataset.add_column(
            self.output_cols[0],
            self._parse(outputs),  # pylint: disable=no-value-for-parameter
        )

        return output_dataset


@BlockRegistry.register("LLMMessagesBlock")
class LLMMessagesBlock(Block):
    def __init__(
        self,
        block_name,
        client,
        input_col,
        output_col,
        model_prompt=None,
        model_id=None,
        **batch_kwargs,
    ) -> None:
        self.block_name = block_name
        self.model_prompt = model_prompt
        self.batch_params = batch_kwargs.get("batch_kwargs", {})
        self.input_col = input_col
        self.output_col = output_col
        self.client = client

        if model_id:
            self.model = model_id
        else:
            self.model = self.client.models.list().data[0].id

        self.defaults = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 4096,
        }
        self.server_supports_batched = server_supports_batched(client, self.model)

    def _generate(self, samples, **gen_kwargs) -> list:
        generate_args = {**self.defaults, **gen_kwargs}

        if "n" in generate_args and generate_args.get("temperature", 0) <= 0:
            generate_args["temperature"] = 0.7
            logger.warning(
                "Temperature should be greater than 0 for n > 1, setting temperature to 0.7"
            )

        messages = samples[self.input_col]

        results = []
        n = gen_kwargs.get("n", 1)
        for message in messages:
            responses = self.client.chat.completions.create(
                messages=message, **generate_args
            )
            if n > 1:
                results.append([choice.message.content for choice in responses.choices])
            else:
                results.append(responses.choices[0].message.content)
        return results

    def generate(self, samples: Dataset, **gen_kwargs) -> Dataset:
        outputs = self._generate(samples, **gen_kwargs)
        samples = samples.add_column(self.output_col, outputs)
        return samples
