import os
import threading
import streamlit as st
from streamlit_extras.concurrency_limiter import concurrency_limiter


@concurrency_limiter(max_concurrency=1)
def generate_image(api_token, input_data):
    """
    Generate an image using the Civitai SDK.

    :param input_data: The input parameters for the image generation.
    :return: The job result
    """
    os.environ['CIVITAI_API_TOKEN'] = api_token
    import civitai
    
    try:
        res = civitai.image.create(input_data, wait=True)
        return res
    except Exception as e:
        st.error(f'Failed to generate image: {str(e)}')
        return None


# Initialization
st.title('Civitai Image Generator')
model_list = {
    'Default': 'urn:air:sd1:checkpoint:civitai:4384@128713',
    'TMND-Mix': 'urn:air:sd1:checkpoint:civitai:27259@221220'
}

# Sidebar
with st.sidebar:
    with st.form('image_gen_form'):   
        st.write('Grab your token from [your Civitai account](https://civitai.com/user/account)')
        api_token = st.text_input('API Token (Required)', type='password')
        model = st.selectbox('Model Selection', model_list.keys(), index=0)
        scheduler = st.selectbox(
            'Scheduler', ['EulerA', 'DPM2MKarras', 'DPMSDEKarras', 'Heun'], index=0)
        prompt = st.text_area('Prompt (Required)', placeholder='A cat')
        negative_prompt = st.text_area('Negative Prompt (Optional)', placeholder='A dog')
        steps = st.slider('Steps', min_value=1, max_value=100, value=25)
        cfg_scale = st.slider('CFG Scale', min_value=1, max_value=15, value=7)
        width = st.number_input('Width', min_value=1,
                                max_value=1024, value=512)
        height = st.number_input(
            'Height', min_value=1, max_value=1024, value=512)
        seed = st.number_input('Seed (-1 for random)', value=-1)
        submit_button = st.form_submit_button('Generate')

# Main content
if submit_button:
    if api_token != '' and model != '' and prompt != '':
        input_data = {
            'model': model_list[model],
            'params': {
                'prompt': prompt,
                'negativePrompt': negative_prompt,
                'scheduler': scheduler,
                'steps': steps,
                'cfgScale': cfg_scale,
                'width': width,
                'height': height,
                'seed': seed,
                'clipSkip': 2,
            },
        }
        
        # Call the Civitai API and wait for the result
        with st.spinner('Generating...'):
            res = generate_image(api_token, input_data)

        # Show generated image
        if res:
            if 'jobs' in res and res['jobs'][0].get('result'):
                st.image(res['jobs'][0]['result']['blobUrl'],
                            caption='Generated Image')
                st.toast('Task completed!', icon = "✅")
            else:
                st.error('Failed to retrieve the generated image.')       
    else:
        st.warning(f'Required fields cannot be empty.')
        
