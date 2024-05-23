# https://github.com/IAmCristiano/GokuAI/
# <a target=_blank href=https://icons8.com/icon/24563/indiana-jones>Indiana Jones</a> icon by <a target=_blank href=https://icons8.com/>Icons8</a>

import  streamlit           as   st
import  google.generativeai as   genai

st.set_page_config(page_title='Indiana Jones', page_icon='IMG/icons8-indiana-jones.svg', layout='wide', initial_sidebar_state='collapsed')

#  Session State Start:
st.session_state.setdefault(None)
if      'message' not in st.session_state:st.session_state.messages=[]
if      'api_key' not in st.session_state:st.session_state.api_key =True
if      'model'   not in st.session_state:st.session_state.model   =True
if      'chat'    not in st.session_state:st.session_state.chat    =True

# API-KEY
api_key = st.secrets['api_key']
genai.configure(api_key=api_key)

# SIDE
st.sidebar.image(   'https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg')
st.sidebar.markdown('[![Gemini](https://img.shields.io/badge/Gemini_by_Google-34A853?style=flat&logo=google&logoColor=EA4335&labelColor=4285F4&color=FBBC05)](https://gemini.google.com/)')
st.sidebar.title(   'ƊⱭȾɅViƧi🧿Ƞ')
st.sidebar.divider()
st.sidebar.info(    'Indiana')
st.sidebar.success( 'Jones')
# Building Model:
model_name        =  'gemini-pro'
generation_config = {'candidate_count'  : 1,
                     'temperature'      : 0.75,
                     'top_p'            : 0.95,
                     'top_k'            : 3,
                     'stop_sequences'   : None,
                     'max_output_tokens': 1024}
safety_settings   = {'HATE'             :'BLOCK_ONLY_HIGH',
                     'HARASSMENT'       :'BLOCK_ONLY_HIGH',
                     'SEXUAL'           :'BLOCK_ONLY_HIGH',
                     'DANGEROUS'        :'BLOCK_ONLY_HIGH'}
tools             =   None
system_instruction='''
                      Você é o Indiana Jones, personagem de filmes, séries de TV e livros, falando com o Leonardo.
                      Responda sempre de forma amigável e coerente com o personagem Indiana Jones.
                      Responda sempre em português do Brasil.
                      
                      Quando perguntado sobre fatos reais,
                      responda sempre com o conteúdo correto relacionado ao assunto,
                      incluindo referências às aventuras do Indiana Jones para manter o interesse.

                      Lembre-se que o Indiana Jones é um grande arqueólogo com PhD, com grande conhecimento histórico e de artefatos arqueológicos.
                      Lembre-se também que o Indiana Jones é professor universitário renomado.
                      Você então conhece muito desses assuntos bem como assuntos relacionados a artes plásticas.
                      Os pintores favoritos do Leonardo são Bartolomé Esteban Murillo, Willem Adolphe-Bouguereau, Norman Rockwell, Ernst Carlos, Alex Ross.
                      Você já está com 70 anos e já viveu muitas aventuras e passou por muitas situações.
                      Agora você aconselha pessoas mais jovens, como se fossem seus ex-alunos.

                      Henry Walton Jones Jr. é um indivíduo com vida dupla: além de pacato professor de Arqueologia,
                      é um aventureiro destemido e pouco convencional, com seu chicote e chapéu,
                      ele é mais conhecido por Indiana, apelido tirado do nome do cão que tinha quando criança.
                      Possui senso de humor, conhecimento profundo de muitas civilizações e línguas antigas e medo de cobras.

                      In his role as a college professor of archaeology Jones is scholarly, wears a tweed suit, and lectures on ancient civilizations.
                      At the opportunity to recover important artifacts, Dr. Jones transforms into Indiana, a non-superhero superhero image he has concocted for himself.
                      Indy is a fallible character. He makes mistakes and gets hurt. He's a real character, not a character with superpowers.
                      He express his pain and get his mad out and to take pratfalls and sometimes be the butt of his own jokes.
                      Indiana Jones is not a perfect hero, and his imperfections make people feel that, with a little more exercise and a little more courage, they could be just like him.
                      Indiana created his heroic figure so as to escape the dullness of teaching at a school.
                      Both of Indiana's personas reject one another in philosophy, creating a duality.
                      Indiana is both a romantic and a cynic, having traits of a lone wolf, a man on a quest, a noble treasure hunter, a hardboiled detective, and a human superhero.

                      Se query tiver conteúdo sensível, racista, sexual, homofóbico ou discurso de ódio,
                      desaprove a conversao ao estilo do Indiana Jones.

                      {query}

                   '''
model             =genai.GenerativeModel(model_name        =     model_name,
                                         generation_config =generation_config,
                                         safety_settings   =    safety_settings,
                                        #system_instruction=    system_instruction,
                                         tools             =    tools )
st.sidebar.divider()
st.sidebar.markdown('''
![2024.05.15](  https://img.shields.io/badge/24.05.15-000000)

[![GitHub](     https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](     https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](   https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](     https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)

[![License](    https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logo=&logoColor=0065FF&label=&copy;2024&labelColor=0065FF&color=0065FF)](https://datavision.one/)
                    ''')

# MAIN
st.markdown('''![Indiana Jones](https://images.disneymovieinsiders.com/6a5f34338b5d6d2809d22332629893ae/29fc4360-3592-4361-a6bf-50255a295e4b.jpg)''')
st.divider()
# Chat:
chat            =model.start_chat(enable_automatic_function_calling=False)
start           = chat.send_message(system_instruction.format(query='Inicie a conversa'))
ai_avatar       ='🧔‍♂️'
hm_avatar       ='🧑🏻'
if 'message' not in st.session_state:
        with  st.chat_message('ai', avatar='🧔‍♂️'):
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
        st.session_state.messages.append({'role':'ai','content':response.text})
        st.write(response.text)

st.toast('Indy!', icon='🪬')
