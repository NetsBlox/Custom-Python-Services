"""
This is a service providing access to Stable Diffusion in NetsBlox
"""
import netsblox as nb
from netsblox import types

import requests

sd_baseurl = 'http://127.0.0.1:7860/sdapi/v1/'


@nb.image_rpc('Generate an image with the given prompt')
@nb.argument('prompt', type=types.String, help='Text to use to generate image')
@nb.argument('negative_prompt', type=types.String, help='Text to describe things to avoid in generated image', optional=True)
def get_image(prompt, negative_prompt=""):
    payload = {
        "prompt": prompt,
        "negative_prompt": "poor quality" if len(negative_prompt) == 0 else negative_prompt,
        "steps": 20,
        "filter_nsfw": True
    }

    response = requests.post(url=sd_baseurl + 'txt2img', json=payload)
    response_json = response.json()

    return response_json['images'][0]


@nb.image_rpc('Generate an image with the given prompt and options')
@nb.argument('prompt', type=types.String, help='Text to use to generate image')
@nb.argument('negative_prompt', type=types.String, help='Text to describe things to avoid in generated image', optional=True)
@nb.argument('width', type=types.Number, help='Text to describe things to avoid in generated image', optional=True)
@nb.argument('height', type=types.Number, help='Text to describe things to avoid in generated image', optional=True)
def get_image_advanced(prompt, negative_prompt="", width=512, height=512):
    if width > 768 or width < 128:
        raise "Width must be betwen 128 and 768"

    if height > 768 or height < 128:
        raise "Height must be betwen 128 and 768"

    payload = {
        "prompt": prompt,
        "negative_prompt": "poor quality" if len(negative_prompt) == 0 else negative_prompt,
        "steps": 20,
        "filter_nsfw": True,
        "width": width,
        "height": height
    }

    response = requests.post(url=sd_baseurl + 'txt2img', json=payload)
    response_json = response.json()

    return response_json['images'][0]
