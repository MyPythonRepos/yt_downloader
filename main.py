from flask import Flask, render_template, request, redirect
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress

from logger_config import setup_logger
import logging

import os
import re


# Configurar el logger
setup_logger()
logger = logging.getLogger()

app = Flask(__name__)


#########
# RUTAS #
#########


@app.route("/")
def index():
    logger.info("Se accedió a la página de inicio.")
    return render_template("index.html", title='Inicio')


@app.route("/download_file", methods=['GET', 'POST'])
def download_file():
    print("aqui")
    dwld_type = request.form.get("dwld_type")
    save_path = request.form.get("save_path")
    link = request.form.get("yt_link")
    logger.info(f"Descarga {dwld_type} desde {link} en {save_path}")
    download(link, save_path) if dwld_type == "vídeo" else download_playlist(link, save_path)
    # TODO: Recuperar errores de la descarga y mostrarlo en la web
    return redirect("/")


#############
# FUNCIONES #
#############


def download(link, save_path):
    youtube_object = YouTube(link, on_progress_callback=on_progress)
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        if not save_path:
            save_path = os.path.dirname(os.path.abspath(__file__))
        youtube_object.download(save_path)
        logger.info("Descarga finalizada correctamente.")
    except Exception as e:
        logger.error(f"Error al procesar la descarga: {e}")
        exit(1)


def download_playlist(link, save_path):
    logger.info("Descargando playlist...")
    pl = Playlist(link)
    if not save_path:
        save_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + pl.title
    else:
        save_path += "\\" + pl.title
    for idx, video in enumerate(pl.videos):
        logger.info(f"Descargando video {video.title}")
        try:
            video.streams.get_highest_resolution().download(save_path)
            pattern = "[:?\"|/*$]"
            out_file = (save_path+"\\" +
                        re.sub(pattern, "", str(video.streams.get_highest_resolution().default_filename)))
            print(out_file)
            new_file = (save_path+"\\"+str(idx)+"_" +
                        re.sub(pattern, "", str(video.streams.get_highest_resolution().default_filename)))
            print(new_file)
            os.rename(out_file, new_file)
        except Exception as e:
            logger.error(f"Error al procesar la descarga: {e}")
            # exit(1)


if __name__ == '__main__':
    app.run(debug=True)
