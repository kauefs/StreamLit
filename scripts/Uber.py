# https://sigmoidal.ai/
import  numpy    as np
import  pandas   as pd
import streamlit as st
st.set_page_config(page_title='UBER', page_icon='🚕', layout='wide', initial_sidebar_state='expanded')
# DATA:
DATE =   'date/time'
DATA =  ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')
@st.cache_data
def LoadData(nrows):
    data                       = pd.read_csv(DATA, nrows=nrows)
    lowercase                  = lambda x: str(x).lower(      )
    data.rename(lowercase, axis='columns',inplace=True        )
    data[DATE]               = pd.to_datetime(data[DATE]      )
    return data
data=LoadData(1000)
# SIDE:
st.sidebar.title    ('ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.divider  (           )
st.sidebar.subheader('DashBoard')
hour       = st.sidebar.slider('Hour:', 0, 23, 9)
# Filtered Hour  PlaceHolder:
info       = st.sidebar.empty ()
# CheckBox       PlaceHolder:
table      = st.sidebar.empty ()
# Filtered Rides PlaceHolder:
success    = st.sidebar.empty ()
st.sidebar.divider(            )
st.sidebar.markdown('''
![2024.05.01   ](https://img.shields.io/badge/2024.05.01-000000)

[![GitHub      ](https://img.shields.io/badge/GitHub-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium      ](https://img.shields.io/badge/Medium-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn    ](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python      ](https://img.shields.io/badge/Python3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![License     ](https://img.shields.io/badge/Apache--2.0-D22128?&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&logoColor=0065FF&label=&copy;2024&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
'---'#st.divider()
st.title('Uber PickUps in NYC')
'---'#st.divider()
FilteredData= data[data[DATE].dt.hour == hour]
info.info(f'''Loading {FilteredData.shape[0]} PickUps…''')
st.subheader('PickUps @ %sh: %s' %  (hour, FilteredData.shape[0]))
st.map(FilteredData)
'---'#st.divider(        )
st.subheader('PickUps by Hour:')
hist  = np.histogram(data[DATE].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist)
'---'#st.divider(      )
if table.checkbox( 'DataFrame', value=False):
    st.subheader(  'DATA'                  )
    success.success(f'''Loading {data.shape[0]} entries…''')
    st.write(data)
    '---'#st.divider(  )
