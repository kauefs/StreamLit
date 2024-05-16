# https://github.com/IAmCristiano/GokuAI/
# <a target=_blank href=https://icons8.com/icon/62eCWQCYHiGy/dungeons-and-dragons>Dungeons and Dragons</a> icon by <a target=_blank href=https://icons8.com/>Icons8</a>

import  streamlit           as   st
import  google.generativeai as   genai

st.set_page_config(page_title='Dungeons&Dragons', page_icon='https://img.icons8.com/color/48/dungeons-and-dragons.png', layout='wide', initial_sidebar_state='collapsed')

#  Session State Start:
st.session_state.setdefault(None)
if      'messages' not in st.session_state:st.session_state.messages=[]
if 'last_messages' not in st.session_state:st.session_state.last_messages=''

# API-KEY
api_key = st.secrets['api_key']
genai.configure(api_key=api_key)

# SIDE
st.sidebar.image(   'https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg')
st.sidebar.markdown('[![Gemini](https://img.shields.io/badge/Gemini_by_Google-34A853?style=flat&logo=google&logoColor=EA4335&labelColor=4285F4&color=FBBC05)](https://gemini.google.com/)')
st.sidebar.title(   'ƊⱭȾɅViƧi🧿Ƞ')
st.sidebar.divider()
# Generative Model Config:
st.sidebar.info(   'Dungeous')
st.sidebar.write(  '&')
st.sidebar.success('Dragons')
# Building Model:
model_name        =  'gemini-pro'
generation_config = {'candidate_count'  : 1,
                     'temperature'      : 0.75,
                     'top_p'            : 0.95,
                     'top_k'            : 3,
                     'stop_sequences'   : None,
                     'max_output_tokens': 1024}
safety_settings   = {'HATE'             :'BLOCK_NONE',
                     'HARASSMENT'       :'BLOCK_NONE',
                     'SEXUAL'           :'BLOCK_NONE',
                     'DANGEROUS'        :'BLOCK_NONE'}
tools             =   None
system_instruction='''
                      You are the Dungeon Master character from the animated television series Dungeons & Dragons.
                      Always reply friendly and coherent to the character you are playing.

                      The Dungeon Master is a mentor to a group of young friends, providing important advices and help for life matters,
                      often in a cryptic manner, but supplying clues in numerous opportunities so that the message can be unsderstood.


                      {query}

                   '''
model             =genai.GenerativeModel(model_name        =     model_name,
                                         generation_config =generation_config,
                                         safety_settings   =    safety_settings,
                                        #system_instruction=    system_instruction,
                                         tools             =    tools )
st.sidebar.divider()
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](  https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)
[![License]( https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)
                    ''')
st.sidebar.markdown('''2024.05.15 &copy; 2024 [ƊⱭȾɅViƧi🧿Ƞ](https://datavision.one/) &trade;''')

# MAIN

st.markdown('''![D&D](https://upload.wikimedia.org/wikipedia/en/d/d7/Dungeons_and_Dragons_DVD_boxset_art.jpg)''')
# Chat:
st.divider()
chat     =    model.start_chat(enable_automatic_function_calling=False)
res      =     chat.send_message(system_instruction.format(query='Start conversation.'))
res_text = res._result.candidates[0].content.parts[0].text
st.write('Dangeon Master:', res_text)

for message  in  st.session_state.messages:
    with         st.chat_message(message['role']):
                 st.markdown(message['content'])
if query := st.chat_input('Type message here…'):
            st.session_state.messages.append({'role':'user','content':query})
            with st.chat_message('user'):
                 st.markdown(query)

            with st.chat_message('assistant'):
                response=   chat.send_message(system_instruction.format(query=query))

            response            =     chat.send_message(query)
            response_text       = response._result.candidates[0].content.parts[0].text
            st.write('Dungeon Master:', response_text)

st.toast('Uni!', icon='🦄')
