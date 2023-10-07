#https://www.youtube.com/watch?v=KlillpfYK6g
import  pandas   as pd
import  pydeck   as pdk
import streamlit as st
st.set_page_config(page_title='SP', page_icon='🔫')
@st.cache_data
def load_data():
    df      = pd.read_csv('datasets/CriminalidadeSP.csv')
    return df
df          = load_data()
st.title(    '   Criminalidade  em São Paulo')
st.markdown('''**Criminalidade** é problema recorrente nas grandes cidades brasileiras,
                 apesar da busca constante por soluções para a questão.
                 Técnicas de Ciência de Dados podem ajudar a melhor compreender a situação,
                 podendo gerar _InSights_ para direcionar ações de combate ao crime.''')
df.time     =  pd.to_datetime(df.time)
st.sidebar.title('DashBoard')
ano         =  st.sidebar.slider('Escolha do Ano:', 2010, 2018, 2014)
FilteredDF  =  df[(df.time.dt.year == ano)]
st.sidebar.info( ' {} Registros'.format(FilteredDF.shape[0]))
if  st.sidebar.checkbox('Exibir Tabela', value=True):
    st.subheader(       'Dados:')
    st.markdown( '''     Fonte: [GeoSpatial Sao Paulo Crime DataBase](https://www.kaggle.com/datasets/danlessa/geospatial-sao-paulo-crime-database/data)''')
    st.markdown(f'''➡️Exibindo   {' **{}** ocorrências'.format(FilteredDF.shape[0])} em **{ano}**:''')
    st.write(FilteredDF)
st.sidebar.write('Opções de Mapa:')
if  st.sidebar.checkbox('Complexo', value=True):
    st.subheader('Mapa   Complexo:')
    st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(longitude=-46.65,
                                                          latitude =-23.55,
                                                          zoom     =  8   ,
                                                          min_zoom =  None,
                                                          max_zoom =  None,
                                                          pitch    = 50   ,
                                                          bearing  = 50)  ,
                                    layers=[pdk.Layer('HexagonLayer'      ,
                                            data           = FilteredDF,
                                            get_position   = '[longitude,latitude]',
                                            auto_highlight = True,
                                            elevation_scale= 50,
                                            elevation_range=[ 0,2750],
                                            pickable=True,
                                            extruded=True,
                                            coverage=1)],
                                    views=[{'@@type':'MapView', 'controller':True}],
                                    map_style   ='dark',
                                    api_keys    = None ,
                                    width       ='100%',
                                    height      = 500  ,
                                    tooltip     = True, #{'text':'Bairro {bairro}'},
                                    description ='CriminalidadeSP',
                                    effects     = None ,
                                    map_provider='carto',
                                    parameters  = None))
if  st.sidebar.checkbox('Simples'):
    st.subheader('Mapa   Simples:')
    st.map(FilteredDF)
