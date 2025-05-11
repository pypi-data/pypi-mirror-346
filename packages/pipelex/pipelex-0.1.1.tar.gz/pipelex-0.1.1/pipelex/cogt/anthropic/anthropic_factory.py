import asyncio
from typing import List, Optional, Union

from anthropic import AsyncAnthropic, AsyncAnthropicBedrock
from anthropic.types import Usage
from anthropic.types.image_block_param import ImageBlockParam
from anthropic.types.message_param import MessageParam
from anthropic.types.text_block_param import TextBlockParam
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
)

from pipelex.cogt.exceptions import CogtError
from pipelex.cogt.image.prompt_image_factory import PromptImageFactory
from pipelex.cogt.llm.llm_job import LLMJob
from pipelex.cogt.llm.llm_models.llm_platform import LLMPlatform
from pipelex.cogt.llm.llm_report import NbTokensByCategoryDict
from pipelex.cogt.llm.token_category import TokenCategory
from pipelex.config import get_config
from pipelex.hub import get_secrets_provider


class AnthropicFactoryError(CogtError):
    pass


class AnthropicFactory:
    @staticmethod
    def make_anthropic_client(
        llm_platform: LLMPlatform,
    ) -> Union[AsyncAnthropic, AsyncAnthropicBedrock]:
        # TODO: also support Anthropic with VertexAI
        match llm_platform:
            case LLMPlatform.ANTHROPIC:
                anthropic_config = get_config().cogt.llm_config.anthropic_config
                api_key = anthropic_config.get_api_key(secrets_provider=get_secrets_provider())
                return AsyncAnthropic(api_key=api_key)
            case LLMPlatform.BEDROCK_ANTHROPIC:
                aws_config = get_config().pipelex.aws_config
                aws_access_key_id, aws_secret_access_key, aws_region = aws_config.get_aws_access_keys()
                return AsyncAnthropicBedrock(
                    aws_secret_key=aws_secret_access_key,
                    aws_access_key=aws_access_key_id,
                    aws_region=aws_region,
                )
            case _:
                raise AnthropicFactoryError(f"Unsupported LLM platform for Anthropic sdk: '{llm_platform}'")

    @classmethod
    def user_message(
        cls,
        llm_job: LLMJob,
    ) -> MessageParam:
        message: MessageParam
        content: List[Union[TextBlockParam, ImageBlockParam]] = []

        if llm_job.llm_prompt.user_text:
            text_block_param: TextBlockParam = {
                "type": "text",
                "text": llm_job.llm_prompt.user_text,
            }
            content.append(text_block_param)
        if llm_job.llm_prompt.user_images:
            images_block_params: List[ImageBlockParam] = []
            for image in llm_job.llm_prompt.user_images:
                image_bytes = PromptImageFactory.promptimage_to_b64(image)
                # TODO: use a real image format passed in from the prompt image. Currently it seems more tolerant
                # when receiving png when expecting jpeg than the contrary, go figure...
                image_block_param_in_loop: ImageBlockParam = {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_bytes.decode("utf-8"),
                    },
                }
                images_block_params.append(image_block_param_in_loop)
            content += images_block_params

        message = {
            "role": "user",
            "content": content,
        }

        return message

    @classmethod
    async def user_message_async(
        cls,
        llm_job: LLMJob,
    ) -> MessageParam:
        message: MessageParam
        content: List[Union[TextBlockParam, ImageBlockParam]] = []

        if llm_job.llm_prompt.user_text:
            text_block_param: TextBlockParam = {
                "type": "text",
                "text": llm_job.llm_prompt.user_text,
            }
            content.append(text_block_param)
        if llm_job.llm_prompt.user_images:
            tasks_to_get_images = [PromptImageFactory.promptimage_to_b64_async(image) for image in llm_job.llm_prompt.user_images]
            image_bytes_list = await asyncio.gather(*tasks_to_get_images)
            images_block_params: List[ImageBlockParam] = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_bytes.decode("utf-8"),
                    },
                }
                for image_bytes in image_bytes_list
            ]
            content += images_block_params

        message = {
            "role": "user",
            "content": content,
        }

        return message

    # This creates a MessageParam disguised as a ChatCompletionMessageParam to please instructor type checking
    @staticmethod
    def openai_typed_user_message(
        user_content_txt: str,
        user_prompt_images_bytes: Optional[List[bytes]] = None,
    ) -> ChatCompletionMessageParam:
        text_block_param: TextBlockParam = {"type": "text", "text": user_content_txt}
        message: MessageParam
        if user_prompt_images_bytes is not None:
            images_block_params: List[ImageBlockParam] = []
            for image_bytes in user_prompt_images_bytes:
                image_block_param_in_loop: ImageBlockParam = {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_bytes.decode("utf-8"),
                    },
                }
                images_block_params.append(image_block_param_in_loop)

            content: List[Union[TextBlockParam, ImageBlockParam]] = images_block_params + [text_block_param]
            message = {
                "role": "user",
                "content": content,
            }

        else:
            message = {
                "role": "user",
                "content": [text_block_param],
            }

        return message  # type: ignore

    @classmethod
    def make_simple_messages(
        cls,
        llm_job: LLMJob,
    ) -> List[ChatCompletionMessageParam]:
        """
        Makes a list of messages with a system message (if provided) and followed by a user message.
        """
        llm_prompt = llm_job.llm_prompt
        messages: List[ChatCompletionMessageParam] = []
        #### System message ####
        if system_content := llm_prompt.system_text:
            messages.append(ChatCompletionSystemMessageParam(role="system", content=system_content))

        user_prompt_images_bytes: Optional[List[bytes]]
        if llm_prompt.user_images:
            user_prompt_images_bytes = [PromptImageFactory.promptimage_to_b64(image) for image in llm_prompt.user_images]
        else:
            user_prompt_images_bytes = None

        #### Concatenation ####
        messages.append(
            AnthropicFactory.openai_typed_user_message(
                user_content_txt=llm_prompt.user_text if llm_prompt.user_text else "",
                user_prompt_images_bytes=user_prompt_images_bytes,
            )
        )
        return messages

    @classmethod
    async def make_simple_messages_async(
        cls,
        llm_job: LLMJob,
    ) -> List[ChatCompletionMessageParam]:
        """
        Makes a list of messages with a system message (if provided) and followed by a user message.
        """
        llm_prompt = llm_job.llm_prompt
        messages: List[ChatCompletionMessageParam] = []
        #### System message ####
        if system_content := llm_prompt.system_text:
            messages.append(ChatCompletionSystemMessageParam(role="system", content=system_content))

        user_prompt_images_bytes: Optional[List[bytes]]
        if llm_prompt.user_images:
            tasks_to_get_images = [PromptImageFactory.promptimage_to_b64_async(image) for image in llm_prompt.user_images]
            user_prompt_images_bytes = await asyncio.gather(*tasks_to_get_images)
        else:
            user_prompt_images_bytes = None

        #### Concatenation ####
        messages.append(
            AnthropicFactory.openai_typed_user_message(
                user_content_txt=llm_prompt.user_text if llm_prompt.user_text else "",
                user_prompt_images_bytes=user_prompt_images_bytes,
            )
        )
        return messages

    @staticmethod
    def make_nb_tokens_by_category(usage: Usage) -> NbTokensByCategoryDict:
        nb_tokens_by_category: NbTokensByCategoryDict = {
            TokenCategory.INPUT: usage.input_tokens,
            TokenCategory.OUTPUT: usage.output_tokens,
        }
        return nb_tokens_by_category

    @staticmethod
    def make_nb_tokens_by_category_from_nb(nb_input: int, nb_output: int) -> NbTokensByCategoryDict:
        nb_tokens_by_category: NbTokensByCategoryDict = {
            TokenCategory.INPUT: nb_input,
            TokenCategory.OUTPUT: nb_output,
        }
        return nb_tokens_by_category
