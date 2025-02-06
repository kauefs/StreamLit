import altair         as   alt
import pandas         as   pd
import streamlit      as   st
from   urllib.error import URLError
import                     sys
st.set_page_config(page_title='ƊⱭȾɅViƧi🧿Ƞ', page_icon='👨🏻‍💻', layout='wide', initial_sidebar_state='expanded')
# DATA:
@st.cache_data
def get_UN_data():
    DATA  =  'https://streamlit-demo-data.s3-us-west-2.amazonaws.com'
    df    =pd.read_csv (DATA + '/agri.csv.gz')
    return df.set_index('Region')
# SIDE:
st.sidebar.title   ('ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.markdown('''👨🏻‍💻 **|** DS **|** CV **|** ML **|** AI **|** ☁️ **|** CS **|** ''')
'---'#st.sidebar.divider(                )
with    st.sidebar.container(      ):
    if  st.button('StreamLit Hello'):
        st.sidebar.success ('Hello World!')
    else:
        st.sidebar.info    ('Hello There' )
'---'#st.sidebar.divider(                       )
st.sidebar.header  ('Data Analysis')
PlaceHolder = st.sidebar.empty(    )
st.sidebar.write   ('System Ready: Python –', sys.version)
st.sidebar.markdown('''
![2024.04.01   ](https://img.shields.io/badge/2024.04.01-000000)

[![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![GitHub      ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium      ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn    ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python      ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2024&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.markdown('''![ƊⱭȾɅViƧi&#x1F9FF;Ƞ](https://raw.githubusercontent.com/kauefs/StreamLit/%40/img/DataVision3.png)''')
'---'#st.divider()
st.title   ('StreamLitDEMO'  )
st.header  ('DataFrame&Chart')
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
'---'#st.divider()
