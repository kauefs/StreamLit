import pandas           as pd
import altair           as alt
import streamlit        as st
from   urllib.error import URLError
import sys
st.set_page_config(page_title='ƊⱭȾɅViƧi&#x1F9FF;Ƞ', page_icon='👨🏻‍💻', layout='wide', initial_sidebar_state='expanded')
# DATA:
@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL  =    'https://streamlit-demo-data.s3-us-west-2.amazonaws.com'
    df              =   pd.read_csv(AWS_BUCKET_URL + '/agri.csv.gz')
    return df.set_index('Region')
# SIDE:
st.sidebar.title('ƊⱭȾɅViƧi&#x1F9FF;Ƞ')
st.sidebar.markdown('''Data Science **|** Computer Vision **|** ML **|** AI **|** ☁️ **|** CyberSecurity **|**  👨🏻‍💻''')
st.sidebar.divider(                )
with    st.sidebar.container(      ):
    if  st.button('StreamLit Hello'):
        st.sidebar.success( 'Hello World!')
    else:
        st.sidebar.info(    'Hello There' )
st.sidebar.divider(                       )
st.sidebar.header('Data Analysis')
PlaceHolder = st.sidebar.empty(  )
st.sidebar.markdown(sys.version  )
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](                                 https://github.com/kauefs/)
[![Medium](  https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](                                 https://medium.com/@kauefs)
[![LinkedIn](https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](                               https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)
[![License]( https://img.shields.io/github/license/kauefs/StreamLit?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)

2024.04.01 &copy; 2024 [![ƊⱭȾɅViƧi🧿Ƞ]( https://img.shields.io/badge/ViƧi🧿Ƞ-0065FF?style=plastic&logo=&logoColor=0065FF&label=ƊⱭȾɅ&labelColor=0065FF&color=0065FF)](https://datavision.one/)
 &trade;''')
# MAIN:
st.markdown('''![ƊⱭȾɅViƧi&#x1F9FF;Ƞ](https://raw.githubusercontent.com/kauefs/StreamLit/%40/img/DataVision3.png)''')
st.divider()
st.title(       'StreamLitDEMO')
st.header(      'DataFrame&Chart')
try:
    df              = get_UN_data()
    countries       =  st.multiselect('🌎🌍🌏:', list(df.index), ['Australia', 'Brazil', 'China', 'France', 'Germany', 'United States of America'])
    if not countries:  st.error(      'Please select at least one country.')
    else:
        data        =  df.loc[countries]
        data       /=      1000000.0
        st.write(                     '### Gross Agricultural Production ($B)', data.sort_index())
        data        = data.T.reset_index()
        data        =  pd.melt(data, id_vars=['index']).rename(columns={'index':'year', 'value':'Gross Agricultural Product ($B)'})
        chart       =(alt.Chart(data).mark_area(opacity=.25).encode(x    =      'year:T',
                                                                    y    =alt.Y('Gross Agricultural Product ($B):Q', stack=None),
                                                                    color=      'Region:N'))
        st.altair_chart(chart, use_container_width=True)
except  URLError as e:st.error( '''
                                **This demo requires internet access.**
                                Connection error: %s
                                '''
                                % e.reason)
PlaceHolder.scatter_chart(df, height=450, use_container_width=True)
st.divider()
