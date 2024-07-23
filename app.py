import os
import sys
import streamlit as st
import importlib
from streamlit_extras.concurrency_limiter import concurrency_limiter


@concurrency_limiter(max_concurrency=1)
def generate_image(api_key, input_data):
    # Reset API key before reload civitai module
    os.environ['CIVITAI_API_TOKEN'] = api_key

    if 'civitai' in sys.modules:
        del sys.modules['civitai']
        civitai = importlib.import_module('civitai')
    else:
        import civitai

    # Send the request and wait for the response
    try:
        res = civitai.image.create(input_data, wait=True)
        return res
    except Exception as e:
        st.error(f'Failed to generate image: {str(e)}')
        return None


def show_input_data(placeholder, input_data):
    placeholder.empty()
    with placeholder:
        st.json(input_data)


# Initialization
st.set_page_config(page_title='Civitai Image Generator',
                   page_icon='🎨',
                   layout='wide')
st.title('🎨 :rainbow[Civitai Image Generator]')

model_list = {
    'Realistic-Mix': 'urn:air:sd1:checkpoint:civitai:4384@128713',
    'TMND-Mix': 'urn:air:sd1:checkpoint:civitai:27259@221220',
    'Other': ''
}

# Sidebar
with st.sidebar:
    # Parameters for generated model
    st.info(
        'Grab your API Key from your [Civitai account](https://civitai.com/user/account) and paste the token 👇'
    )
    api_key = st.text_input(':rainbow[**API Key**]')
    model = st.selectbox(':rainbow[**Model Selection**]',
                         model_list.keys(),
                         index=0)

    if model == 'Other':
        model_urn = st.text_input('Model (URN)')
        model_list['Other'] = model_urn

    scheduler = st.selectbox(':rainbow[**Scheduler**]',
                             ['EulerA', 'DPM2MKarras', 'DPMSDEKarras', 'Heun'],
                             index=0)
    prompt = st.text_area(':rainbow[**Prompt (Required)**]',
                          placeholder='A cat')
    negative_prompt = st.text_area(':rainbow[**Negative Prompt (Optional)**]',
                                   placeholder='A dog')
    steps = st.slider(':rainbow[**Steps**]',
                      min_value=1,
                      max_value=50,
                      value=20)
    cfg_scale = st.slider(':rainbow[**CFG Scale**]',
                          min_value=1,
                          max_value=15,
                          value=7)
    width = st.slider(':rainbow[**Width**]',
                      min_value=1,
                      max_value=1024,
                      value=512)
    height = st.slider(':rainbow[**Height**]',
                       min_value=1,
                       max_value=1024,
                       value=768)
    seed = st.number_input(':rainbow[**Seed (-1 for random seed)**]', value=-1)
    show = st.checkbox('Show Input Data')

# Main content
col1, col2 = st.columns(2, gap='large')

if show:
    if api_key != '' and model_list[model] != '' and prompt != '':
        if 'input_data' not in st.session_state:
            st.session_state['input_data'] = {}

        st.session_state['input_data'].update({
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
            }
        })

        with col1:
            # Show input data (json format)
            st.subheader(':rainbow[Input Data]')
            placeholder = st.empty()
            show_input_data(placeholder, st.session_state['input_data'])

            # Parameters for additional networks
            with st.expander(':rainbow[**Additional Networks**]',
                             expanded=False):
                additional_networks = st.text_input(
                    ':rainbow[**Model (URN)**]')
                strength = st.slider('Strength',
                                     min_value=0.0,
                                     max_value=1.0,
                                     value=0.6)

                # If user wants to add additional networks
                if st.button('Add'):
                    if additional_networks != '':
                        if 'additionalNetworks' not in st.session_state[
                                'input_data']:
                            st.session_state['input_data'][
                                'additionalNetworks'] = {}

                        st.session_state['input_data'][
                            'additionalNetworks'].update(
                                {additional_networks: {
                                    'Strength': strength
                                }})
                        show_input_data(placeholder,
                                        st.session_state['input_data'])
            if st.button('Generate'):
                with st.spinner('Generating...'):
                    # Call the Civitai API and wait for the result
                    res = generate_image(api_key,
                                         st.session_state['input_data'])

                    if res:
                        # Show generated image
                        with col2:
                            if 'jobs' in res and res['jobs'][0].get('result'):
                                st.subheader(':rainbow[Generated Image]')
                                st.image(res['jobs'][0]['result']['blobUrl'],
                                         caption='Generated Image')
                                st.toast('Task completed!', icon="✅")
                            else:
                                st.error(
                                    'Failed to retrieve the generated image.')
    else:
        st.warning(f'Required fields cannot be empty.')
else:
    st.session_state['input_data'] = {}
