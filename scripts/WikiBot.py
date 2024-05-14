import  textwrap
import  wikipedia
import  numpy               as   np
import  google.generativeai as   genai
import  google.ai.generativelanguage  as    glm
from wikipedia.exceptions import DisambiguationError, PageError
import  streamlit           as   st

st.set_page_config(page_title='SEARCH', page_icon='🔎', layout='wide', initial_sidebar_state='auto')

# Session Start:
st.session_state.setdefault(None)
if      'messages' not in st.session_state:st.session_state.messages=[]
if 'last_messages' not in st.session_state:st.session_state.last_messages=''

# API-KEY
api_key = st.secrets['api_key']
genai.configure(api_key=api_key)

# CONFIGS
# Search Function:
def wikipedia_search(search_queries:list[str])->list[str]:
    '''Search WikipediA for each query & summarize relevant docs.'''
    topics         = 3
    search_history =set()
    search_urls    =[]
    mining_model   =genai.GenerativeModel('gemini-pro')
    summary_results=[]
    for query in search_queries:
        print(f'Searching for "{query}"')
        search_terms = wikipedia.search(query)
        print(f'Related Search Terms: {search_terms[:topics]}')
        for    search_term in search_terms[:topics]:
            if search_term in search_history: continue
            print(f'Returning Page: "{search_term}"')
            search_history.add(search_term)
            try:
                page     = wikipedia.page(search_term, auto_suggest=False)
                url      = page.url
                print(f'Source: {url}')
                search_urls.append(url)
                page     = page.content
                response = mining_model.generate_content(textwrap.dedent(f'''\
                            Extracting relevant information about the query: {query}
                            Source:
        
                            {page}
                            
                            Note: Do not summarize. Only Extract and return the relevant information.'''))
                urls = [url]
                if response.candidates[0].citation_metadata:
                    extra_citations = response.candidates[0].citation_metadata.citation_sources
                    extra_urls      = [source.url for source in extra_citations]
                    urls.extend(extra_urls)
                    search_urls.extend(extra_urls)
                    print('Additional Citations:', response.candidates[0].citation_metadata.citation_sources)
                try                   :text = response.text
                except      ValueError:pass
                else                  :summary_results.append(text + '\n\nCom base em:\n  ' + ',\n  '.join(urls))
            except DisambiguationError:print(f'''Results when searching for "{search_term}"
                                        (originally for "{query}") were ambiguous, hence skipping…''')
            except           PageError:print(f'{search_term} did not match with any page id, hence skipping…')
            except      AttributeError:print(f'Unknown field for CitationSource: url, hence skipping…')
    print(f'Sources:')
    for url in search_urls            :print('  ', url)
    return summary_results
# Suplementary Search:
# Instructions:
instructions      ='''
You have access to the Wikipedia API which you will be using to answer a user's query.
Your job is to generate a list of search queries which might    answer a user's question.
Be creative by using various key-phrases from the user's query.
To generate variety of queries, ask questions which are related to the user's query that might help to find the answer.
The more queries you generate the better are the odds of you finding the correct answer.

Here is an example:

user: Tell me about Cricket World cup 2023 winners.

function_call: wikipedia_search(['What is the name of the team that
won the Cricket World Cup 2023?', 'Who was the captain of the Cricket World Cup
2023 winning team?', 'Which country hosted the Cricket World Cup 2023?', 'What
was the venue of the Cricket World Cup 2023 final match?', 'Cricket World cup 2023',
'Who lifted the Cricket World Cup 2023 trophy?'])

The search function will return a list of article summaries, use these to answer the  user's question.

Here is the user's query: {query}
                     '''

# SIDE
st.sidebar.image(   'https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg')
st.sidebar.markdown('[![Gemini](   https://img.shields.io/badge/Gemini-34A853?style=flat&logo=google&logoColor=EA4335&labelColor=4285F4&color=FBBC05)](https://gemini.google.com/)')
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
st.sidebar.info(   'Generation Config')
temperature       = st.sidebar.slider(      'Temperature:', 0.00,  1.00, 0.65, 0.05)
top_p             = st.sidebar.slider(      'Top P:'      , 0.00,  1.00, 0.95, 0.05)
top_k             = st.sidebar.number_input('Top K:'            ,  1,     100,    3)
max_output_tokens = st.sidebar.number_input('Max OutPut Tokens:',  1,    2048, 1024)
st.sidebar.divider()
# Safety Settings:
st.sidebar.success('Safety Settings')
seg               =   ['BLOCK_NONE','BLOCK_ONLY_HIGH', 'BLOCK_MEDIUM_AND_ABOVE', 'BLOCK_LOW_AND_ABOVE']
hate              = st.sidebar.selectbox(   'Hate:'      , seg, index=0)
harassment        = st.sidebar.selectbox(   'Harassment:', seg, index=0)
sexual            = st.sidebar.selectbox(   'Sexual:'    , seg, index=0)
dangerous         = st.sidebar.selectbox(   'Dangerous:' , seg, index=0)
# Building Model:
model_name        =  'gemini-pro'
generation_config = {'candidate_count'  :    1 ,
                     'temperature'      : temperature,
                     'top_p'            : top_p,
                     'top_k'            : top_k,
                     'stop_sequences'   : None ,
                     'max_output_tokens': max_output_tokens}
safety_settings   = {'HATE'             :hate,
                     'HARASSMENT'       :harassment,
                     'SEXUAL'           :sexual,
                     'DANGEROUS'        :dangerous}
tools             = [wikipedia_search]
model             =genai.GenerativeModel(model_name       =     model_name,
                                         generation_config=generation_config,
                                         safety_settings  =    safety_settings,
                                         tools            =    tools )
st.sidebar.divider()
st.sidebar.markdown('''2024.05.10 &copy; 2024 ƊⱭȾɅViƧi🧿Ƞ &trade;''')

# MAIN
st.image(   'https://pt.wikipedia.org/static/images/icons/wikipedia.png')
st.markdown('[![Wikipedia](https://img.shields.io/badge/WikipediA_Donation-636466?style=flat&logo=wikipedia&logoColor=000000&labelColor=FFFFFF&color=939598)](https://donate.wikimedia.org/w/index.php?title=Special:LandingPage&country=US&uselang=en)')
st.title(   'WikipediA Search')
# Chat:
chat   =  model.start_chat(history=[], enable_automatic_function_calling=False)
for message in st.session_state.messages:
          with      st.chat_message(message['role']):
                    st.markdown(message['content'])
if query :=    st.chat_input('Search WikipediA'):
                    st.session_state.messages.append({'role':'user', 'content':query})
                    with    st.chat_message('user'):
                            st.markdown(query)
                    with    st.chat_message('assistant'):
                            res      =    chat.send_message(instructions.format(query=query))
                            st.write('Searching…')
                            fc       =     res.candidates[0].content.parts[0].function_call
                            fc       =type(fc).to_dict(fc)
                            summaries=  wikipedia_search(**fc['args'])
                            st.write('Summaries:\n', summaries)
                            response = chat.send_message(glm.Content(parts=[glm.Part(
                                       function_response=glm.FunctionResponse(
                                                    name='wikipedia_search', response={'result':summaries}
                                                                                                        )
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        )
                            st.markdown(response.text)
                            # HyDE:
                            hyde           =  model.generate_content(f'''
                                Gere resposta hipotética para a busca do usuário usando seu próprio conhecimento.
                                Assuma que você sabe tudo sobre o tópico. Não use informação factual,
                                use substituições para completar sua resposta.
                                query: {query}
                                                                      ''')
                            st.write(hyde.text)
                            # Embedding Function:
                            def get_embeddings(content:list[str])->np.ndarray:
                                embeddings = genai.embed_content('models/embedding-001', content, 'SEMANTIC_SIMILARITY')
                                embds      = embeddings.get('embedding', None)
                                embds      = np.array(embds).reshape(len(embds),-1)
                                return embds
                            # Scalar Product:
                            def dot_product(a:np.ndarray,  b:np.ndarray):
                                return (a @ b.T)
                            # Getting Embeddings:
                                embed_query = get_embeddings([query])
                                embed_hyde  = get_embeddings([hyde.text])
                                embed_search= get_embeddings(summaries)
                            # Similarity Score:
                            sim_value       = dot_product(embed_search, embed_query)
                            sim_value       = dot_product(embed_search, embed_hyde )
                            # Query Rank:
                            st.write('  Query Scores:\n',                   sim_value_query)
                            st.write('\n  Ordered Query Scores:\n', np.sort(sim_value_query, axis=0)[::-1])
                            # Selecting Query Best Candidate:
                            st.write('\n  Rank:', np.argmax(sim_value_query), sim_value_query[0],'\n')
                            st.markdown(summaries[np.argmax(sim_value_query)])
                            # Query Rank:
                            st.write('  Query Scores:\n',                   sim_value_hyde)
                            st.write('\n  Ordered Query Scores:\n', np.sort(sim_value_hyde, axis=0)[::-1])
                            # Selecting Hyde Best Candidate:
                            st.write('\n  Rank:', np.argmax(sim_value_hyde), sim_value_hyde[0],'\n')
                            st.markdown(summaries[np.argmax(sim_value_hyde)])
st.divider()
st.toast('Search!', icon='🔍')
