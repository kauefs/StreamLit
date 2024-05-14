import  textwrap
import  wikipedia
import  numpy               as   np
import  google.generativeai as   genai
import  google.ai.generativelanguage   as  glm
from wikipedia.exceptions import DisambiguationError, PageError
import  streamlit           as   st

st.set_page_config(page_title='SEARCH', page_icon='🔎', layout='wide', initial_sidebar_state='auto')

# Iniciando Sessão:
st.session_state.setdefault(None)
if      'messages' not in st.session_state:st.session_state.messages=[]
if 'last_messages' not in st.session_state:st.session_state.last_messages=''

# API-KEY
api_key = st.secrets['api_key']
genai.configure(api_key=api_key)

# CONFIGURAÇÕES GERAIS
# Função de Busca na WikePédia:
def wikipedia_search(search_queries:list[str])->list[str]:
    '''WikipediA research returning most relevant pages.'''
    topics         = 3
    search_history =set()
    search_urls    =[]
    mining_model   =genai.GenerativeModel('gemini-pro')
    summary_results=[]
    for query in search_queries:
        print(f'Searching for "{query}"')
        search_terms = wikipedia.search(query)
        print(f'Related Topics: {search_terms[:topics]}')
        for    search_term in search_terms[:topics]:
            if search_term in search_history: continue
            print(f'Returning page: "{search_term}"')
            search_history.add(search_term)
            try:
                page     = wikipedia.page(search_term, auto_suggest=False)
                url      = page.url
                print(f'Source: {url}')
                search_urls.append(url)
                page     = page.content
                response = mining_model.generate_content(textwrap.dedent(f'''\
                            Extracting relevant information about the researshed term: {query}
                            Source:
        
                            {page}
                            
                            Note: no summary, extracting only relevant information.'''))
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
                                        (originated from "{query}") were ambiguous, dropping…''')
            except           PageError:print(f'{search_term} did not find a page, dropping…')
    print(f'Sources:')
    for url in search_urls            :print('  ', url)
    return summary_results
# Buscas Suplementares:
# Passando Instruções ao Modelo:
instructions      ='''
Acesso a API da WikipédiA para responder buscas.
Gerar lista de possíveis resultados que possam responder a buscas.
Seja criativo usando frases chave da busca.
Gerar variedade de resultados fazendo perguntas relacionadas à busca para encontrar a melhor resposta.
Quanto mais perguntas gerar, melhores as changes de encontrar a resposta correta.

Exemplo: 

user: Fale-me sobre os vencedores da Copa do Mundo de 2022.

function_call: wikipedia_search(['Qual time ganhou a Copa do Mundo de 2022?',
'Quem era o capitaão do time que ganhou a Copa do Mundo de 2022?',
'Que país sediou a Copa do Mundo de 2022?',
'Em qual estádio aconteceu o jogo da final da Copa do Mundo de 2022?',
'Copa do Mundo de 2022','Quem levantou o troféu da Copa do Mundo de 2022?'])

Use a lista de resumo de artigos retornada pela função de busca para responder ao usuário.

Busca do usuário: {query}
                    '''

# SIDE
st.sidebar.image(   'https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg')
st.sidebar.markdown('[![Gemini](   https://img.shields.io/badge/Gemini-34A853?style=flat&logo=google&logoColor=EA4335&labelColor=4285F4&color=FBBC05)](https://donate.wikimedia.org/w/index.php?title=Special:LandingPage&country=BR&uselang=pt-br)')
st.sidebar.image(   'https://pt.wikipedia.org/static/images/icons/wikipedia.png')
st.sidebar.markdown('[![Wikipedia](https://img.shields.io/badge/WikipediA_Donation-636466?style=flat&logo=wikipedia&logoColor=000000&labelColor=FFFFFF&color=939598)](https://donate.wikimedia.org/w/index.php?title=Special:LandingPage&country=US&uselang=en)')
st.sidebar.title(   'AI Google Gemini')
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium](  https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn](https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)
[![License]( https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)
                    ''')
st.sidebar.divider()
# Configuração do Modelo Generativo:
st.sidebar.info(   'Generation Config')
temperature       = st.sidebar.slider(      'Temperature:', 0.00,  1.00, 0.65, 0.05)
top_p             = st.sidebar.slider(      'Top P:'      , 0.00,  1.00, 0.95, 0.05)
top_k             = st.sidebar.number_input('Top K:'            ,  1,     100,    3)
max_output_tokens = st.sidebar.number_input('Max OutPut Tokens:',  1,    2048, 1024)
st.sidebar.divider()
# Configurações de Segurança:
st.sidebar.success('Safety Settings')
seg               =   ['BLOCK_NONE','BLOCK_ONLY_HIGH', 'BLOCK_MEDIUM_AND_ABOVE', 'BLOCK_LOW_AND_ABOVE']
hate              = st.sidebar.selectbox(   'Hate:'      , seg, index=0)
harassment        = st.sidebar.selectbox(   'Harassment:', seg, index=0)
sexual            = st.sidebar.selectbox(   'Sexual:'    , seg, index=0)
dangerous         = st.sidebar.selectbox(   'Dangerous:' , seg, index=0)
# Configurando Modelo:
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
# Construindo Modelo:
model             =genai.GenerativeModel(model_name       =     model_name,
                                         generation_config=generation_config,
                                         safety_settings  =    safety_settings,
                                         tools            =    tools )
st.sidebar.divider()
st.sidebar.markdown('''2024.05.10 &copy; 2024 ƊⱭȾɅViƧi🧿Ƞ &trade;''')

# MAIN
st.title('WikipediA Search')
st.markdown('''
            Inspired by an [exemplo](https://github.com/google-gemini/cookbook/blob/main/examples/Search_reranking_using_embeddings.ipynb) from Google,
            using _Embedding_ from Google's Artificial Inteligence (AI) **Gemini** to rerank search results in WikipediA.

            _Embedding_ é uma técnica de Processamento de Linguagem Natural (PLN) que converte texto em vetores numéricos,
            capturando significado semântico **&** contexto, de forma que textos com conteúdos semelhantes apresentam _embeddings_ mais próximos,
            permitindo comparações textuais e o relacionamento entre textos, facilitando busca **&** classificação.
            ''')
st.divider()
# Chat de Pesquisa:
chat   =  model.start_chat(enable_automatic_function_calling=False)
st.subheader('Search WikipediA from here:')
for message in st.session_state.messages:
          with      st.chat_message(message['role']):
                    st.markdown(message['content'])
if query :=    st.chat_input('Search WikipediA from here.'):
                    st.session_state.messages.append({'role':'user', 'content':query})
                    with    st.chat_message('user'):
                            st.markdown(query)
                    with    st.chat_message('assistant'):
                            result   =    chat.send_message(instructions.format(query=query))
                            st.write('Searching…')
                            fc       =  result.candidates[0].content.parts[0].function_call
                            fc       =type(fc).to_dict(fc)
                            summaries=  wikipedia_search(**fc['args'])
                            st.write('Consultations:\n', summaries)
                            response = chat.send_message(glm.Content(parts=[glm.Part(
                                       function_response=glm.FunctionResponse(
                                                    name='wikipedia_search', response={'result':summaries}
                                                                                                        )
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        )
                            st.markdown(response.text)
                            # Função Embedding:
                            def get_embeddings(content:list[str])->np.ndarray:
                                embeddings = genai.embed_content('models/embedding-001', content, 'SEMANTIC_SIMILARITY')
                                embds      = embeddings.get('embedding', None)
                                embds      = np.array(embds).reshape(len(embds),-1)
                                return embds
                            # Função Produto Escalar:
                            def dot_product(a:np.ndarray,  b:np.ndarray):
                                return (a @ b.T)
                            # Aplicando a Função Embedding:
                            search_res     = get_embeddings(summaries)
                            embedded_query = get_embeddings([query])
                            # Calculando Pontuação de Similaridade:
                            sim_value      = dot_product(search_res, embedded_query)
                            st.markdown(summaries[np.argmax(sim_value)])
                            st.write('Rank:', sim_value[0])
                            hyde             =model.generate_content(f'''
                                Gere resposta hipotética para a busca do usuário usando seu próprio conhecimento.
                                Assuma que você sabe tudo sobre o tópico. Não use informação factual,
                                use substituições para completar sua resposta.
                                query: {query}
                                                                      ''')
                            st.write(hyde.text)
                            # Embedding a resposta hipotética para comparar com os resultados da busca:
                            hyde_res  = get_embeddings([hyde.text])
                            # Calculando Pontuação de Similaridade para Ranquear os Resultados:
                            sim_value = dot_product(search_res, hyde_res)
                            st.markdown(summaries[np.argmax(sim_value)])
                            st.write('Rerank:', sim_value[0])
st.divider()
st.toast('Search!', icon='🔍')
