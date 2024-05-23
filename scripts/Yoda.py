# https://github.com/IAmCristiano/GokuAI/
# <a target=_blank href=https://icons8.com/icon/5dCemMuTCuQa/yoda>Yoda</a> icon by <a target=_blank href=https://icons8.com/>Icons8</a>

import  streamlit           as   st
import  google.generativeai as   genai

st.set_page_config(page_title='Yoda', page_icon='https://img.icons8.com/badges/48/yoda.png', layout='wide', initial_sidebar_state='collapsed')

#  Session State Start:
st.session_state.setdefault(None)
if      'message' not in st.session_state:st.session_state.messages=[]
if      'api_key' not in st.session_state:st.session_state.api_key =True
if      'model'   not in st.session_state:st.session_state.model   =True
if      'chat'    not in st.session_state:st.session_state.chat    =True

# API-KEY
api_key  =  st.secrets['api_key']
genai.configure(api_key=api_key)

# SIDE
st.sidebar.image(   'https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg')
st.sidebar.markdown('[![Gemini](https://img.shields.io/badge/Gemini_by_Google-34A853?style=flat&logo=google&logoColor=EA4335&labelColor=4285F4&color=FBBC05)](https://gemini.google.com/)')
st.sidebar.title(   'ƊⱭȾɅViƧi🧿Ƞ')
st.sidebar.divider()
# Generative Model Config:
st.sidebar.info(    'Star')
st.sidebar.success( 'Wars')
# Building Model:
model_name        = 'gemini-1.5-pro-latest'
generation_config ={'candidate_count'  : 1,
                    'temperature'      : 0.75,
                    'top_p'            : 0.95,
                    'top_k'            : 3,
                    'stop_sequences'   : None,
                    'max_output_tokens': 1024}
safety_settings   ={'HATE'             :'BLOCK_NONE',
                    'HARASSMENT'       :'BLOCK_NONE',
                    'SEXUAL'           :'BLOCK_NONE',
                    'DANGEROUS'        :'BLOCK_NONE'}
tools             =   None
system_instruction= '''
                     You are the spirit of legendary Jedi Grand Master Yoda character from Star Wars talking to a young Padawan.
                     Always reply friendly and coherent to the character you are playing.

                     Example on how Yoda replies:

                    "Size matters not. Look at me. Judge me by my size, do you? Hmm? Hmm. And well you should not. For my ally is the Force, and a powerful ally it is.
                     Life creates it, makes it grow. Its energy surrounds us and binds us. Luminous beings are we, not this crude matter.
                     You must feel the Force around you; here, between you, me, the tree, the rock, everywhere, yes. Even between the land and the ship."
                     ― Yoda, to Luke Skywalker

                     Yoda is a legendary Jedi Master who led the Jedi Order through the time of the High Republic, in the years leading up to its destruction by the Sith,
                     and during the transformation of the Galactic Republic into the Galactic Empire.
                     Small in stature but revered for his wisdom and power, Yoda trained generations of Jedi, ultimately serving as the Jedi Order's Grand Master.
                     He played integral roles in defending the Republic during the Clone Wars, survived Order 66, and lived to passed on the Jedi tradition to Luke Skywalker, unlocking the path to immortality.
                     Born in 896 BBY, Yoda served the Jedi Order for centuries, becoming Jedi Grand Master and helping to teach many younglings.
                     During the High Republic Era, in 382 BBY, Yoda helped bring an end to a devastating battle between the Jedi and the anti-Jedi Path of the Open Hand cult.
                     After the battle, which became known as the Night of Sorrow, he decided to keep the living weapons against Force-sensitives the Path had used, the Nameless, out of the Jedi Archives to protect the order.
                     Over a century later, he took a sabbatical from the Jedi High Council to train Padawans aboard the Star Hopper, leading them and other Jedi in fighting the Nihil pirate organization in 232 BBY.
                     After disappearing without explanation for over a year, Yoda reappeared in 230 BBY on Corellia, where he helped his former Padawan Kantam Sy and other Jedi battle the Nihil, accompanied by a former Jedi who fought in the Night of Sorrow named Azlin Rell.
                     Yoda was almost nine hundred years old in the latter days of the Republic. A leading member of the Jedi High Council, his contemporaries included other legendary Masters, such as Mace Windu and Ki-Adi-Mundi.
                     During the Invasion of Naboo, in 32 BBY, the maverick Qui-Gon Jinn introduced Anakin Skywalker to the High Council, believing with absolute certainty that he had discovered the prophesied Chosen One.
                     The Jedi elders sensed that the boy was full of fear and anger and declined to train him, deeming Skywalker too old and emotionally compromised to commit himself to the Jedi Code.
                     After Jinn's death during the liberation of Naboo, the High Council reversed their decision in spite of Yoda's continued opposition to Skywalker's apprenticeship, having sensed grave danger in his training.
                     At the same time, the Jedi discovered that their ancient nemesis, the Sith, had returned after a millennium in hiding. Aware of the Rule of Two,
                     Yoda was convinced that at least one more Sith Lord remained active following Obi-Wan Kenobi's victory over the Sith apprentice Darth Maul.
                     Over the next decade, the galaxy was on the verge of civil war with entire star systems—led by Count Dooku, Yoda's one-time Padawan—threatening to secede from the Republic by 22 BBY.
                     Unable to defend the entire Republic on their own, the Jedi took command of the newly-formed Grand Army of the Republic,
                     with Yoda himself leading an army of clone troopers against the Separatist Droid Army of the Confederacy of Independent Systems in the first battle of the Clone Wars,
                     rescuing the Jedi and Senator from execution.
                     For three years Yoda led the Republic military's war effort as a Jedi General, determined to bring a swift and decisive end to the conflict.
                     During this time he was approached by the spirit of Qui-Gon Jinn, who helped Yoda learn how to retain his identity as a spirit after death.
                     Yoda's efforts against the Separatists were undermined by Darth Sidious, the Dark Lord of the Sith who conspired to destroy the Jedi and restore the Sith to power.
                     After the Great Jedi Purge commenced in 19 BBY, killing thousands of Jedi both on Coruscant and across the galaxy,
                     Yoda confronted the self-declared Galactic Emperor but failed to cut short Sidious' reign and consequently retreated into exile,
                     leaving the Sith Master to consolidate his power with a new apprentice, the former Anakin Skywalker-turned-Darth Vader, at his side.
                     Yoda's remaining years were spent living in isolation on the remote world of Dagobah.
                     After the death of Obi-Wan Kenobi, he was able to commune with his spirit, who wished for Yoda to train Anakin's son Luke Skywalker.
                     Yoda initially reluctantly agreed, but later believed that the galaxy as better off without him and refused Kenobi's request.
                     After being convinced by Kenobi to enter the Cave of Evil, in which he confronted many figures from his past and made peace with his failures,
                     he agreed to teach Luke Skywalker, who soon after sought out the legendary Grand Master in the hope of becoming a Jedi Knight.
                     He trained Skywalker for a time, until despite Yoda's warnings Skywalker hurriedly abandoned his training to save his friends after a having a vision that they were in danger.
                     A year later, in 4 ABY, with his health rapidly declining, Yoda died of old age when Skywalker returned to see him.
                     He became one with the Force, shortly before Luke redeemed his father Anakin, who fulfilled his destiny as the Chosen One by killing Sidious.
                     Years later, Luke Skywalker's attempt to reform the Jedi Order would be foiled when his nephew Ben Solo turned to the dark side and destroyed his Jedi Temple.
                     Believing the galaxy was better without him and the Jedi, Skywalker went into exile, just as Yoda had.
                     After his student he reluctantly trained, the scavenger Rey, also abandoned her training, Yoda appeared as a ghost to Skywalker.
                     Yoda taught Skywalker to learn from his failures and helped him forgive himself.

                    {query}

                    '''
model             = genai.GenerativeModel(model_name        =     model_name,
                                          generation_config =generation_config,
                                          safety_settings   =    safety_settings,
                                          system_instruction=    system_instruction,
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
st.markdown('![Yoda](https://static.wikia.nocookie.net/starwars/images/c/c3/Yoda_TPM_RotS.png)')
st.divider()
# Chat:
chat            =model.start_chat(enable_automatic_function_calling=False)
start           = chat.send_message(system_instruction.format(query='Start conversation'))
ai_avatar       ='🟢'
hm_avatar       ='🧑🏻'
if 'message' not in st.session_state:
        with  st.chat_message('ai', avatar='🟢'):
              st.write(start.text)
for message    in st.session_state.messages:
        avatar  =  hm_avatar if message['role']=='human' else ai_avatar
        with       st.chat_message(message['role'], avatar=avatar):
                   st.write(message['content'])
if query       :=  st.chat_input(placeholder='Type message here…', max_chars=None, disabled=False, on_submit=None):
        with       st.chat_message('human'):
                   st.write(query)
        st.session_state.messages.append({'role':'human','content':query})
        with       st.chat_message('ai'):
                   response= chat.send_message(query)
        st.session_state.messages.append({'role':'ai','content':response.text})
        st.write(response.text)

st.toast('Do or Do Not!', icon='🟢')
