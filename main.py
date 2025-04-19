from flask import Flask, render_template, send_file, request, redirect
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress

import os

app = Flask(__name__)

#########
# RUTAS #
#########


@app.route("/")
def index():
    return render_template("index.html", title='Inicio')


@app.route("/download_file", methods=['GET', 'POST'])
def download_file():
    print("aqui")
    dwld_type = request.form.get("dwld_type")
    save_path = request.form.get("save_path")
    link = request.form.get("yt_link")
    print(F"Descarga {type(dwld_type)} desde {link} en {save_path}")
    download(link, save_path) if dwld_type == "vídeo" else download_playlist(link, save_path)
    # if dwld_type == "vídeo":
    #     download(link, path)
    # else:
    #     download_playlist(link, path)

    return redirect("/")


#############
# FUNCIONES #
#############


def download(link, save_path):
    print("Descargando video")
    youtube_object = YouTube(link, on_progress_callback = on_progress)
    youtube_object = youtube_object.streams.get_highest_resolution()
    print(youtube_object)
    try:
        if not save_path:
            save_path = os.path.dirname(os.path.abspath(__file__))
        print(F"Descargando en {save_path}")
        youtube_object.download(save_path)
        print("Download is completed successfully")
    except Exception:
        print(f"An error has occurred: \n{Exception}")
        exit(1)



def download_playlist(link, save_path):
    print("Descargando lista")
    pl = Playlist(link)
    for idx, video in enumerate(pl.videos):
        print(f"Descargando: {video.title}")
        video.streams.get_highest_resolution().download(save_path)
        out_file = save_path+"\\"+video.streams.get_highest_resolution().default_filename
        new_file = save_path+"\\"+str(idx)+"_"+video.streams.get_highest_resolution().default_filename
        os.rename(out_file, new_file)


if __name__ == '__main__':
    app.run( debug=True)
