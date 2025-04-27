from flask import Flask, render_template, request, redirect
#from flask_bootstrap import Bootstrap5

from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress

import os
import re

app = Flask(__name__)
#bootstrap = Bootstrap5(app)

app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'  # default to 'md'

#########
# RUTAS #
#########


@app.route("/")
def index():
    return render_template("index.html", title='Inicio')


@app.route("/download_file", methods=['GET', 'POST'])
def download_file():
    dwld_type = request.form.get("dwld_type")
    save_path = request.form.get("save_path")
    link = request.form.get("yt_link")
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
        print("Descarga finalizada correctamente")
    except Exception as e:
        print(f"Ha ocurrido un error: \n{e}")
        exit(1)


def download_playlist(link, save_path):
    print("Descargando lista")
    pl = Playlist(link)
    if not save_path:
        save_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + pl.title
    else:
        save_path += "/" + pl.title
    for idx, video in enumerate(pl.videos):
        print(f"Descargando: {video.title}")
        try:
            video.streams.get_highest_resolution().download(save_path)
            pattern = "[:?\"|/*$]"
            out_file = (save_path+"/" +
                        re.sub(pattern, "", str(video.streams.get_highest_resolution().default_filename)))
            print(out_file)
            new_file = (save_path+"/"+str(idx)+"_" +
                        re.sub(pattern, "", str(video.streams.get_highest_resolution().default_filename)))
            print(new_file)
            os.rename(out_file, new_file)
        except Exception as e:
            print(f"Ha ocurrido un error: \n{e}")
            # exit(1)


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            debug=True)
