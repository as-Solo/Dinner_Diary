# Realizado por Solo a 15/05/2021, última actualización 16/05/2021, WIP


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


import codecs
import folium
import json
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import sys


from datetime import date
from datetime import datetime
from dotenv import load_dotenv
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
from PIL import Image
from src import busquedas as td
from streamlit_folium import folium_static

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


st.set_page_config(layout="wide")

cabecera = Image.open('img/Cabecera_ejemplo.jpg')

st.image(cabecera)

hueco_01, mail_log, pass_log = st.beta_columns([1.8,1.2,1.3])

with mail_log:

    usuario = st.text_input("Introduce tu mail", 'ejemplo@jungle.com')
    nombre_usuario = td.buscar_en('nombre', usuario, 'usuarios', 'mail')

with pass_log:

    password = st.text_input("Introduce tu contraseña",  type = 'password')
    confirmar = td.confirmar_pass(usuario, password)


if mail_log.checkbox('Login'):
    if confirmar == 'Ok':
        id_usuario = td.buscar_en('id_usuario', usuario, 'usuarios', 'mail')
        pass_log.success(f'Bienvenido {nombre_usuario}')
        
    else:
        pass_log.warning('Error en el registro')
        id_usuario = None



menu = ['HOME', 'AÑADIR RESTAURANTE', 'RECOMENDACIONES', 'ITINERARIO', 'REGISTRARSE']

choice = st.sidebar.selectbox('MENU', menu)

if choice == 'HOME':
    try:
        hueco_01.header(f'MIS SITIOS {id_usuario}')  
        
    except:
        hueco_01.header('MIS SITIOS')
        hueco_01.warning('No te encuentras registrado')
        id_usuario = None

    if id_usuario == None:
            pass
    else:
        #----------------------------------------------EJECUCIÓN LISTA VISITADOS---------------------------------------------------

        st.write('Hasta que seamos capaces de acceder a tus datos de geolocalización, por favor, indicanos dónde te encuentras o dónde quieres realizar la búsqueda')
        
        menu01_01, menu01_02, menu01_03 = st.beta_columns([1,1,1])
        with menu01_01:
            zona = st.text_input('Introduce la zona en la que quieres buscar', 'centro')

        with menu01_02:
            ciudad = st.text_input('Introduce la ciudad', 'Madrid')
        
        busqueda_coord = zona + ', ' + ciudad
        
        coordenadas = td.geocode_fol(busqueda_coord)
        
        #with menu01_03:
            #st.write(busqueda_coord)
            #st.write(coordenadas)

        menu01_04, menu01_05 = st.beta_columns([2,1])
        map_1 = folium.Map(location= [coordenadas[0],coordenadas[1]], zoom_start= 15)
        
        ubicacion = Marker(location = [coordenadas[0],coordenadas[1]], tooltip="Usted está aquí. O no")
        ubicacion.add_to(map_1)

        with menu01_04:
            folium_static(map_1)
        with menu01_05:
            st.write('BLA BLA BLA BLA BLABLA  BLABLA')
        #--------------------------------------------------------------------------------------------------------------------------

if choice == 'AÑADIR RESTAURANTE':
    try:
        hueco_01.header(f'AÑADIR RESTAURANTE {id_usuario}')  
        
    except:
        hueco_01.header('AÑADIR RESTAURANTE')
        hueco_01.warning('No te encuentras registrado')
        id_usuario = None

    if id_usuario == None:
            pass
    else:
        #----------------------------------------- EJECUCIÓN AÑADIR A VISITADOS ---------------------------------------------------
        
        st.write('¿En qué zona se encuentra el restaurante que quieres añadir?, y ¿cómo se llama?')
        
        menu01_01, menu01_02, menu01_03 = st.beta_columns([1,1,1])
        with menu01_01:
            zona = st.text_input('Introduce la zona en la que quieres buscar', 'Marqués de Vadillo')

        with menu01_02:
            ciudad = st.text_input('Introduce la ciudad', 'Madrid')
        
        busqueda_coord = zona + ', ' + ciudad
        
        coordenadas = td.geocode(busqueda_coord)
        coordenadas_fol = td.geocode_fol(busqueda_coord)
        
        with menu01_03:
            nombre_res = st.text_input('Introduce el nombre del restaurante', 'Casa Enriqueta')

        menu01_04, menu01_05, = st.beta_columns([2, 1])

        comentario = menu01_04.text_input('Deja tus comentarios')

        valoracion = menu01_05.selectbox('Puntuación',[1, 2, 3, 4, 5])
                
        df = td.buscar_visitado(nombre_res, zona, ciudad)


        #try:
        id_restaurante = td.buscar_en('id_rest', nombre_res, 'restaurantes', 'nombre')
        #    st.write (id_restaurante)
        #except:
        #    menu01_05.warning('Revisa que los datos están bien')
        

        if menu01_05.button('Crear comentario'):
            pass

                
        st.write(df.shape)

        st.write(df)

                    

                    #td.add_visitado(id_usuario, id_restaurante, valoracion, comentario)

        #--------------------------------------------------------------------------------------------------------------------------

elif choice == 'RECOMENDACIONES':
    try:
        hueco_01.header(f"RECOMENDACIONES  {id_usuario}")
    except:
        hueco_01.subheader('RECOMENDACIONES')
        hueco_01.warning('No te encuentras registrado')

    if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
    else:
        #----------------------------------------------EJECUCIÓN RECOMENDACIONES---------------------------------------------------

        st.write('Hasta que seamos capaces de acceder a tus datos de geolocalización, por favor, indicanos dónde te encuentras o dónde quieres realizar la búsqueda')
        
        menu03_01, menu03_02, menu03_03 = st.beta_columns([1,1,1])
        with menu03_01:
            zona = st.text_input('Introduce la zona en la que quieres buscar', 'centro')

        with menu03_02:
            ciudad = st.text_input('Introduce la ciudad', 'Madrid')
        
        busqueda_coord = zona + ', ' + ciudad
        
        coordenadas_fol = td.geocode_fol(busqueda_coord)
        origen = td.geocode(busqueda_coord)
        
        with menu03_03:
            busqueda = st.text_input('¿QUÉ TE APETECE HOY?', 'Hamburguesas')
            #st.write(coordenadas_fol)
            #st.write(busqueda)

        if menu03_03.button('BUSCAR'):
            lista_recomendacion = td.peticion_4s(origen, busqueda)
            mostrar = pd.DataFrame(lista_recomendacion).sort_values('distancia')
            st.write('')

            menu03_04, menu03_05, menu03_06 = st.beta_columns([1,4,1])
            map_1 = td.mapa_sugerencias(lista_recomendacion, coordenadas_fol)

            with menu03_05:
                folium_static(map_1)
            #with menu03_05:
            st.write(mostrar[['nombre', 'direccion', 'etiqueta', 'distancia']], layout="wide")
        #--------------------------------------------------------------------------------------------------------------------------

elif choice == 'ITINERARIO':
    try:
        hueco_01.header(f'ITINERARIO {id_usuario}')
        if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
        else:
            pass
    except:
        pass

elif choice == 'REGISTRARSE':
    hueco_01.header('REGISTRARSE ')
    colum1, colum2 = st.beta_columns([1,2])

    nombre = colum1.text_input("Introduce tu nombre", "Nombre*")
    if nombre == "Nombre*" or nombre == '':
        nombre = None

    apellidos = colum2.text_input("Introduce tus apellidos", "Apellidos*")
    if apellidos == "Apellidos*" or apellidos == '':
        apellidos = None

    mail = colum1.text_input("Introduce tu mail", "ejemplo@jungle.com*")
    if mail == "ejemplo@jungle.com*" or mail == '':
        mail = None

    direccion = colum2.text_input("Introduce tu dirección",  'Dirección')
    if direccion == "Dirección" or direccion == '':
        direccion = None

    colum3, colum4, colum5 = st.beta_columns([1,1,1])

    telefono = colum3.text_input("Introduce tu teléfono", 'Teléfono')
    if telefono == "Teléfono" or telefono == '':
        telefono = None

    password_n = colum5.text_input("Introduce una contraseña",  type = 'password')
    if password_n == "":
        password_n = None

    if nombre != None and apellidos != None and mail != None and password_n != None:
        if colum5.button('Registro'):
            mensaje_r = td.add_usuario(nombre, apellidos, direccion, mail, telefono, password_n)
            colum3.success(mensaje_r)
    else:
        colum3.warning('Hay campos obligatorios (*)')
    

