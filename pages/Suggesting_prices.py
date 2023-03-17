from re import template
from PIL import Image
import streamlit as st
import pandas as pd
import joblib
import numpy as np
# import boto3
import tempfile



st.set_page_config(page_title='App - Suggesting prices',
                    layout="wide", 
                    page_icon='🚀',  
                    initial_sidebar_state="expanded")

st.title("Suggesting propertie prices")
st.sidebar.markdown("Description of the property")

@st.cache(allow_output_mutation=True)
def get_data():
     url = 'https://raw.githubusercontent.com/sebmatecho/CienciaDeDatos/master/ProyectoPreciosCasas/data/kc_house_data.csv'
     return pd.read_csv(url)

def transform(data):
     X = pd.DataFrame()
     banhos = st.sidebar.select_slider(
               'How many bathrooms?',
               options=list(sorted(set(data['bathrooms']))), value = 1.5)

     X.loc[0,'bathrooms'] = banhos
     scaler = joblib.load('./parameters/bathrooms.sav')
     X[['bathrooms']] = scaler.transform(X[['bathrooms']])

     # pisos = st.sidebar.select_slider(
     #           'Número de Pisos',
     #           options=list(sorted(set(data['floors']))))

     # X.loc[0,'floors'] = pisos
     # scaler = joblib.load('../parameters/floors.sav')
     # X[['floors']] = scaler.transform(X[['floors']])


     habitaciones = st.sidebar.select_slider(
               'How many rooms?',
               options=list(sorted(set(data['bedrooms']))), value = 2)

     # st.sidebar.number_input('Número de habitaciones', min_value=1, max_value=10, value=3, step=1)

     X.loc[0,'bedrooms'] = habitaciones
     scaler = joblib.load('./parameters/bedrooms.sav')

     X[['bedrooms']] = scaler.transform(X[['bedrooms']])

     area = st.sidebar.select_slider(
               'Square footage',
               options=list(sorted(set(data['sqft_living']))), value = 1000)

     # st.sidebar.number_input('', value = 1000)

     X.loc[0,'sqft_living'] = area
     scaler = joblib.load('./parameters/sqft_living.sav')
     X[['sqft_living']] = scaler.transform(X[['sqft_living']])




     vista = st.sidebar.select_slider(
               'View mark',
               options=list(sorted(set(data['view']))), value = 0)

     # st.sidebar.select_slider(
     #      'Puntaje de la vista',
     #      (0,1,2,3,4))

     X.loc[0,'view'] = vista
     scaler = joblib.load('./parameters/view.sav')
     X[['view']] = scaler.transform(X[['view']])



     condicion = st.sidebar.select_slider(
          'General condition',
               options=list(sorted(set(data['condition']))), value = 3)

     # st.sidebar.selectbox(
          
     #      (0,1,2,3,4))

     X.loc[0,'condition'] = condicion
     scaler = joblib.load('./parameters/condition.sav')
     X[['condition']] = scaler.transform(X[['condition']])


     puntaje = st.sidebar.select_slider(
          'Construction mark',
               options=list(sorted(set(data['grade']))), value = 8)


     X.loc[0,'grade'] = puntaje
     scaler = joblib.load('./parameters/grade.sav')
     X[['grade']] = scaler.transform(X[['grade']])

     edad = st.sidebar.select_slider(
          'Age of property', 
          options=list(range(1,80)), value = 10)
     
     X.loc[0,'property_age'] = edad
     scaler = joblib.load('./parameters/property_age.sav')
     X[['property_age']] = scaler.transform(X[['property_age']])

     waterfront = st.sidebar.selectbox(
          'Waterfront?',
          ('Yes', 'No'))

     if waterfront == 'Yes': 
          waterfront = 1
     else:  
          waterfront = 0

     X.loc[0,'waterfront'] = waterfront
     scaler = joblib.load('./parameters/waterfront.sav')
     X[['waterfront']] = scaler.transform(X[['waterfront']])

     renovacion = st.sidebar.selectbox(
          'Has the property being renovated?',
          ('Yes', 'No'))

     if renovacion == 'Yes': 
          renovacion = 1
     else:  
          renovacion = 0

     X.loc[0,'yr_renovated_dummy'] = renovacion
     scaler = joblib.load('./parameters/yr_renovated_dummy.sav')
     X[['yr_renovated_dummy']] = scaler.transform(X[['yr_renovated_dummy']])
     df_coord = data[['zipcode','lat','long']].groupby('zipcode').agg({'lat':'mean','long':'mean'}).reset_index()
     
     cod = st.sidebar.selectbox(
          'ZIP code',
          list(set(df_coord['zipcode'])))


     X.loc[0,'lat'] = float(df_coord.loc[df_coord['zipcode']==cod,'lat'])
     X.loc[0,'long'] = float(df_coord.loc[df_coord['zipcode']==cod,'long'])
     variables = ['bedrooms', 'bathrooms', 'sqft_living', 'waterfront', 'view', 'condition', 'grade', 'yr_renovated_dummy', 'property_age','lat','long']
     return X 




def load(X):
     st.markdown("""
Here, a Machine Learning model will suggest a price for a given property based on its specifics. The user must provide the characteristics of the property using the menu on the left bar. The required information is defined below:
          
- Number of bathrooms: Number of bathrooms of the property of interest. Values ​​such as 1.5 bathrooms refer to the existence of a bathroom with a shower and a bathroom without a shower.
- Number of floors: Number of floors of the property of interest
- Number of rooms: Number of rooms of the property of interest
- Area of ​​the property: Footage in square feet of the property of interest
- Waterfront: Does the property of interest have a water view?
- View score: View score of the property of interest
- Condition of the property: General condition of the property of interest
- Score on the construction: Score on the construction of the property of interest
- Renovation: Has the property of interest been renovated?
- Age of the property: The 'age' of the property of interest
- Postal Code in which property of interest is based
     """)


     if st.button('Suggest price'):

          # with tempfile.TemporaryFile() as fp: 
          #      client.download_fileobj(Fileobj = fp, 
          #                               Bucket = 'precioscasas',
          #                               Key = 'xbg_final.sav'
          #      )
          #      fp.seek(0)
          modelo_final = joblib.load('./parameters/xbg_final.sav')
          precio = modelo_final.predict(X)[0]
          # st.balloons()
          st.success('A suggested value is now available!')
     #     st.write('El precio sugerido es:', )
          st.metric("Suggested price", '$'+str(f'{round(np.expm1(precio)):,}')+ ' usd')
     else:
          # st.snow()
          st.error('Please enter the specifics of the property of interest.')
     
     return None
     

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__=='__main__':
     #Extract
     data = get_data()
     #Transform
     data2 = transform(data)
     #Load
     load(data2)