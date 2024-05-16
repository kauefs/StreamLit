# https://github.com/IAmCristiano/GokuAI/
# <a target="_blank" href="https://icons8.com/icon/tlzsVoeHOw9V/scooby-doo">Scooby Doo</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
# 'https://static.wikia.nocookie.net/disneyfanon/images/5/56/Scooby_Doo_Clipart_APNSD.png'

import streamlit           as st
import google.generativeai as genai

st.set_page_config(page_title='Scooby-Doo', page_icon='img/icons8-scooby-doo.svg', layout='wide', initial_sidebar_state='collapsed')

#  Session State Start:
st.session_state.setdefault(None)
if      'messages' not in st.session_state:st.session_state.messages=[]
if 'last_messages' not in st.session_state:st.session_state.last_messages=''

# API-KEY
api_key = st.secrets['api_key']
genai.configure(api_key=api_key)

# SIDE
st.sidebar.image(   'https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg')
st.sidebar.markdown('[![Gemini](   https://img.shields.io/badge/Gemini_by_Google-34A853?style=flat&logo=google&logoColor=EA4335&labelColor=4285F4&color=FBBC05)](https://gemini.google.com/)')
st.sidebar.title(   'ƊⱭȾɅViƧi🧿Ƞ')
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](  https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)
[![License]( https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)
                    ''')
st.sidebar.divider()
# Generative Model Config:
st.sidebar.info(   'A Pup Named')
# st.sidebar.info(   'Generation Config')
# temperature       = st.sidebar.slider(      'Temperature:', 0.00,  1.00, 0.65, 0.05)
# top_p             = st.sidebar.slider(      'Top P:'      , 0.00,  1.00, 0.95, 0.05)
# top_k             = st.sidebar.number_input('Top K:'            ,  1,     100,    3)
# max_output_tokens = st.sidebar.number_input('Max OutPut Tokens:',  1,    2048, 1024)
# st.sidebar.divider()
# Safety Settings:
st.sidebar.success('Scooby-Doo')
# st.sidebar.success('Safety Settings')
# seg               =   ['BLOCK_NONE','BLOCK_ONLY_HIGH', 'BLOCK_MEDIUM_AND_ABOVE', 'BLOCK_LOW_AND_ABOVE']
# hate              = st.sidebar.selectbox(   'Hate:'      , seg, index=0)
# harassment        = st.sidebar.selectbox(   'Harassment:', seg, index=0)
# sexual            = st.sidebar.selectbox(   'Sexual:'    , seg, index=0)
# dangerous         = st.sidebar.selectbox(   'Dangerous:' , seg, index=0)
# Building Model:
model_name        =  'gemini-pro'
generation_config = {'candidate_count'  : 1,
                     'temperature'      : 0.75,
                     'top_p'            : 0.95,
                     'top_k'            : 3,
                     'stop_sequences'   : None,
                     'max_output_tokens': 1024}
safety_settings   = {'HATE'             :'BLOCK_MEDIUM_AND_ABOVE',
                     'HARASSMENT'       :'BLOCK_MEDIUM_AND_ABOVE',
                     'SEXUAL'           :'BLOCK_MEDIUM_AND_ABOVE',
                     'DANGEROUS'        :'BLOCK_MEDIUM_AND_ABOVE'}
tools             =   None
system_instruction='''
                      Você é o Scooby-Doo, personagem de desenho animado, falando com uma jovem menina.
                      Responda sempre de forma amigável, entusiasmada e coerente com o personagem Scooby-Doo.
                      Responda sempre em português do Brasil.

                      
                      
                      Se for perguntado sobre assuntos de escola ou lição (dever) de casa,
                      responda sempre com o conteúdo correto relacionado ao assunto,
                      incluindo referências do Scooby-Doo para manter o interesse.

                      Lembre-se que o Scooby-Doo e seu inseparável amigo Salsicha gostam muito de comer.
                      Você então conhece muitas receitas e também entende bastante sobre mesa posta.
                      
                      Se query tiver conteúdo sensível, racista, sexual, homofóbico ou discurso de ódio,
                      desaprove e não converse sobre isso, respondendo 'Ei, não é legal falar assim! Vamos conversar sobre outra coisa.'

                      {query}

                   '''
model             =genai.GenerativeModel(model_name        =     model_name,
                                         generation_config =generation_config,
                                         safety_settings   =    safety_settings,
                                        #system_instruction=    system_instruction,
                                         tools             =    tools )
st.sidebar.divider()
st.sidebar.markdown('''2024.05.15 &copy; 2024 [ƊⱭȾɅViƧi🧿Ƞ](https://datavision.one/) &trade;''')

# MAIN
st.markdown('''![PupScooby](https://github.com/kauefs/StreamLit/raw/%40/img/PupScooby.png)''')
st.title(   'A Pup Named Scooby-Doo!')
# Chat:

# ss       =  '''
#                 Se prompt contiver conteúdo sensível, racista, sexual, homofóbico ou discurso de ódio,
#                 desaprove e não converse sobre isso.
#                 '''

chat     =    model.start_chat(enable_automatic_function_calling=False)
res      =     chat.send_message(system_instruction.format(query='Faça uma breve saudação.'))
res_text = res._result.candidates[0].content.parts[0].text
st.write('Scooby-Doo:', res_text)

for message  in  st.session_state.messages:
    with         st.chat_message(message['role']):
                 st.markdown(message['content'])
if query := st.chat_input('Digite aqui sua mensagem…'):
            st.session_state.messages.append({'role':'user','content':query})
            with st.chat_message('user'):
                 st.markdown(query)

            with st.chat_message('assistant'):
                response=   chat.send_message(system_instruction.format(query=query))

                # if  ss in query:
                #     st.write('Ei, não é legal falar assim! Vamos conversar sobre outra coisa.')

            response            =     chat.send_message(query)
            response_text       = response._result.candidates[0].content.parts[0].text
            st.write('Scooby-Doo:', response_text)

st.toast('Scooby-Doo!', icon='🐕')
