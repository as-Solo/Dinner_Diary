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
from time import sleep

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



menu = ['HOME', 'AÑADIR RESTAURANTE', 'RECOMENDACIONES', 'NUEVO RESTAURANTE', 'REGISTRARSE']

choice = st.sidebar.selectbox('MENU', menu)


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


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
        #----------------------------------------------------EJECUCIÓN HOME---------------------------------------------------

        st.write('Hasta que seamos capaces de acceder a tus datos de geolocalización, por favor, indicanos dónde te encuentras o dónde quieres realizar la búsqueda')
        
        menu01_01, menu01_02, menu01_03 = st.beta_columns([1,1,1])
        with menu01_01:
            zona_home = st.text_input('Introduce la zona en la que quieres buscar')

        with menu01_02:
            ciudad_home = st.text_input('Introduce la ciudad')
        
        if menu01_01.checkbox('Coordenadas'):
            try:
                busqueda_coord = zona_home + ', ' + ciudad_home
                coordenadas_fol_home = td.geocode_fol(busqueda_coord)

            except:
                st.warning('Estamos teniendo problemas para localizarte')
                st.write(coordenadas_fol_home)
            
            if coordenadas_fol_home != None:
                    
                    
                    map_1 = folium.Map(location= coordenadas_fol_home, zoom_start= 15)
                    
                    ubicacion = Marker(location = coordenadas_fol_home, tooltip="Usted está aquí. O no")
                    ubicacion.add_to(map_1)

                    visitados = td.lista_visitados(id_usuario)

                    st.write(visitados)
                    folium_static(map_1)
                    
                        
        
        
        #with menu01_03:
            #st.write(busqueda_coord)
            #st.write(coordenadas)

        
        #--------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------
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
        
        menu02_01, menu02_02, menu02_03 = st.beta_columns([1,1,1])
        with menu02_01:
            zona_visitados = st.text_input('Introduce la zona en la que quieres buscar')

        with menu02_02:
            ciudad_visitados = st.text_input('Introduce la ciudad')

        with menu02_03:
            nombre_visitados = st.text_input('Introduce el nombre del restaurante')

        menu02_04, menu02_05, = st.beta_columns([2, 1])

        comentario = menu02_04.text_input('Deja tus comentarios')

        valoracion = menu02_05.selectbox('Puntuación',[1, 2, 3, 4, 5])

        {zona_visitados}, {ciudad_visitados}, {nombre_visitados}, {comentario}, {valoracion}, 
        if zona_visitados != '' and ciudad_visitados != '':
        
                busqueda_coord = zona_visitados + ', ' + ciudad_visitados
                                
                coordenadas_fol_visitados = td.geocode_fol(busqueda_coord)
                coordenadas_visitados = str(coordenadas_fol_visitados[0]) + ', ' + str(coordenadas_fol_visitados[1])
                {busqueda_coord}, {coordenadas_visitados}
                sleep(1)

                if coordenadas_visitados == None:
                    menu01_04.warning('No localizamos la zona. Normalmente se soluciona volviendo a introducir algún dato')

                else:
                    try:
                        df = td.buscar_visitado(nombre_visitados, zona_visitados, ciudad_visitados)
                        id_restaurante = td.buscar_en('id_rest', nombre_visitados, 'restaurantes', 'nombre')
                        st.write([df, id_restaurante])
                    except:
                        st.warning('Por favor, actualiza algún dato de tu busqueda')

                    if id_restaurante != None:
                        st.success('BIEEEEN!')
                        if menu01_05.button('Crear comentario'):
                            try:
                                td.add_visitado(id_usuario, id_restaurante, valoracion, comentario)
                            except:
                                td.warning('Ha ocurrido un error, recuerda que los comentarios no pueden ser idénticos')
                        

                    else:
                        st.warning('No estamos encontrando el restaurante que buscas. Prueba a modificar el nombre o la localización o introducelo en el menú NUEVO RESTAURANTE') 
    #                    

                        

            

                        

                        #td.add_visitado(id_usuario, id_restaurante, valoracion, comentario)

        #--------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


elif choice == 'RECOMENDACIONES':
    try:
        hueco_01.header(f"RECOMENDACIONES  {id_usuario}")
    except:
        hueco_01.subheader('RECOMENDACIONES')
        id_usuario = None

    if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
    else:
        #----------------------------------------------EJECUCIÓN RECOMENDACIONES---------------------------------------------------

        st.write('Hasta que seamos capaces de acceder a tus datos de geolocalización, por favor, indicanos dónde te encuentras o dónde quieres realizar la búsqueda')
        
        menu03_01, menu03_02, menu03_03 = st.beta_columns([1,1,1])
        with menu03_01:
            zona = st.text_input('Introduce la zona en la que quieres buscar')

        with menu03_02:
            ciudad = st.text_input('Introduce la ciudad')
        
        with menu03_03:
            busqueda = st.text_input('¿QUÉ TE APETECE HOY?')
        
        if menu03_01.checkbox('Coordenadas'):
            try:
                busqueda_coord = zona + ', ' + ciudad
                coordenadas_fol = td.geocode_fol(busqueda_coord)
                origen = td.geocode(busqueda_coord)
            except:
                st.warning('Estamos teniendo problemas para localizarte')
            
            if coordenadas_fol != None and origen != None:
                
                
                menu03_02.write(str(coordenadas_fol) + ' ' + origen + ' ' + busqueda)
                
                if busqueda != '':
                    if menu03_03.button('BUSCAR'):
                        lista_recomendacion = td.peticion_4s(origen, busqueda)
                        mostrar = pd.DataFrame(lista_recomendacion).sort_values('distancia')
                        st.write('')

                        menu03_04, menu03_05, menu03_06 = st.beta_columns([1,4,1])
                        map_1 = td.mapa_sugerencias(lista_recomendacion, coordenadas_fol)

                        with menu03_05:
                            folium_static(map_1)
                        st.write(mostrar[['nombre', 'direccion', 'etiqueta', 'distancia']], layout="wide")
            else:
                st.warning('No encontramos el sitio donde quieres buscar')

        
        
            
        #--------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


elif choice == 'NUEVO RESTAURANTE':
    try:
        hueco_01.header(f'NUEVO RESTAURANTE {id_usuario}')
        if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
        else:
            pass
    except:
        pass


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
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
    

