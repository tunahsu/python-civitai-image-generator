# Streamlit Image Generation App

This project is an image generation application built using Streamlit and the Civitai Python SDK.

[View Online Demo](https://pickup100-python-civitai-image-generator.streamlit.app)

## Overview

<img src="https://i.imgur.com/RSuGWaN.png" width="70%" />

This application leverages the power of Streamlit for the web interface and the Civitai Python SDK for image generation. Users can generate images based on specific models, schedulers, prompts, and other parameters. 

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
  ```bash
  git clone https://github.com/tunahsu/python-civitai-image-generator.git
  cd python-civitai-image-generator/
  ```

2. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Run the Streamlit application:
  ```bash
  streamlit run app.py
  ```

## Usage

1. Grab your token from your [Civitai account](https://civitai.com/user/account)
2. Select a model and scheduler.
3. Enter your prompt/negative prompt and configure other settings.
4. Click the "Show Input Data" button to create and show your input data.
5. Check the input data, then click the "Generate" button to generate image. Or you can add additional networks first.
6. View and download the generated image.

## Example

Below is an example configuration for generating an image:

- **Model:** TMND-Mix
- **Scheduler:** EulerA
- **Prompt:** ```masterpiece, best quality, looking at viewer,
1girl, solo, (petite:1.2), 150cm, smile, sitting, shoulder cutout, braid, dress, cat ears, blonde hair, twin braids, blush, long hair, bench, grin, grass, white dress, jewelry, clothing cutout, bangs, necklace, floral print, blurry, hand between legs, blurry background, between legs, bow, facing viewer, bare shoulders, day, collarbone, hair bow, short sleeves, feet out of frame, ribbon, red headwear, on bench, depth of field, park bench, hair over shoulder, day, sky, flower field, petals```
- **Negative Prompt:** ```badhandv4, EasyNegative, verybadimagenegative_v1.3, (worst quality:2), (low quality:2), (normal quality:2)```
- **Steps:** 30
- **CFG Scale:** 7

- **Width:** 512
- **Height:** 512
- **Seed:** 3444137032

