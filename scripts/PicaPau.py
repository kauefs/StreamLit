# https://github.com/IAmCristiano/GokuAI/
# <a target=_blank href=https://icons8.com/icon/32453/woody-woodpecker>Woody Woodpecker</a> icon by <a target=_blank href=https://icons8.com/>Icons8</a>

import streamlit           as   st
import google.generativeai as   genai

st.set_page_config(page_title='Pica-Pau', page_icon='img/icons8-woody-woodpecker.svg', layout='wide', initial_sidebar_state='collapsed')

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
st.sidebar.info(    'Pica')
st.sidebar.success( 'Pau')
# Building Model:
model_name        = 'gemini-pro'
generation_config ={'candidate_count'  : 1,
                    'temperature'      : 0.65,
                    'top_p'            : 0.95,
                    'top_k'            : 3,
                    'stop_sequences'   : None,
                    'max_output_tokens': 1024}
safety_settings   ={'HATE'             :'BLOCK_LOW_AND_ABOVE',
                    'HARASSMENT'       :'BLOCK_LOW_AND_ABOVE',
                    'SEXUAL'           :'BLOCK_MEDIUM_AND_ABOVE',
                    'DANGEROUS'        :'BLOCK_LOW_AND_ABOVE'}
tools             =  None
system_instruction='''
                     Você é o Pica-Pau, personagem de desenho animado, falando com uma criança (menino).
                     Responda sempre de forma amigável, entusiasmada e coerente com o personagem Pica-Pau.
                      
                     Se for perguntado sobre assuntos de escola ou lição (dever) de casa,
                     responda sempre com o conteúdo correto relacionado ao assunto,
                     incluindo referências do Pica-Pau para manter o interesse.
                      
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
st.sidebar.markdown('''
![2024.05.15](  https://img.shields.io/badge/2024.05.15-000000)

[![GitHub](     https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](     https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](   https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](     https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)

[![License](    https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logo=&logoColor=0065FF&label=&copy;2024&labelColor=0065FF&color=0065FF)](https://datavision.one/)
                    ''')

# MAIN
st.title(   'Converse com o Pica-Pau!')
st.markdown('''![Pica-Pau](https://static.wikia.nocookie.net/walterlantz/images/8/84/Woody_Woodpecker_artwork.png)''')

def safety(chat, prompt):
    prompt       ='''
                Se prompt contiver conteúdo sensível, racista, sexual, homofóbico ou discurso de ódio,
                desaprove e não converse sobre isso.

                {prompt}

                  '''
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return 'Ei, não é legal falar assim! Vamos conversar sobre outra coisa.'

st.divider()
# Chat:
ss      ='Se prompt contiver conteúdo sensível, racista, sexual, homofóbico ou discurso de ódio, desaprove e não converse sobre isso.'
chat            =model.start_chat(enable_automatic_function_calling=False)
start           = chat.send_message(system_instruction.format(query='Inicie a conversa'))
ai_avatar       ='🐤'
hm_avatar       ='👦🏼'
if 'message' not in st.session_state:
        with  st.chat_message('ai', avatar='🐤'):
              st.write(start.text)
for message    in st.session_state.messages:
        avatar  =  hm_avatar if message['role']=='human' else ai_avatar
        with       st.chat_message(message['role'], avatar=avatar):
                   st.write(message['content'])
if query       :=  st.chat_input(placeholder='Digite aqui sua mensagem…', max_chars=None, disabled=False, on_submit=None):
        with       st.chat_message('human'):
                   st.write(query)
        st.session_state.messages.append({'role':'human','content':query})
        with       st.chat_message('ai'):
                   response= chat.send_message(system_instruction.format(query=query))

        if  ss in query:
                   st.write('Ei, não é legal falar assim! Vamos conversar sobre outra coisa.')

        st.session_state.messages.append({'role':'ai','content':response.text})
        st.write(response.text)

st.toast('Pica-Pau!', icon='🐤')
