# https://github.com/PacktPublishing/Streamlit-for-Data-Science/blob/main/trees_app/all_code.py
import   datetime            as   dt
import      numpy            as   np
import     pandas            as   pd
import  streamlit            as   st
import    seaborn            as   sns
import     altair            as   alt
import matplotlib.pyplot     as   plt
import     pydeck            as   pdk
import     plotly.express    as   px
# from        bokeh.plotting import figure
# Settings:
pd.options.plotting.matplotlib.register_converters = True
plt.rcParams[  'figure.autolayout']    =             True
plt.rcParams[    'font.family'    ]    =                                         'sans-serif'
sns.set_theme(context='notebook', style='whitegrid', palette='colorblind',  font='sans-serif', font_scale=1.15, color_codes=True, rc={'grid.color':'1','grid.linestyle':':'})
FontT={'family':'sans-serif'    ,'color':'#000000', 'size'  : 13,   'fontweight':'semibold'  }
FontY={'family':'sans-serif'    ,'color':'#FF4500', 'size'  : 10,   'fontweight':'regular'   }
FontX={'family':'sans-serif'    ,'color':'#4CAF50', 'size'  : 10,   'fontweight':'regular'   }
# Page:
st.set_page_config(page_title='ƊⱭȾɅ Ʌnalysis', page_icon='📊', layout='wide', initial_sidebar_state='collapsed')
if 'points' not in st.session_state:st.session_state.points=[]
# SIDE
st.sidebar.title   ('ƊⱭȾɅViƧi🧿Ƞ&trade;')
st.sidebar.divider ( )
st.sidebar.info    ('ƊⱭȾɅ'              )
st.sidebar.success ('Ʌnalysis'          )
st.sidebar.divider ( )
st.sidebar.warning ('Source: SFDPW')
st.sidebar.divider ( )
st.sidebar.markdown('''
![2025.08.15  ](https://img.shields.io/badge/2025.08.15-000000)

[![GitHub     ](https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](https://github.com/kauefs/)
[![Medium     ](https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](https://medium.com/@kauefs)
[![LinkedIn   ](https://img.shields.io/badge/in-0077B5?logo=linkedin&logoColor=FFFFFF)](https://www.linkedin.com/in/kauefs/)
[![Python     ](https://img.shields.io/badge/3-646464?logo=python&logoColor=FFDE57&labelColor=4584B6)](https://www.python.org/)

[![License    ](https://img.shields.io/badge/Apache--2.0-D22128?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)

[![ƊⱭȾɅViƧi🧿Ƞ](https://img.shields.io/badge/ƊⱭȾɅViƧi🧿Ƞ&trade;-0065FF?style=plastic&label=&copy;2025&labelColor=0065FF)](https://datavision.one/)
                    ''')
# MAIN:
st.title('San Francisco Trees')
st.divider( )
@st.cache_data
def loadTreesData  ( ):
    return pd.read_csv('https://github.com/PacktPublishing/Streamlit-for-Data-Science/raw/refs/heads/main/trees_app/trees.csv')
trees=loadTreesData( )
# PyDeck:
st.subheader('PyDeck')
trees.dropna(how='any', inplace=True)
initial_view_state=pdk.ViewState(latitude=37.77,  longitude=-122.4, zoom=11, pitch=30)
layers            =pdk.Layer('HexagonLayer', data=trees, get_position=['longitude','latitude'], radius=100, extruded=True)
st.pydeck_chart   (pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=initial_view_state, layers=[layers]))
st.divider( )
# Map:
st.subheader('Map')
m=trees.dropna(subset=['longitude','latitude'])
m=m.sample(n=1000)
st.map(m)
st.divider( )
# MatPlotLib:
st.subheader('MatPlobLib')
trees['age']=(pd.to_datetime('today')-pd.to_datetime(trees['date'])).dt.days
figMPL,axMPL=plt.subplots(tight_layout=True)
axMPL       =plt.hist(trees['age'], color='#6595EE')
plt.xlabel('Age (Days)', fontdict=FontX)
plt.box   (False)
st .pyplot(figMPL)
plt.close (figMPL)
st .divider( )
# SeaBorn:
st.subheader('SeaBorn')
figSB,axSB=plt.subplots(tight_layout=True)
axSB      =sns.histplot(trees['age'], color='#6595EE')
plt.ylabel(      None)
plt.xlabel('Age (Days)', fontdict=FontX)
sns.despine(top= True , left=True, bottom=True, right=True)
st .pyplot(figSB)
plt.close (figSB)
st .divider( )
# BoKeh:
# st.subheader('BoKeh')
# scatterplot=figure (title='Bokeh ScatterPlot')
# scatterplot.scatter(trees['dbh'], trees['site_order'], color='#6595EE')
# scatterplot.yaxis.axis_label='Site Order'
# scatterplot.xaxis.axis_label='DBH'
# st.bokeh_chart(scatterplot)
# st.divider( )
# Plotly:
st.subheader('Plotly')
fig=px.histogram(trees['dbh'])
fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title=None)
fig.update_traces(name='Tree Diameter @ Breast Height (DBH)')
st.plotly_chart(fig)
st.divider( )
# Charts I:
st.subheader('Grouped Charts I')
grouped=pd.DataFrame(trees.groupby(['dbh']).count( )['tree_id'])
grouped.columns=['tree_count']
st.write('Line Chart')
st.line_chart(grouped)
st.write('Bar Chart')
st .bar_chart(grouped)
st.write('Area Chart')
st.area_chart(grouped)
st.divider( )
# Charts II:
st.subheader('Grouped Charts II')
grouped['new_col']=np.random.randn(len(grouped))*500
st.write('Line Chart')
st.line_chart(grouped)
st.write('Bar Chart')
st .bar_chart(grouped)
st.write('Area Chart')
st.area_chart(grouped)
st.divider( )
# AltAir:
st.subheader('AltAir')
col1,col2=st.columns(2)
with col1:
    caretaker =trees  .groupby(['caretaker']).count( )['tree_id'].reset_index( )
    caretaker .columns=['caretaker',    'tree_count']
    fig1=alt  .Chart (caretaker).mark_bar( ).encode(x=alt.X('caretaker' , title='Tree Caretaker'),
                                                    y=alt.Y('tree_count', title='Number of Trees'))
    st  .altair_chart(fig1, use_container_width=True)
with col2:
    fig2=alt   .Chart(    trees).mark_bar( ).encode(x=alt.X('caretaker' , title='Tree Caretaker'),
                                                    y=alt.Y('count(*):Q', title='Count of Records'))
    st  .altair_chart(fig2, use_container_width=True)
st      .divider( )
# https://github.com/PacktPublishing/Streamlit-for-Data-Science/blob/main/penguin_app/penguins.py
st          .title    ("Palmer's Penguins")
st          .markdown ('ScatterPlot about Penguins!')
y      =  st.selectbox('y',['bill_depth_mm' ,'bill_length_mm','flipper_length_mm','body_mass_g'])
x      =  st.selectbox('x',['bill_length_mm','bill_depth_mm' ,'flipper_length_mm','body_mass_g'])
# penguin=  st.file_uploader('Select Local Penguins CSV')
# if penguin is not None:df=pd.read_csv(penguin)
# else:     st.stop( )
@st.cache_data
def loadPenguinsData( ):
    return pd.read_csv('https://github.com/PacktPublishing/Streamlit-for-Data-Science/raw/refs/heads/main/penguin_app/penguins.csv')
df=loadPenguinsData ( )
chart   =(alt.Chart (df, title="Palmer's Penguins")
             .mark_circle( )
             .encode(x=x, y=y, color='species')
             .interactive( ))
st.altair_chart(chart, use_container_width=True)
st.divider( )
