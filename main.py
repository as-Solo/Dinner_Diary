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



menu = ['HOME', 'AÑADIR COMENTARIO', 'RECOMENDACIONES', 'NUEVO RESTAURANTE', 'BORRAR COMENTARIO', 'REGISTRARSE']

choice = st.sidebar.selectbox('MENU', menu)


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


if choice == 'HOME':
    try:
        print(id_usuario)
        hueco_01.header(f'MIS SITIOS')  
        
    except:
        hueco_01.header('MIS SITIOS')
        hueco_01.warning('No te encuentras registrado')
        id_usuario = None

    if id_usuario == None:
            pass
    else:
        #--------------------------------------------------------EJECUCIÓN HOME---------------------------------------------------

        st.write('Hasta que seamos capaces de acceder a tus datos de geolocalización, por favor, indicanos dónde te encuentras o dónde quieres realizar la búsqueda')
        
        menu01_01, menu01_02, menu01_03 = st.beta_columns([1,2,1])
        with menu01_01:
            zona_home = st.text_input('Introduce: zona, ciudad, país', key = 'kz_home',)
        

        with menu01_02:
            st.write('')
            st.write('')
            st.write('En muchos casos el País no será necesario. Pero si ves que el resultado no es el esperado prueba a ponerlo')
            #ciudad_home = st.text_input('Introduce la ciudad', key = 'kc_home')
        
        if menu01_01.checkbox('Coordenadas'):
            try:
                #busqueda_coord = zona_home + ', ' + ciudad_home
                coordenadas_fol_home = td.geocode_fol(zona_home)
    #            st.write(coordenadas_fol_home)

            except:
                st.warning('Estamos teniendo problemas para localizarte')
                coordenadas_fol_home = None
    #            st.write(coordenadas_fol_home)
            
            if coordenadas_fol_home != None:
                    
                    
                    map_1 = td.mapa_visitados(id_usuario, coordenadas_fol_home)
                    
                    #ubicacion = Marker(location = coordenadas_fol_home, tooltip="Usted está aquí. O no")
                    #ubicacion.add_to(map_1)

                    visitados = td.lista_visitados(id_usuario)

                    st.write(visitados)
                    folium_static(map_1, width = 1106)
            else:
                st.warning('No te encontramos. Prueba en inglés que eso siempre funciona.')
                    
                        
        
        
        #with menu01_03:
            #st.write(busqueda_coord)
            #st.write(coordenadas)

        
        #--------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


if choice == 'AÑADIR COMENTARIO':
    try:
        print(id_usuario)
        hueco_01.header(f'AÑADIR COMENTARIO')  
        
    except:
        hueco_01.header('AÑADIR RESTAURANTE')
        hueco_01.warning('No te encuentras registrado')
        id_usuario = None

    if id_usuario == None:
            pass
    else:
        #----------------------------------------- EJECUCIÓN AÑADIR COMENTARIO ---------------------------------------------------
        
        st.write('¿En qué zona se encuentra el restaurante que quieres añadir?, y ¿cómo se llama?')
        
        menu02_01, menu02_02, menu02_03 = st.beta_columns([1,1,1])
        with menu02_01:
            zona_visitados = st.text_input('Introduce zona, ciudad, país', key = 'kz_visitados')
        
        with menu02_02:
            st.write('')
            st.write('')
            if st.checkbox('coordenadas'):
                try:
                    coordenadas_fol_visitados = td.geocode_fol(zona_visitados)
                    coordenadas_visitados = str(coordenadas_fol_visitados[0]) + ', ' + str(coordenadas_fol_visitados[1])
                except:
                    st.warning('Hay que darle al botón')
                    coordenadas_visitados = None
            else:
                coordenadas_fol_visitados = ''
                coordenadas_visitados = ''

        with menu02_03:
            nombre_visitados = st.text_input('Introduce el nombre del restaurante', key = 'kn_visitados')

        menu02_04, menu02_05, menu02_05b = st.beta_columns([1.5, 3, 1])

        direccion_visitados = menu02_04.text_input('direccion', key = 'kd_visitados')

        comentario = menu02_05.text_input('Deja tus comentarios sobre el restaurante', key = 'kc_visitados')

        valoracion = menu02_05b.selectbox('Puntuación',[1, 2, 3, 4, 5], key = 'kv_visitados')

        #menu02_06, menu02_07, menu02_08 = st.beta_columns([1.5, 3, 1])

        #nombre_plato = menu02_06.text_input('Introduce el nombre del plato', key = 'kp_nombrePlato')

        #comentario_plato = menu02_07.text_input('Introduce tu comentario sobre el plato', key = 'kp_comentarioPlato')

        #puntuacion_plato = menu02_08.selectbox('Puntuación del plato', [1, 2, 3, 4, 5], key = 'kp_pusntuacionPlato')

#        {zona_visitados}, {coordenadas_visitados}, {nombre_visitados}, {direccion_visitados}, {comentario}, {valoracion}
#        {nombre_plato}, {comentario_plato}, {puntuacion_plato}
        if menu02_05b.checkbox('Dame opciones'):
            if coordenadas_visitados != '':
                    
        #            {zona_visitados}, {coordenadas_visitados}
                    #sleep(1)

                    if coordenadas_visitados == None:
                        menu02_04.warning('No localizamos la zona. Normalmente se soluciona volviendo a introducir algún dato')

                    else:
                        try:
                            df = td.buscar_visitado(nombre_visitados, coordenadas_visitados)
                            #id_restaurante = td.buscar_en('id_rest', nombre_visitados, 'restaurantes', 'nombre')
                            st.write('')
                            st.write('Estos son los restaurantes que coinciden con los datos introducidos')
                            st.write(df)
                        except:
                            #st.warning('Por favor, actualiza algún dato de tu busqueda')
                            #id_restaurante = None
                            pass

                        if nombre_visitados != '':
                            
                            if comentario != '':

                                if direccion_visitados != '':

                                    #try:

                                    id_restaurante = td.buscar_id_rest(nombre_visitados, direccion_visitados)
#                                    {id_restaurante}
                                    if st.button('Crear comentario'):
                                        
                                        try:
                                            td.add_visitado(id_usuario, id_restaurante, valoracion, comentario)
                                            st.success('Comentario añadido satisfactoriamente')
                                        except:
                                            st.warning('Ha ocurrido un error, recuerda que los comentarios no pueden ser idénticos')
                                
                                    #except:
                                    # st.warning('El nombre del restaurante y la dirección no coinciden')
                                else:
                                    st.warning('Rescuerda que tienes que introducir un dirección para comentar a un restaurante concreto. La tabla te puede ser de ayuda.')
                            
                            else:
                                st.warning('Tienes que introducir un comentario')
                        else:
                            st.warning('No estamos encontrando el restaurante que buscas. Prueba a modificar el nombre o la localización o introducelo en el menú NUEVO RESTAURANTE') 
                            

                            

                

                            

                        #td.add_visitado(id_usuario, id_restaurante, valoracion, comentario)

        #--------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


elif choice == 'RECOMENDACIONES':
    try:
        print(id_usuario)
        hueco_01.header(f"RECOMENDACIONES")
    except:
        hueco_01.subheader('RECOMENDACIONES')
        id_usuario = None

    if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
    else:
        #----------------------------------------------EJECUCIÓN RECOMENDACIONES---------------------------------------------------

        st.write('Hasta que seamos capaces de acceder a tus datos de geolocalización, por favor, indicanos dónde te encuentras o dónde quieres realizar la búsqueda')
        
        menu03_01, menu03_02, menu03_03 = st.beta_columns([1,1,1.5])
        with menu03_01:
            zona_recomendacion = st.text_input('Introduce: zona, ciudad, país', key = 'kz_recomendacion')

        with menu03_02:
            busqueda_recomendacion = st.text_input('¿QUÉ TE APETECE HOY?', key = 'ke_recomendacion')

        lista_etiquetas_recomendacion = td.lista_etiquetas()
    
        with menu03_03:
            etiqueta_recomendacion = st.selectbox('Nuestras opciones', lista_etiquetas_recomendacion)
            radio = st.slider('Distancia máxima en metros', min_value = 500, max_value = 3000, key = 'kr_radio_recomendacion')
        
        if menu03_01.checkbox('Coordenadas'):
            try:
                coordenadas_fol_recomendacion = td.geocode_fol(zona_recomendacion)
                origen = str(coordenadas_fol_recomendacion[0]) + ', ' + str(coordenadas_fol_recomendacion[1])
            except:
                #st.warning('Estamos teniendo problemas para localizarte')
                coordenadas_fol_recomendacion = None
            
            if coordenadas_fol_recomendacion != None and origen != None:
                            
    #            menu03_02.write(str(coordenadas_fol_recomendacion) + ' ' + origen + ' ' + busqueda_recomendacion)
                if busqueda_recomendacion == '':
                            busqueda_recomendacion = etiqueta_recomendacion
                if busqueda_recomendacion != '':
                    if menu03_03.button('BUSCAR'):
                        lista_recomendacion = td.peticion_4s(origen, busqueda_recomendacion, radio = radio)
                        td.add_restaurantes(lista_recomendacion)
                        mostrar = pd.DataFrame(lista_recomendacion).sort_values('distancia')
                        st.write('')

                        menu03_04, menu03_05, menu03_06 = st.beta_columns([1,4,1])
                        map_1 = td.mapa_sugerencias(lista_recomendacion, coordenadas_fol_recomendacion)

                        #with menu03_05:
                        folium_static(map_1, width = 1106)
                        st.write(mostrar[['nombre', 'direccion', 'etiqueta', 'distancia']], layout="wide")
            else:
                st.warning('No encontramos el sitio donde quieres buscar')

        
        
            
        #--------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------EJECUCIÓN NUEVO RESTAURANTE---------------------------------------------------------

elif choice == 'NUEVO RESTAURANTE':
    try:
        print(id_usuario)
        hueco_01.header(f'NUEVO RESTAURANTE')
        if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
        else:

            lista_etiquetas_nuevo_restaurante = td.lista_etiquetas()
            nuevo_restaurante_datos = {}

            #------------------------------------------------------------------------------------------------FILA 1 INTERFAZ
            menu04_01, menu04_02, menu04_03, menu04_04 = st.beta_columns([1, 1.5, 0.65, 1])
            
            with menu04_01:
                nuevo_restaurante_datos['nombre'] = st.text_input('Nombre *', key = 'kn_nuevo_restaurante')

            with menu04_02:
                nuevo_restaurante_datos['direccion'] = st.text_input('Dirección *', key = 'kd_nuevo_restaurante')

            with menu04_03:
                nuevo_restaurante_datos['telefono'] = st.text_input('Teléfono', key = 'kt_nuevo_restaurante')

            with menu04_04:
                nuevo_restaurante_datos['web'] = st.text_input('Web', key = 'kw_nuevo_restaurante')

            #------------------------------------------------------------------------------------------------FILA 2 INTERFAZ
            menu04_05, menu04_06, menu04_07, menu04_08, menu04_09 = st.beta_columns([1, 1, 1, 1, 1])
            
            with menu04_05:
                nuevo_restaurante_datos['municipio'] = st.text_input('Municipio', key = 'km_nuevo_restaurante')

            with menu04_06:
                nuevo_restaurante_datos['codigo'] = st.text_input('Código Postal', key = 'kcp_nuevo_restaurante')

            with menu04_07:
                nuevo_restaurante_datos['ciudad'] = st.text_input('Ciudad *', key = 'kc_nuevo_restaurante')

            with menu04_08:
                nuevo_restaurante_datos['pais'] = st.text_input('Pais *', key = 'kp_nuevo_restaurante')

            with menu04_09:
                nuevo_restaurante_datos['etiqueta'] = st.selectbox('Etiqueta', lista_etiquetas_nuevo_restaurante, key = 'ke_nuevo_restaurante')

            #------------------------------------------------------------------------------------------------
            if menu04_09.button('Añadir Restaurante'):
                address = nuevo_restaurante_datos['direccion'] + ', ' + nuevo_restaurante_datos['ciudad'] + ', ' + nuevo_restaurante_datos['pais']
                coordenadas_fol_nuevo_restaurante = td.geocode_fol(address)
                
                st.write(address)
                st.write(coordenadas_fol_nuevo_restaurante)

                if nuevo_restaurante_datos['nombre'] != '' and nuevo_restaurante_datos['direccion'] != '' and nuevo_restaurante_datos['ciudad'] != '' and nuevo_restaurante_datos['pais'] != '':
                        try:
                            nuevo_restaurante_datos['latitud'] = coordenadas_fol_nuevo_restaurante[0]
                            nuevo_restaurante_datos['longitud'] = coordenadas_fol_nuevo_restaurante[1]
            #                st.write(address)
            #                st.write(coordenadas_fol_nuevo_restaurante)
            #                st.write(nuevo_restaurante_datos['latitud'])
            #                st.write(nuevo_restaurante_datos['longitud'])
            #                st.write(nuevo_restaurante_datos)
                            try:
                                td.add_nuevo_restaurante(nuevo_restaurante_datos)
                                st.success('Restaurante incluido con exito')
                            except:
                                st.warning('No hemos podido añadir el restaurante a la base de datos')
                        except:
                           nuevo_restaurante_datos['latitud'] = None
                           nuevo_restaurante_datos['longitud'] = None
            #               st.write(address)
            #               st.write(coordenadas_fol_nuevo_restaurante)


                        
                else:
                    st.warning('Recuerda que hay campos olbligatorios *')

            

    except:
        pass


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

elif choice == 'BORRAR COMENTARIO':
    try:
        print(id_usuario)
        hueco_01.header(f'BORRAR COMENTARIO')
        if id_usuario == None:
            hueco_01.warning('No te encuentras registrado')
        else:
            menu05_01, menu05_02, menu05_03 = st.beta_columns([5,1,2])
            #st.write('VAS A ELIMINAR UN COMENTARIO')
            lista_desplegable = td.lista_comentarios(id_usuario)
            comentario_borrar = menu05_01.selectbox('Tus comentarios', lista_desplegable, key = 'Lista de comentarios')
            menu05_03.write('')
            menu05_03.write('')
            menu05_03.write('')
            if menu05_03.button('Borrar comentario'):
                td.borrar_comentario(id_usuario, comentario_borrar)
                menu05_01.success('Comentario borrado con éxito')

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
    

