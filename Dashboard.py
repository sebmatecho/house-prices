import json
# from tkinter import N
from matplotlib import gridspec, ticker
import folium
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
# import pyautogui

from st_aggrid                import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from PIL                      import Image
from plotly                   import express as px
from folium.plugins           import MarkerCluster
from streamlit_folium         import folium_static
from matplotlib.pyplot        import figimage
from distutils.fancy_getopt   import OptionDummy


def folium_static(fig, width=1200, height=750):
# width, height=1300, 800#pyautogui.size()
    """
    Renders `folium.Figure` or `folium.Map` in a Streamlit app. This method is 
    a static Streamlit Component, meaning, no information is passed back from
    Leaflet on browser interaction.
    Parameters
    ----------
    width : int
        Width of result
    
    Height : int
        Height of result
    Note
    ----
    If `height` is set on a `folium.Map` or `folium.Figure` object, 
    that value supersedes the values set with the keyword arguments of this function. 
    Example
    -------
     m = folium.Map(location=[45.5236, -122.6750])
     folium_static(m)
    """

    # if Map, wrap in Figure
    if isinstance(fig, folium.Map):
        fig = folium.Figure().add_child(fig)
        return components.html(
            fig.render(), height=(fig.height or height) + 10, width=width
            )

    # if DualMap, get HTML representation
    elif isinstance(fig, plugins.DualMap):
        return components.html(
            fig._repr_html_(), height=height + 10, width=width
        )
# Load
@st.cache_data()#allow_output_mutation=True)

def get_file():
     url = 'https://raw.githubusercontent.com/sebmatecho/CienciaDeDatos/master/ProyectoPreciosCasas/data/kc_house_data.csv'
     data = pd.read_csv(url)
     data = data[data['bedrooms']!=33]
     return data

@st.cache_data()#allow_output_mutation=True)
def get_geofile():
     url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
     geofile = gpd.read_file(url)
     # geofile = geofile[geofile['ZIP'].isin(ZIP_list)]
     return geofile
# get geofile

def dashboard (data):
     plt.rcParams.update(plt.rcParamsDefault)
     plt.style.use('bmh')
     fig = plt.figure(figsize = (24,12), constrained_layout = True)
     gs = gridspec.GridSpec(2, 2, figure = fig)
     fig.add_subplot(gs[0,:])
     # primer gráfico
     df = data[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
     sns.lineplot(x = df['yr_built'], y = df['price'], color = 'orange')
     plt.ylabel('Price (Millions of Dollars)', fontsize = 20)
     plt.xlabel('Year of construction', fontsize = 20)
     plt.xticks(fontsize=16)
     plt.yticks(fontsize=16)
     


     # Segundo gráfico 
     fig.add_subplot(gs[1,0])
     df = data[['bedrooms','price']].groupby('bedrooms').mean().reset_index()

     sns.barplot(x = df['bedrooms'], y = df['price'], color = 'orange')
     plt.ylabel('Price (Millions of Dollars)', fontsize = 20)
     plt.xlabel('No. of bedrooms', fontsize = 20)
     plt.xticks(fontsize=16)
     plt.yticks(fontsize=16)
     # Tercer gráfico
     fig.add_subplot(gs[1,1])
     df = data[['bathrooms','price']].groupby('bathrooms').mean().reset_index()
     sns.barplot(x = df['bathrooms'], y = df['price'], color = 'orange')
     plt.ylabel('Price (Millions of Dollars)', fontsize = 20)
     plt.xlabel('No. of bathrooms', fontsize = 20)
     plt.xticks(fontsize=16, rotation=90)
     plt.yticks(fontsize=16)
     st.pyplot(fig)
     return None

def mapa1(data,geo_info,width=1100, height=750):
     data_aux = data[['id','zipcode']].groupby('zipcode').count().reset_index()
     custom_scale = data_aux['id'].quantile([0,0.2,0.4,0.6,0.8,1]).tolist()
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
     folium.Choropleth(geo_data= geo_info, 
                         data=data_aux,
                         key_on='feature.properties.ZIPCODE',
                         columns=['zipcode', 'id'],
                         threshold_scale=custom_scale,
                         fill_color='YlOrRd',
        highlight=True).add_to(mapa)
     folium_static(mapa, width=0.38*width, height=0.38*width)
     return None

def mapa2(data,geo_info,width=1100, height=750):
     data_aux = data[['price','zipcode']].groupby('zipcode').mean().reset_index()
     custom_scale = (data_aux['price'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
     folium.Choropleth(geo_data=geo_info, 
                    data=data_aux,
                    key_on='feature.properties.ZIPCODE',
                    columns=['zipcode', 'price'],
                    threshold_scale=custom_scale,
                    fill_color='YlOrRd',
                    highlight=True).add_to(mapa)
     folium_static(mapa, width=0.38*width, height=0.38*width)
     return None

def mapa3(data,geo_info,width=1000, height=750):
     data_aux = data[['price/sqft','zipcode']].groupby('zipcode').mean().reset_index()
     custom_scale = (data_aux['price/sqft'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
     folium.Choropleth(geo_data=geo_info, 
                    data=data_aux,
                    key_on='feature.properties.ZIPCODE',
                    columns=['zipcode', 'price/sqft'],
                    threshold_scale=custom_scale,
                    fill_color='YlOrRd',
                    highlight=True).add_to(mapa)
     folium_static(mapa, width=0.38*width, height=0.38*width)
     return None

def info_geo(data,width=1000, height=750):
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=9)
     markercluster = MarkerCluster().add_to(mapa)
     for nombre, fila in data.iterrows():
          folium.Marker([fila['lat'],fila['long']],
                         popup = 'Price: ${}, \n Date: {} \n {} # rooms \n {} # bathrooms \n Built in {} \n  {} square foot \n Price per square foot: {}'.format(
                         fila['price'],
                         fila['date'],
                         fila['bedrooms'],
                         fila['bathrooms'],
                         fila['yr_built'], 
                         fila['sqft_living'], 
                         fila['price/sqft'])
          ).add_to(markercluster)
     folium_static(mapa, width=width, height=0.33*width)
     return None

def descriptiva(data):
     att_num = data.select_dtypes(include = ['int64','float64'])
     media = pd.DataFrame(att_num.apply(np.mean))
     mediana = pd.DataFrame(att_num.apply(np.median))
     std = pd.DataFrame(att_num.apply(np.std))
     maximo = pd.DataFrame(att_num.apply(np.max))
     minimo = pd.DataFrame(att_num.apply(np.min))
     df_EDA = pd.concat([minimo,media,mediana,maximo,std], axis = 1)
     df_EDA.columns = ['Min','Average','Median','Max','Variability (DE)']
     df_EDA = df_EDA.drop(index =['id', 'lat', 'long','yr_built','yr_renovated'], axis = 0 )

     df_EDA['Variable'] =['Price','No. rooms', 'No. bathrooms', 'Footage (sqrt feet)', 
                         'terrain footage (sqrt feet)', 'No. floors', 'Waterfront (dummy)',
                         'View grade (1-5)', 'Condition (1-10)','Property assessment (1-13)',
                         'Footage (non basement area)', 'Footage (basement area)', 'Footage 15 closest houses', 
                         'Footage terrain 15 closest houses', 'Price per sqrt feet']
     df_EDA = df_EDA[['Variable','Min','Average','Median','Max','Variability (DE)']]  
     df_EDA = df_EDA.round(3)
     return df_EDA 

def filt_opc(data):
     tier = st.multiselect(
          'Cuartil de precios', 
          list(data['price_tier'].unique()),
          list(data['price_tier'].unique())
          )
     data = data[data['price_tier'].isin(tier)]

     OptFiltro = st.multiselect(
          'Filters',
          ['Rooms', 'Bathrooms', 'Footage (sqrt feet)','Floors','View','Property Assesment','Condition', 'ZIP Code'],
          ['Rooms', 'Bathrooms'])

     if 'ZIP Code' in OptFiltro:
          zipcod = st.multiselect(
               'Códigos postales',
               list(sorted(set(data['zipcode']))),
               list(sorted(set(data['zipcode']))))
          data = data[data['zipcode'].isin(zipcod)]

     if 'Rooms' in OptFiltro: 
          if data['bedrooms'].min() < data['bedrooms'].max():
               min_habs, max_habs = st.sidebar.select_slider(
               'How many rooms?',
               options=list(sorted(set(data['bedrooms']))),
               value=(data['bedrooms'].min(),data['bedrooms'].max()))
               data = data[(data['bedrooms']>= min_habs)&(data['bedrooms']<= max_habs)]
          else:
               st.markdown("""
                    **Rooms** is not applicable to the current selection of filters
                    """)
     if 'Bathrooms' in OptFiltro: 
          if data['bathrooms'].min() < data['bathrooms'].max():
               min_banhos, max_banhos = st.sidebar.select_slider(
               'How many bathrooms?',
               options=list(sorted(set(data['bathrooms']))),
               value=(data['bathrooms'].min(), data['bathrooms'].max()))
               data = data[(data['bathrooms']>= min_banhos)&(data['bathrooms']<= max_banhos)]
          else:
               st.markdown("""
                    **Bathrooms** is not applicable to the current selection of filters
                    """)
     if 'Footage (sqrt feet)' in OptFiltro: 
          if data['sqft_living'].min() < data['sqft_living'].max():
               area = st.sidebar.slider('Footage', int(data['sqft_living'].min()),int(data['sqft_living'].max()),2000)
               data = data[data['sqft_living']<area]
          else:  
               st.markdown("""
                    **Footage (sqrt feet)** is not applicable to the current selection of filters
                    """)

     if 'Floors' in OptFiltro: 
          if data['floors'].min() < data['floors'].max():
               min_pisos, max_pisos = st.sidebar.select_slider(
               'How many floors?',
               options=list(sorted(set(data['floors']))),
               value=(data['floors'].min(),data['floors'].max()))
               data = data[(data['floors']>= min_pisos)&(data['floors']<= max_pisos)]
          else:
               st.markdown("""
                    **Floors** is not applicable to the current selection of filters
                    """)

     if 'View' in OptFiltro: 
          if data['view'].min() < data['view'].max():
               min_vista, max_vista = st.sidebar.select_slider(
               'View',
               options=list(sorted(set(data['view']))),
               value=(data['view'].min(),data['view'].max()))
               data = data[(data['view']>= min_vista)&(data['view']<= max_vista)]
          else:
               st.markdown("""
                    **View** is not applicable to the current selection of filters
                    """)
     if 'Property Assesment' in OptFiltro:
          if data['grade'].min() < data['grade'].max():
               min_cond, max_cond = st.sidebar.select_slider(
               'Property Assesment',
               options=list(sorted(set(data['grade']))),
               value=(data['grade'].min(),data['grade'].max()))
               data = data[(data['grade']>= min_cond)&(data['grade']<= max_cond)]
          else:
               st.markdown("""
                   **Property Assesment** is not applicable to the current selection of filters
                    """)

     if 'Condition' in OptFiltro:
          if data['condition'].min() < data['condition'].max():
               min_condi, max_condi = st.sidebar.select_slider(
               'Condition',
               options=list(sorted(set(data['condition']))),
               value=(data['condition'].min(),data['condition'].max()))
               data = data[(data['condition']>= min_condi)&(data['condition']<= max_condi)]
          else:
               st.markdown("""
                **Condition** is not applicable to the current selection of filters
                    """)
     return data

st.set_page_config(page_title='App - Selling properties',
                    layout="wide", 
                    page_icon=':house',  
                    initial_sidebar_state="expanded")

### Transform

def transform(data): 
     data['date'] = pd.to_datetime(data['date'], format = '%Y-%m-%d').dt.date
     data['yr_built']= pd.to_datetime(data['yr_built'], format = '%Y').dt.year
     # data['yr_renovated'] = data['yr_renovated'].apply(lambda x: pd.to_datetime(x, format ='%Y') if x >0 else x )
     # data['id'] = data['id'].astype(str)

     #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
     data['house_age'] = 'NA'
     #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
     data.loc[data['yr_built']>1990,'house_age'] = 'new_house' 
     #llenar la columna anterior con old_house para fechas anteriores a 2015-01-01
     data.loc[data['yr_built']<1990,'house_age'] = 'old_house'

     data['zipcode'] = data['zipcode'].astype(str)


     data.loc[data['yr_built']>=1990,'house_age'] = 'new_house' 
     data.loc[data['yr_built']<1990,'house_age'] = 'old_house'

     data.loc[data['bedrooms']<=1, 'dormitory_type'] = 'studio'
     data.loc[data['bedrooms']==2, 'dormitory_type'] = 'apartment'
     data.loc[data['bedrooms']>2, 'dormitory_type'] = 'house'

     data.loc[data['condition']<=2, 'condition_type'] = 'bad'
     data.loc[data['condition'].isin([3,4]), 'condition_type'] = 'regular'
     data.loc[data['condition']== 5, 'condition_type'] = 'good'

     data['price_tier'] = data['price'].apply(lambda x: 'First Tier' if x <= 321950 else
                                                       'Second Tier' if (x > 321950) & (x <= 450000) else
                                                       'Third Tier' if (x > 450000) & (x <= 645000) else
                                                       'Fourth Tier')

     data['price/sqft'] = data['price']/data['sqft_living']
     return data

### Load

def load(data,geo_data):
     data_ref = data.shape[0]
     st.sidebar.markdown("# Parameters")

     st.title('King County Housing Dynamics')
     st.markdown(
     """
     ##### Proposed by [Sébastien Lozano-Forero](https://www.linkedin.com/in/sebastienlozanoforero/)

     In the United States, the real estate market represents between 3% and 5% of the domestic Gross Domestic Product and continuously receives important injections of capital that seek to optimize profitability. Therefore, there is an interesting window of opportunity to integrate some of the global trends in the use of historical information and technological capabilities, which assist decision-making at various points in the process flowcharts of real estate entities.
     
     This dashboard is derived from the study of a year of real estate activity (between 2014 and 2015) in King County, WA - USA, which has ~2.2 million inhabitants, the original data is available[here](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). The main idea is to facilitate the presentation and manipulation of such information with a view to a deeper understanding of the trends in this real estate market.

     The **Dashboard** tab allows the user to incorporate filters that allow these trends to be studied in a disaggregated manner ([Simpson's Paradox](https://en.wikipedia.org/wiki/Simpson%27s_paradox)). The **Recommending Prices** tab incorporates a previously trained Machine Learning model to recommend a price based on the main characteristics of the property. The repository of this project is available [here](https://github.com/sebmatecho/HousesPrices)

     ## Required Filters

     The houses have been divided into four groups of equal size, based on their price.
     - The First Tier will contain information on properties that cost less than $321,950
     - The Second Tier will contain information on properties that cost between $321,950 and $450,000
     - The Third Tier will contain information on properties that cost between $450,000 and $645,000
     - The Fourth Tier will contain information on properties that cost more than $645,000

     The zip code can be used as a proxy for locating a property in King County. See [here](https://www.zipdatamaps.com/king-wa-county-zipcodes) para más información. 

     ### Optional Filters
     In order to facilitate the exploration of the data, the user is free to select the necessary filters. Once you select the variable you want to use as a filter from the next menu, use the sliders on the left banner to manipulate the allowed values ​​of the variable. Please note that the inclusion and use of filters will also modify the figures presented in the rest of this page.
     """)
     
     data = filt_opc(data)
     geo_data = geo_data[geo_data['ZIP'].isin(list(map(int, list(set(data['zipcode'])))))]
     ## Dashboard general 
     dashboard(data)

     # Mapas
     st.header('ZIP code distribution')
     st.markdown("""
     The following figures show the distribution, via heat maps, of the number of available properties, total price and price per square foot based on zip codes. That is, once the properties are grouped by zip code and the average value within each cluster is obtained, they are classified into one of five groups using the respective quintiles. Thus, each an approximate number of postal codes in each cluster.""")
     
     col1, col2 = st.columns(2)
     with col1: 
          st.header("Available Properties")
          mapa1(data,geo_data)    
     # st.dataframe(geoData)

     with col2: 
          st.header("Overall Price")
          mapa2(data,geo_data)

     col1, col2 = st.columns(2)
     with col1: 
          st.header("Square foot costing")
          mapa3(data,geo_data)
          
     with col2: 
          st.header('Summary by ZIP code')
          df = data[['id','zipcode','price','price/sqft']].groupby('zipcode').agg({'id':'count','price':'mean','price/sqft':'mean'}).reset_index().rename(columns= {'zipcode':'Postal code','id':'Count','price':'Average price','price/sqft':'Average price/sqft'})
          # st.dataframe(df)
          AgGrid(df.round(3),fit_columns_on_grid_load=True)


     st.header("Where are these properties?")
     
     width, height= 1000, 750
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=9)
     markercluster = MarkerCluster().add_to(mapa)
     # for nombre, fila in data.iterrows():
     #      folium.Marker([fila['lat'],fila['long']],
     #                     popup = 'Price: ${}, \n Date: {} \n {} # rooms \n {} # bathrooms \n Built in {} \n  {} square foot \n Price per square foot: {}'.format(
     #                     fila['price'],
     #                     fila['date'],
     #                     fila['bedrooms'],
     #                     fila['bathrooms'],
     #                     fila['yr_built'], 
     #                     fila['sqft_living'], 
     #                     fila['price/sqft'])
     #      ).add_to(markercluster)
     folium_static(mapa, width=width, height=0.33*width)

     st.markdown(
          """
     ### Additional Information
    Finally, the numerical summary of all the variables considered in this database is presented below. Such information can be useful to find trends within clusters that are of interest. 
          
          """)

     col1, col2 = st.columns(2)
     col1.metric("No. Properties", data.shape[0],str(100*round(data.shape[0]/data_ref,4))+'% match the criteria',delta_color="off")
     col2.metric("No. Properties (Built after 1990)",data[data['house_age'] == 'new_house'].shape[0],str(100*round(data[data['house_age'] == 'new_house'].shape[0]/data_ref,4))+'% match the criteria',delta_color="off")
     AgGrid(descriptiva(data),fit_columns_on_grid_load=True)  
     return None


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ =='__main__':
     # Extract
     data = get_file() 
     geo_data = get_geofile()
     # Transform
     data2 = transform(data)
     # Load
     load(data2,geo_data)
     