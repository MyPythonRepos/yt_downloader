from flask import Flask, render_template, send_file, request, redirect
from pytube import YouTube, Playlist

import os

app = Flask(__name__)

#########
# RUTAS #
#########


@app.route("/")
def index():
    return render_template("index.html", title='Inicio')


@app.route("/download", methods=['GET','POST'])
def download_file():
    tipo_descarga = request.form.get("dwld_type")
    path = request.form.get("save_path")
    link = request.form.get("yt_link")
    download(link, path) if tipo_descarga == "video" else download_playlist(link, path)
    return redirect("/")


#############
# FUNCIONES #
#############


def download(link, save_path):
    youtube_object = YouTube(link)
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        if not save_path:
            save_path = os.path.dirname(os.path.abspath(__file__))
        youtube_object.download(save_path)
    except Exception:
        print(f"An error has occurred: \n{Exception}")
        exit(1)
    print("Download is completed successfully")


def download_playlist(link, save_path):
    pl = Playlist(link)
    for idx, video in enumerate(pl.videos):
        print(f"Descargando: {video.title}")
        video.streams.get_highest_resolution().download(save_path)
        out_file = save_path+"\\"+video.streams.get_highest_resolution().default_filename
        new_file = save_path+"\\"+str(idx)+"_"+video.streams.get_highest_resolution().default_filename
        os.rename(out_file, new_file)


if __name__ == '__main__':
    app.run( debug=True)
