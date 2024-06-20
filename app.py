import civitai
import streamlit as st
from streamlit_extras.concurrency_limiter import concurrency_limiter


@concurrency_limiter(max_concurrency=1)
def generate_image(input_data):
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
st.set_page_config(layout='wide')
st.title('Civitai Image Generator')

model_list = {
    'Realistic-Mix': 'urn:air:sd1:checkpoint:civitai:4384@128713',
    'TMND-Mix': 'urn:air:sd1:checkpoint:civitai:27259@221220',
    'Other': ''
}

# Sidebar
with st.sidebar:
    # Parameters for generated model
    model = st.selectbox('Model Selection', model_list.keys(), index=0)

    if model == 'Other':
        model_urn = st.text_input('Model (URN)')
        model_list['Other'] = model_urn

    scheduler = st.selectbox('Scheduler',
                             ['EulerA', 'DPM2MKarras', 'DPMSDEKarras', 'Heun'],
                             index=0)
    prompt = st.text_area('Prompt (Required)', placeholder='A cat')
    negative_prompt = st.text_area('Negative Prompt (Optional)',
                                   placeholder='A dog')
    steps = st.slider('Steps', min_value=1, max_value=50, value=20)
    cfg_scale = st.slider('CFG Scale', min_value=1, max_value=15, value=7)
    width = st.slider('Width', min_value=1, max_value=1024, value=512)
    height = st.slider('Height', min_value=1, max_value=1024, value=768)
    seed = st.number_input('Seed (-1 for random seed)', value=-1)
    show = st.checkbox('Show Input Data')

# Main content
col1, col2 = st.columns(2, gap='large')

with col1:
    st.header(':gray[Input Data:]')
with col2:
    st.header(':gray[Generated Image:]')

if show:
    if model != '' and prompt != '':
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
            placeholder = st.empty()
            show_input_data(placeholder, st.session_state['input_data'])

            # Parameters for additional networks
            additional_networks = st.text_input('Additional Networks (URN)')
            strength = st.slider('Strength',
                                 min_value=0.0,
                                 max_value=1.0,
                                 value=0.6)

            # If user wants to add additional networks
            if st.button('Add Additional Networks'):
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

        with col2:
            if st.button('Generate'):
                with st.spinner('Generating...'):
                    # Call the Civitai API and wait for the result
                    res = generate_image(st.session_state['input_data'])

                # Show generated image
                if res:
                    if 'jobs' in res and res['jobs'][0].get('result'):
                        # st.write(str(res))
                        st.image(res['jobs'][0]['result']['blobUrl'],
                                 caption='Generated Image')
                        st.toast('Task completed!', icon="✅")
                    else:
                        st.error('Failed to retrieve the generated image.')
    else:
        st.warning(f'Required fields cannot be empty.')
else:
    st.session_state['input_data'] = {}
