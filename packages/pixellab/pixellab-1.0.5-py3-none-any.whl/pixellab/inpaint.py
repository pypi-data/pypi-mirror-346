from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Literal, Union, Dict

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize
from .types import CameraView, Detail, Direction, Outline, Shading

if TYPE_CHECKING:
    from .client import PixelLabClient


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class InpaintResponse(BaseModel):
    image: Base64Image
    usage: Usage


def inpaint(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    inpainting_image: PIL.Image.Image,
    mask_image: PIL.Image.Image,
    negative_description: str = "",
    text_guidance_scale: float = 3.0,
    extra_guidance_scale: float = 3.0,
    outline: Optional[Outline] = None,
    shading: Optional[Shading] = None,
    detail: Optional[Detail] = None,
    view: Optional[CameraView] = None,
    direction: Optional[Direction] = None,
    isometric: bool = False,
    oblique_projection: bool = False,
    no_background: bool = False,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 300,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> InpaintResponse:
    """Generate an inpainted image.

    Args:
        client: The PixelLab client instance
        description: Text description of the image to generate
        image_size: Size of the generated image
        inpainting_image: Reference image which is inpainted
        mask_image: Inpainting mask (black and white image, white is where to inpaint)
        negative_description: Text description of what to avoid in the generated image
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        extra_guidance_scale: How closely to follow the style reference (0.0-20.0)
        outline: Outline style reference (weakly guiding)
        shading: Shading style reference (weakly guiding)
        detail: Detail style reference (weakly guiding)
        view: Camera view angle (weakly guiding)
        direction: Subject direction (weakly guiding)
        isometric: Generate in isometric view (weakly guiding)
        oblique_projection: Generate in oblique projection (beta)
        no_background: Generate with transparent background
        init_image: Initial image to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        color_image: Forced color palette
        seed: Seed for deterministic generation

    Returns:
        InpaintResponse containing the generated image

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    inpainting_image = Base64Image.from_pil_image(inpainting_image)
    mask_image = Base64Image.from_pil_image(mask_image)
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "description": description,
        "image_size": image_size,
        "negative_description": negative_description,
        "text_guidance_scale": text_guidance_scale,
        "extra_guidance_scale": extra_guidance_scale,
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "view": view,
        "direction": direction,
        "isometric": isometric,
        "oblique_projection": oblique_projection,
        "no_background": no_background,
        "init_image": init_image.model_dump() if init_image else None,
        "init_image_strength": init_image_strength,
        "inpainting_image": inpainting_image.model_dump(),
        "mask_image": mask_image.model_dump(),
        "color_image": color_image.model_dump() if color_image else None,
        "seed": seed,
    }
    try:
        response = requests.post(
            f"{client.base_url}/inpaint",
            headers=client.headers(),
            json=request_data,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        raise

    return InpaintResponse(**response.json())
