import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime
import os
import shutil
import json

import keys_1
import consultas




# Título
st.title("Youtube comparación")

# Subtítulo
st.markdown(
    "<h2 style='font-size: 20px;'>Realiza consultas a la API de youtube</h2>",
    unsafe_allow_html=True
)

# Obtener la fecha actual en formato AAAA-MM-DD para complemetar con la inspección y creacion de archivos.csv
hoy = datetime.now().strftime('%Y-%m-%d')
hoy_dt = datetime.strptime(hoy, "%Y-%m-%d")


direccion = 'datos/archivos_temporales'
directorio = os.listdir(direccion)[0] #siempre existe un solo directorio
directorio_dt = datetime.strptime(directorio, "%Y-%m-%d")

#para los datos de los archivos json
ahora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if directorio_dt < hoy_dt:
    #ELIMINACIÖN DE DIRECTORIO
    eliminar_directorio = f'datos/archivos_temporales/{directorio}'
    shutil.rmtree(eliminar_directorio)

    #CREACIÖN DE DIRECTORIO
    crear_directorio =  f'datos/archivos_temporales/{hoy}'
    os.makedirs(crear_directorio, exist_ok=True)


"""___________"""
columna1, columna2 = st.columns(2)

with columna1:

    enlace_1 = st.text_input("⬇️ Introduce el enlace al que te quieres ditigir",
                            value = None,
                            placeholder = "https://www.youtube.com/...",
                            help = f"por ejemplo podrías poner uno de lso siguientes enlaces:\n\nhttps://www.youtube.com/@dateunvlog\n\nhttps://www.youtube.com/@QuantumFracture")
    
    if enlace_1: 
        try:
            e1_consulta = consultas.get_channel_data(enlace_1)
            st.markdown(
                "<hr style='border: none; border-top: 1px dashed black; margin: 10px 0;'>",
                unsafe_allow_html=True
            )
            
            e1_canal = e1_consulta['items'][0]['snippet']['title']
            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'>{e1_canal}</p>", 
                    unsafe_allow_html=True
                ) 
            
            e1_col1, e1_col2 = st.columns([1,2])
            with e1_col1:
                e1_imagen = e1_consulta['items'][0]['snippet']['thumbnails']['medium']['url']
                
                

                st.image(e1_imagen, use_column_width=True)
                

            with e1_col2:
                #fecha de la creación de la cuenta
                e1_cuenta_creada = e1_consulta['items'][0]['snippet']['publishedAt'].split('T')[0]
                st.markdown(
                    f"<p style='font-size: 13px;'>Cuenta creada: {e1_cuenta_creada}</p>",
                    unsafe_allow_html=True
                )

                #cantidad de vitas a la cuenta
                e1_vistas = e1_consulta['items'][0]['statistics']['viewCount']
                st.markdown(
                    f"<p style='font-size: 13px;'>Vistas {e1_vistas}</p>",
                    unsafe_allow_html=True
                )

                #cantidad de videos
                e1_videos = e1_consulta['items'][0]['statistics']['videoCount']
                st.markdown(
                    f"<p style='font-size: 13px;'>Videos: {e1_videos}</p>",
                    unsafe_allow_html=True
                )

                #cantidad de subscriptores
                e1_subscriptores = e1_consulta['items'][0]['statistics']['subscriberCount']
                st.markdown(
                    f"<p style='font-size: 13px;'>Subscriptos: {e1_subscriptores}</p>",
                    unsafe_allow_html=True
                )

            st.markdown(
                    f"<p style='font-size: 18px; color: black;font-weight: bold;'> Videos más destacados_ _ _ _ _ _ _ </p>",  
                    unsafe_allow_html=True
                    )

            
            try:
                 e1_df = pd.read_csv(f'datos/archivos_temporales/{hoy}/{hoy}_{e1_canal}.csv')
                 st.markdown(
                    f"""<p style='font-size: 12px; color: #808080;'>
                    Ya solicidaron por este canal hoy, por ende, los datos hacen referencia a la primera solicitud del día,
                      para ver una actualización nueva, haz la consulta mañana. Te esperamos</p>""",  
                    unsafe_allow_html=True
                    )
            except:
                #Traigo el df del archivo consultas.py y comienzo a trabajarlo
                e1_df = consultas.get_channel_videos(enlace_1)
                e1_df.to_csv(f'datos/archivos_temporales/{hoy}/{hoy}_{e1_canal}.csv')
                pass

            e1_view_url = e1_df.loc[e1_df['view count'].idxmax()]['url']
            e1_likes_url = e1_df.loc[e1_df['like count'].idxmax()]['url']
            e1_comment_url = e1_df.loc[e1_df['comment count'].idxmax()]['url']


            e1_view = e1_df.loc[e1_df['view count'].idxmax()]['view count']
            e1_likes = e1_df.loc[e1_df['like count'].idxmax()]['like count']
            e1_comment = e1_df.loc[e1_df['comment count'].idxmax()]['comment count']

            #Categorías y videos
            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'> Video más visto </p>",  
                    unsafe_allow_html=True
                    )
            st.video(e1_view_url)

            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'> Video con más likes </p>", 
                    unsafe_allow_html=True
                    )
            st.video(e1_likes_url)

            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'> Video con más comentarios </p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )
            st.video(e1_comment_url)


            # Convertir el DataFrame a CSV
            e1_csv = e1_df.to_csv(index=False).encode('utf-8')



            # CSS personalizado para el botón
            st.markdown("""
                <style>
                .stDownloadButton button {
                    background-color: green;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .stDownloadButton button:hover {
                    background-color: darkgreen;
                }
                </style>
                """, unsafe_allow_html=True)
            st.download_button(
                label="Descargar CSV 1",
                data=e1_csv,
                file_name='archivo.csv',
                mime='text/csv'
            )
            st.markdown(
                    f"<p style='font-size: 12px; color: #808080;'> Descarga información sobre todos los videos del canal</p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )
            # Agregar la metadata

            st.markdown("### Información del CSV 1")
            st.markdown("""
            <table style="width:100%; font-size:12px;"> <!-- Se define font-size aquí -->
                <tr>
                    <th style="text-align:left; padding: 10px; background-color:#f2f2f2;"><b>Columna</b></th>
                    <th style="text-align:left; padding: 10px; background-color:#f2f2f2;"><b>Descripción</b></th>
                    <th style="text-align:left; padding: 10px; background-color:#f2f2f2;"><b>Tipo de Datos</b></th>
                </tr>
                <tr>
                    <td>url</td>
                    <td>dirección url </td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>Título</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>published at</td>
                    <td>Fecha y hora de la publicación</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>description</td>
                    <td>descripción</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>view count</td>
                    <td>Cantidad de vistas</td>
                    <td>Entero</td>
                </tr>
                <tr>
                    <td>comment count</td>
                    <td>Cantidad de comentarios</td>
                    <td>Entero</td>
                </tr>
                <tr>
                    <td>like count</td>
                    <td>Cantidad de likes</td>
                    <td>Entero</td>
                </tr>
                <tr>
                    <td>category</td>
                    <td>Categoría a la que pertenece</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>Consultation date</td>
                    <td>Fecha de la consultaa realizada</td>
                    <td>Texto</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)

            # Datos que para almacenar en el archivo JSON
            busqueda_realizada = {
                "busqueda_realizada": enlace_1,
                "fecha": ahora,
                "busqueda_exitosa": "Si"
            }

            direccion = 'datos/consultas'
            directorio = os.listdir(direccion)


            # Crear y guardar el archivo JSON
            with open(f"{direccion}/{len(directorio)+1}_consulta.json", "w") as archivo_json:
                json.dump(busqueda_realizada, archivo_json, indent=4)

        except Exception as e:
                """El valor ingresado no es reconocido como un canal de youtube"""
                """Un ejemplo de un canal de youtube sería:"""
                """https://www.youtube.com/@dateunvlog\n\nhttps://www.youtube.com/@QuantumFracture"""
                # Datos que para almacenar en el archivo JSON
                busqueda_realizada = {
                    "busqueda_realizada": enlace_1,
                    "fecha": ahora,
                    "busqueda_exitosa": "No"
                }

                direccion = 'datos/consultas'
                directorio = os.listdir(direccion)


                # Crear y guardar el archivo JSON
                with open(f"{direccion}/{len(directorio)+1}_consulta.json", "w") as archivo_json:
                    json.dump(busqueda_realizada, archivo_json, indent=4)
                pass

with columna2:
    enlace_2 = st.text_input("⬇️ Introduce otro enlace al que te quieres ditigir",
                            value = None,
                            placeholder = "https://www.youtube.com/...",
                            help = f"por ejemplo podrías poner uno de los siguientes enlaces:\n\nhttps://www.youtube.com/@dateunvlog\n\nhttps://www.youtube.com/@QuantumFracture")
    
    if enlace_2:
        try: 
            e2_consulta = consultas.get_channel_data(enlace_2)
            st.markdown(
                "<hr style='border: none; border-top: 1px dashed black; margin: 10px 0;'>",
                unsafe_allow_html=True
            )
            
            e2_canal = e2_consulta['items'][0]['snippet']['title']
            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'>{e2_canal}</p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                ) 
            
            e2_col3, e2_col4 = st.columns([1,2])
            with e2_col3:
                e2_imagen = e2_consulta['items'][0]['snippet']['thumbnails']['medium']['url']
                
                

                st.image(e2_imagen, use_column_width=True)
                

            with e2_col4:
                #fecha de la creación de la cuenta
                e2_cuenta_creada = e2_consulta['items'][0]['snippet']['publishedAt'].split('T')[0]
                st.markdown(
                    f"<p style='font-size: 13px;'>Cuenta creada: {e2_cuenta_creada}</p>",
                    unsafe_allow_html=True
                )

                #cantidad de vitas a la cuenta
                e2_vistas = e2_consulta['items'][0]['statistics']['viewCount']
                st.markdown(
                    f"<p style='font-size: 13px;'>Vistas {e2_vistas}</p>",
                    unsafe_allow_html=True
                )

                #cantidad de videos
                e2_videos = e2_consulta['items'][0]['statistics']['videoCount']
                st.markdown(
                    f"<p style='font-size: 13px;'>Videos: {e2_videos}</p>",
                    unsafe_allow_html=True
                )

                #cantidad de subscriptores
                e2_subscriptores = e2_consulta['items'][0]['statistics']['subscriberCount']
                st.markdown(
                    f"<p style='font-size: 13px;'>Subscriptos: {e2_subscriptores}</p>",
                    unsafe_allow_html=True
                )


            st.markdown(
                    f"<p style='font-size: 18px; color: black;font-weight: bold;'> Videos más destacados_ _ _ _ _ _ _ </p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )

            try:
                 e2_df = pd.read_csv(f'datos/archivos_temporales/{hoy}/{hoy}_{e2_canal}.csv')
                 st.markdown(
                    f"""<p style='font-size: 12px; color: #808080;'>
                    Ya solicidaron por este canal hoy, por ende, los datos hacen referencia a la primera solicitud del día,
                      para ver una actualización nueva, haz la consulta mañana. Te esperamos.</p>""",  
                    unsafe_allow_html=True
                    )
            except:
                #Traigo el df del archivo consultas.py y comienzo a trabajarlo
                e2_df = consultas.get_channel_videos(enlace_2)
                e2_df.to_csv(f'datos/archivos_temporales/{hoy}/{hoy}_{e2_canal}.csv')
                pass



            e2_view_url = e2_df.loc[e2_df['view count'].idxmax()]['url']
            e2_likes_url = e2_df.loc[e2_df['like count'].idxmax()]['url']
            e2_comment_url = e2_df.loc[e2_df['comment count'].idxmax()]['url']


            e2_view = e2_df.loc[e2_df['view count'].idxmax()]['view count']
            e2_likes = e2_df.loc[e2_df['like count'].idxmax()]['like count']
            e2_comment = e2_df.loc[e2_df['comment count'].idxmax()]['comment count']


            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'> Video más visto </p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )
            st.video(e2_view_url)

            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'> Video con más likes </p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )
            st.video(e2_likes_url)

            st.markdown(
                    f"<p style='font-size: 16px; color: black;font-weight: bold;'> Video con más comentarios </p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )
            st.video(e2_comment_url)


            # Convertir el DataFrame a CSV
            e2_csv = e2_df.to_csv(index=False).encode('utf-8')



            # CSS personalizado para el botón
            st.markdown("""
                <style>
                .stDownloadButton button {
                    background-color: green;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .stDownloadButton button:hover {
                    background-color: darkgreen;
                }
                </style>
                """, unsafe_allow_html=True)
            st.download_button(
                label="Descargar CSV 2",
                data=e2_csv,
                file_name='archivo.csv',
                mime='text/csv'
            )
            st.markdown(
                    f"<p style='font-size: 12px; color: #808080;'> Descarga información sobre todos los videos del canal</p>",  # Cambia 'black' al color que desees
                    unsafe_allow_html=True
                    )

            # Agregar la metadata
            st.markdown("### Información del CSV 2")
            st.markdown("""
            <table style="width:100%; font-size:12px;"> <!-- Se define font-size aquí -->
                <tr>
                    <th style="text-align:left; padding: 10px; background-color:#f2f2f2;"><b>Columna</b></th>
                    <th style="text-align:left; padding: 10px; background-color:#f2f2f2;"><b>Descripción</b></th>
                    <th style="text-align:left; padding: 10px; background-color:#f2f2f2;"><b>Tipo de Datos</b></th>
                </tr>
                <tr>
                    <td>url</td>
                    <td>dirección url </td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>Título</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>published at</td>
                    <td>Fecha y hora de la publicación</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>description</td>
                    <td>descripción</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>view count</td>
                    <td>Cantidad de vistas</td>
                    <td>Entero</td>
                </tr>
                <tr>
                    <td>comment count</td>
                    <td>Cantidad de comentarios</td>
                    <td>Entero</td>
                </tr>
                <tr>
                    <td>like count</td>
                    <td>Cantidad de likes</td>
                    <td>Entero</td>
                </tr>
                <tr>
                    <td>category</td>
                    <td>Categoría a la que pertenece</td>
                    <td>Texto</td>
                </tr>
                <tr>
                    <td>Consultation date</td>
                    <td>Fecha de la consultaa realizada</td>
                    <td>Texto</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)

            # Datos que para almacenar en el archivo JSON
            busqueda_realizada = {
                "busqueda_realizada": enlace_2,
                "fecha": ahora,
                "busqueda_exitosa": "Si"
            }

            direccion = 'datos/consultas'
            directorio = os.listdir(direccion)


            # Crear y guardar el archivo JSON
            with open(f"{direccion}/{len(directorio)+1}_consulta.json", "w") as archivo_json:
                json.dump(busqueda_realizada, archivo_json, indent=4)
        except Exception as e:
                """El valor ingresado no es reconocido como un canal de youtube"""
                """Un ejemplo de un canal de youtube sería:"""
                """https://www.youtube.com/@dateunvlog\n\nhttps://www.youtube.com/@QuantumFracture"""
                # Datos que para almacenar en el archivo JSON
                busqueda_realizada = {
                    "busqueda_realizada": enlace_2,
                    "fecha": ahora,
                    "busqueda_exitosa": "No"
                }

                direccion = 'datos/consultas'
                directorio = os.listdir(direccion)


                # Crear y guardar el archivo JSON
                with open(f"{direccion}/{len(directorio)+1}_consulta.json", "w") as archivo_json:
                    json.dump(busqueda_realizada, archivo_json, indent=4)
                pass

