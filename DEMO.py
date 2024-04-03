import pandas           as pd
import altair           as alt
import streamlit        as st
from   urllib.error import URLError
import sys
st.set_page_config(page_title='ƊⱭȾɅViƧi🧿Ƞ', page_icon='👨🏻‍💻', layout='wide', initial_sidebar_state='expanded')
# SIDE
st.sidebar.title('ƊⱭȾɅViƧi🧿Ƞ')
st.sidebar.divider()
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/GitHub-000000?logo=github&logoColor=white)](    https://github.com/kauefs/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/Python-3-blue.svg)](                            https://www.python.org/)
[![License]( https://img.shields.io/badge/License-Apache_2.0-black.svg)](                 https://www.apache.org/licenses/LICENSE-2.0/)
            ''')
st.sidebar.markdown('''Data Science **|** Computer Vision **|** ML **|** AI **|** ☁️ **|** CyberSecurity **|** 👨🏻‍💻''')
with st.sidebar.container():
    if  st.button('StreamLit Hello'):
        st.sidebar.success( 'Hello World!')
    else:
        st.sidebar.info(    'Hello There')
st.sidebar.header('Data Analysis')
PlaceHolder = st.sidebar.empty()
st.sidebar.markdown(sys.version)
with st.sidebar.container():
     cols = st.columns(3)
     with cols[0]:st.empty()
     with cols[1]:st.markdown('''©2024™''')
     with cols[2]:st.empty()
# MAIN
st.markdown('''![ƊⱭȾɅViƧi🧿Ƞ](https://raw.githubusercontent.com/kauefs/StreamLit/%40/img/DataVision3.png)''')
st.divider()
with st.container():
     cols = st.columns(3)
     with cols[0]:st.empty()
     with cols[1]:st.write('1 April 2024')
     with cols[2]:st.empty()
st.header(      'DataFrame&ChartDEMO')
@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL =    'https://streamlit-demo-data.s3-us-west-2.amazonaws.com'
    df             =   pd.read_csv(AWS_BUCKET_URL + '/agri.csv.gz')
    return df.set_index('Region')
try:
    df = get_UN_data()
    countries       =  st.multiselect('🌎🌍🌏:', list(df.index), ['Australia', 'Brazil', 'France', 'Germany', 'China', 'United States of America'])
    if not countries:  st.error(      'Please select at least one country.')
    else:
        data        =  df.loc[countries]
        data       /= 1000000.0
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
