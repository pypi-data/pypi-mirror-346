import os
import io
from typing import Type, Dict, Any
from pydantic import BaseModel

from ..base_toolkit_model import BaseToolkitModel
from ..ai_config import Vision
from ..moderation import ModerationError


class VisionModel(BaseToolkitModel):
    model_name = "vision"

    def get_model_config(self) -> Vision:
        return self.ai_config.vision

    def _get_file_extension(self, in_memory_image_stream: io.BytesIO) -> str:
        # Get the file extension from the in-memory stream name
        if not hasattr(in_memory_image_stream, "name"):
            raise ValueError(
                "The in-memory image stream does not have a name attribute."
            )
        base_name = os.path.splitext(in_memory_image_stream.name)[-1]
        if not base_name:
            raise ValueError(
                "The in-memory image stream does not have a valid file extension."
            )
        return base_name.lower().lstrip(".")

    def _prepare_input(
        self,
        system_prompt: str,
        pydantic_model: Type[BaseModel],
        in_memory_image_stream: io.BytesIO,
    ) -> Dict[str, Any]:
        # Encode in base64:
        image_extension = self._get_file_extension(in_memory_image_stream)
        image_base64 = self.get_b64_from_bytes(in_memory_image_stream)
        return {
            "input_dict": {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{image_extension};base64,{image_base64}"
                },
            },
            "system_prompt": system_prompt,
            "pydantic_model": pydantic_model,
        }

    def run_impl(
        self,
        system_prompt: str,
        pydantic_model: Type[BaseModel],
        in_memory_image_stream: io.BytesIO,
    ) -> BaseModel:
        kwargs = self._prepare_input(
            system_prompt=system_prompt,
            pydantic_model=pydantic_model,
            in_memory_image_stream=in_memory_image_stream,
        )
        result = self._get_structured_output(**kwargs)
        # TODO: check moderation before running the model
        if self.moderation_needed and not self.moderate_text(result.model_dump_json()):
            raise ModerationError(
                f"Image description '{result}' was rejected by the moderation system"
            )
        return result

    async def arun_impl(
        self,
        system_prompt: str,
        pydantic_model: Type[BaseModel],
        in_memory_image_stream: io.BytesIO,
    ) -> BaseModel:
        kwargs = self._prepare_input(
            system_prompt=system_prompt,
            pydantic_model=pydantic_model,
            in_memory_image_stream=in_memory_image_stream,
        )
        result = await self._aget_structured_output(**kwargs)
        # TODO: check moderation before running the model
        if self.moderation_needed and not self.moderate_text(result.model_dump_json()):
            raise ModerationError(
                f"Image description '{result}' was rejected by the moderation system"
            )
        return result

    def get_price(
        self,
        image_pixels_count: int,
        *args,
        **kwargs,
    ) -> float:
        input_pixel_price = self.get_model().rate.input_pixel_price
        return image_pixels_count * input_pixel_price
