# Creado por Solo a 15/05/2021, última actualización 16/05/2021, WIP


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

import folium
import json
import os
import pandas as pd
import requests
import sys

from config.config import engine
from datetime import date
from datetime import datetime
from dotenv import load_dotenv
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

sys.path.append("../")
load_dotenv()

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

tok1 = os.getenv('Client_Id')
tok2 = os.getenv('Client_Secret')
tok3 = os.getenv('SQL')

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def geocode(address):
    '''
    Saca las coordenadas de una dirección que le des.
    '''
    data = requests.get(f'https://geocode.xyz/{address}?json=1').json()
    
    try:
        return str(float(data['latt'])) + ', ' + str(float(data['longt']))
    
    except:
        print ('fallo en geocode. No hay resultado')



def geocode_fol(address):
    '''
    Saca las coordenadas de una dirección que le des.
    '''
    data = requests.get(f'https://geocode.xyz/{address}?json=1').json()
    
    try:
        return [float(data['latt']), float(data['longt'])]
    
    except:
        print ('fallo en geocode. No hay resultado')



def buscar_id_mail(mail):

    id_usuario = engine.execute(f"""
        SELECT usuarios.id_usuario
        FROM usuarios
        WHERE usuarios.mail = "{mail}"
    """)

    try:
        respuesta = id_usuario.fetchall()[0][0]
        return respuesta
    except:
        print('Ese usuario no está registrado')



# Esta función me puede ser muy útil a mi, pero no sé cómo de dura se hará para alguien que pueda venir detrás.
# Desde luego a mi me salva un montón de búsquedas de confirmación.
# OJO PORQUE EL DATO DE CONFIRMACIÖN TIENE QUE ESTAR GUARDADO EN UNA VARIABLE (lo suyo es que así sea porque se lo hemos pedido al usuario de alguna manera)
def buscar_en(devolver, dato, tabla, atributo):

    aux = engine.execute(f"""
        SELECT {devolver}
        FROM {tabla}
        WHERE {atributo} = "{dato}"
    """)

    try:
        respuesta = aux.fetchall()[0][0]
        return respuesta
    except:
        return None



def confirmar_pass(mail, password):
    
    usuario = engine.execute(f"""
        SELECT usuarios.pass
        FROM usuarios
        WHERE usuarios.mail = "{mail}"
    """)
    try:
        aux = usuario.fetchall()[0][0]
    except:
        return 'Error de credenciales'
    
    if aux == password:
        return 'Ok'
    else:
        return 'La contraseña o el usuario no coinciden'



def confirmacion(devolver, dato, tabla, atributo):

    aux = engine.execute(f"""
        SELECT {devolver}
        FROM {tabla}
        WHERE {atributo}  = "{dato}"
    """)

    try:
        respuesta = aux.fetchall()[0][0]
        return 'Usuario registrado correctamente'
    except:
        return 'Ese usuario no está registrado'



def add_usuario(nombre, apellidos, direccion, mail, telefono, password):
    try:
        if telefono == 'None':
            engine.execute(f"""
            INSERT INTO usuarios (nombre, apellidos, direccion, mail, telefono, pass)
            VALUES ("{nombre}", "{apellidos}", "{direccion}", "{mail}", "{telefono}", "{password}");
            """ )
            return f'Gracias por registrarte "{nombre}"'

        else:
            engine.execute(f"""
            INSERT INTO usuarios (nombre, apellidos, direccion, mail, pass)
            VALUES ("{nombre}", "{apellidos}", "{direccion}", "{mail}", "{password}");
            """ )
            return f'Gracias por registrarte "{nombre}"'
    except:
        return 'Este usuario ya está registrado'



def buscar_visitado(nombre, zona, ciudad):
    
    origen = geocode(str(zona) + ',' + str(ciudad))
    lista_rest = peticion_4s(origen, nombre, 1000)
    add_restaurantes(lista_rest)
    
    df = pd.read_sql_query(f"""
        SELECT restaurantes.nombre, restaurantes.direccion, municipios.municipio, cp.codigo, ciudades.ciudad, etiquetas.etiqueta
        FROM restaurantes

        INNER JOIN municipios
        ON restaurantes.id_municipio = municipios.id_municipio
        
        INNER JOIN cp
        ON restaurantes.id_cp = cp.id_cp
        
        INNER JOIN ciudades
        ON restaurantes.id_ciudad = ciudades.id_ciudad
        
        INNER JOIN etiquetas
        ON restaurantes.id_etiqueta = etiquetas.id_etiqueta

        WHERE restaurantes.nombre = "{nombre}"
        """, engine)
    
    return df



def lista_visitados(nombre):
    
    df = pd.read_sql_query(f"""
        SELECT restaurantes.nombre, restaurantes.direccion, municipios.municipio, cp.codigo, ciudades.ciudad, etiquetas.etiqueta
        FROM restaurantes

        INNER JOIN municipios
        ON restaurantes.id_municipio = municipios.id_municipio
        
        INNER JOIN cp
        ON restaurantes.id_cp = cp.id_cp
        
        INNER JOIN ciudades
        ON restaurantes.id_ciudad = ciudades.id_ciudad
        
        INNER JOIN etiquetas
        ON restaurantes.id_etiqueta = etiquetas.id_etiqueta

        WHERE restaurantes.nombre = "{nombre}"
        """, engine)
    
    return df



def peticion_4s(origen, busqueda, radio = None, masivo = None):
    
    # Defino las variables que voy a necesitar para hacer el proceso. Son como auxiliares.
    url_query = 'https://api.foursquare.com/v2/venues/explore'
    lista_dic = [] #Esto será lo que devuelva.
    estructura = {} # Esta va a ser mi estructura de datos.
    
    # Defino parámetros de búsqueda para four square (el category se carga la fuerza de la query y además no tiene peso sobre el nombre)
    if masivo == True:
        parametros = {
            'categoryId' : '4d4b7105d754a06374d81259',
            #'section' : 'food',
            'client_id': tok1,
            'client_secret': tok2,
            'v': '20180323',
            'll': origen,
            'query': busqueda, 
            'limit': 100,
            'radius' : radio,    
            }
    else:
         parametros = {
            #'categoryId' : '4d4b7105d754a06374d81259',
            #'section' : 'food',
            'client_id': tok1,
            'client_secret': tok2,
            'v': '20180323',
            'll': origen,
            'query': busqueda, 
            'limit': 100,
            'radius' : radio,    
            }

    
    # Hago la petición
    resp = requests.get(url= url_query, params = parametros).json()

    # La filtro
    data = resp.get("response").get("groups")[0].get("items")
    #return data[0]['venue']['categories'][0]
    
    # Uso esa información para devolver una lista de diccionarios de donde sacar los datos
    for i in range (len(data)):
        dato = data[i]['venue']
        estructura = {'clave' : dato['categories'][0]['id'],
                      'nombre' : dato['name'],
                      'latitud' : dato['location']['lat'],
                      'longitud' : dato['location']['lng'],}      
    # Los datos anteriores están garantizados, los siguientes no, para evitar que se detenga la ejecución hago try
        try:
          estructura['direccion'] = dato['location']['address']
        except:
          estructura['direccion'] = None

        try:
          estructura['distancia'] = dato['location']['distance']
        except:
          estructura['distancia'] = None

        try:
          estructura['postal'] = dato['location']['postalCode']
        except:
          estructura['postal'] = None

        try:
          estructura['acron'] = dato['location']['cc']
        except:
          estructura['acron'] = None

        try:
          estructura['municipio'] = dato['location']['city']
        except:
          estructura['municipio'] = None

        try:
          estructura['ciudad'] = dato['location']['state']
        except:
          estructura['ciudad'] = None

        try:
          estructura['pais'] = dato['location']['country']
        except:
          estructura['pais'] = None

        try:
          estructura['etiqueta'] = dato['categories'][0]['shortName']
        except:
          estructura['etiqueta'] = 'Otros'

        lista_dic.append(estructura)
    
    return lista_dic



def add_restaurantes(lista):  
    
    for elem in lista:
        
        try:
            engine.execute(f"""
            INSERT INTO cp (codigo)
            VALUES ("{elem['postal']}");
            """)
        except:
            print('El código ya existe')
        
        try:
            engine.execute(f"""
            INSERT INTO municipios (municipio)
            VALUES ("{elem['municipio']}");
            """)
        except:
            print('El municipio ya existe')
            
        try:
            engine.execute(f"""
            INSERT INTO ciudades (ciudad)
            VALUES ("{elem['ciudad']}");
            """)
        except:
            print('Esa ciudad ya existe')
            
        try:
            engine.execute(f"""
            INSERT INTO paises (pais, acron)
            VALUES ("{elem['pais']}", "{elem['acron']}");
            """)
        except:
            print('El pais ya existe')
            
        try:
            engine.execute(f"""
            INSERT INTO etiquetas (etiqueta)
            VALUES ("{elem['etiqueta']}");
            """)
        except:
            print('La etiqueta ya existe')
        
        etiqueta = engine.execute(f"""SELECT id_etiqueta FROM etiquetas WHERE etiqueta = "{elem['etiqueta']}" """)
        etiqueta = etiqueta.fetchall()[0][0]
        pais = engine.execute(f""" SELECT id_pais FROM paises WHERE pais = "{elem['pais']}" """)
        pais = pais.fetchall()[0][0]
        ciudad = engine.execute(f""" SELECT id_ciudad FROM ciudades WHERE ciudad = "{elem['ciudad']}" """)
        ciudad = ciudad.fetchall()[0][0]
        municipio = engine.execute(f""" SELECT id_municipio FROM municipios WHERE municipio = "{elem['municipio']}" """)
        municipio = municipio.fetchall()[0][0]
        codigo = engine.execute(f""" SELECT id_cp FROM cp WHERE codigo = "{elem['postal']}" """)
        codigo = codigo.fetchall()[0][0]
        
        try:
            engine.execute(f"""
            INSERT INTO restaurantes (clave, nombre, direccion, latitud, longitud, id_etiqueta, id_pais, id_ciudad, id_municipio, id_cp)
            VALUES ("{elem['clave']}", "{elem['nombre']}", "{elem['direccion']}", "{elem['latitud']}", "{elem['longitud']}", {etiqueta}, "{pais}", "{ciudad}", "{municipio}", "{codigo}");
            """ )
        except:
            print('Este restaurante ya ha sido añadido anteriormente')



def add_visitado(id_usuario, id_restaurante, valoracion, comentario):
    
    fecha = datetime.today().strftime('%Y-%m-%d')
    
    engine.execute(f"""
            INSERT INTO visitado (id_usuario, id_restaurante, valoracion, comentario, fecha)
            VALUES ('{id_usuario}', '{id_restaurante}', '{valoracion}', '{comentario}', '{fecha}');
            """)



def buscar_id_rest(nombre, direccion):

    aux = engine.execute(f"""
        SELECT id_restaurante
        FROM restaurantes
        WHERE nombre = "{nombre}" AND dirección = "{direccion}"
    """)

    try:
        respuesta = aux.fetchall()[0][0]
        return respuesta
    except:
        return None



def mapa_sugerencias(lista, coordenadas_fol):

    map_1 = folium.Map(location= coordenadas_fol, zoom_start= 15)

    iconito = Icon(color = "green",
             prefix = 'fa',
             icon = 'thumbs-o-up',
             icon_color = "black")
            
    usuario = Marker(location = coordenadas_fol, tooltip="Usted está aquí. O no", icon = iconito)
    usuario.add_to(map_1)

    for elem in lista:
        icono = Icon(color = "orange",
             prefix = "fa",
             icon = "cutlery",
             icon_color = "black")

        loc = {"location":[elem['latitud'],elem['longitud']],
            "tooltip": elem['nombre']}

        restaurante = Marker(**loc, icon = icono)

        restaurante.add_to(map_1)
    
    return map_1