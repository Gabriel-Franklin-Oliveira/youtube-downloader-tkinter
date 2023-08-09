from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pytube import YouTube
import urllib.request
import io
import os


# Main Window
root = Tk()
root.title("YouTube Converter")
root.geometry("400x540")
root.resizable(FALSE, FALSE)
root.config(padx=20)
icon = Image.open("img/icon.ico")
root.iconphoto(True, ImageTk.PhotoImage(icon))
logo = Image.open("img/logo.png")
logo_photo = ImageTk.PhotoImage(logo)
example = Image.open("img/example_thumb2.jpg")
example_thumb = ImageTk.PhotoImage(example)


"""
TODO 2 - Voltar para o titulo original caso nao tenha escolhido o formato
"""

#----PROGRAM CONFIGS----------------------------------------------------
selected_format = None


def search_video(event=None):
    video_url = entry_url.get()
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        title_label2.config(text=video_title, fg="black")
        choose_format_button.config(state="normal")
        download_button.config(state="normal")

        thumbnail_url = f"https://img.youtube.com/vi/{video_url.split('=')[1]}/0.jpg"
        response = urllib.request.urlopen(thumbnail_url)
        thumbnail_data = response.read()

        thumbnail_image = Image.open(io.BytesIO(thumbnail_data))
        thumbnail_image = thumbnail_image.resize((300, 200), Image.LANCZOS)

        img = ImageTk.PhotoImage(thumbnail_image)
        thumb_label.configure(image=img)
        thumb_label.image = img


    except Exception:
        title_label2.config(text="Invalid URL", fg="red")
        thumb_label.config(image=example_thumb)

    directory_label.config(text="")
    status_label.config(text="")


def choose_format():
    def set_format(format):
        global selected_format
        selected_format = format
        format_window.destroy()

    format_window = Toplevel(root)
    format_window.title("")
    format_window.geometry("200x150")
    format_window.config(padx=10, pady=10)
    format_window.resizable(FALSE, FALSE)

    format_label = Label(format_window, text="Choose Format:", font=("Arial", 12, "bold"), pady=5)
    format_label.pack()

    mp3_button = Button(format_window, text="MP3", font=("Arial", 12, "bold"), padx=35, pady=4, borderwidth=3, command=lambda: set_format("mp3"))
    mp3_button.pack()

    mp4_button = Button(format_window, text="MP4", font=("Arial", 12, "bold"), padx=35, pady=4, borderwidth=3, command=lambda: set_format("mp4"))
    mp4_button.place(x=30, y=80)


def download_video():
    global selected_format

    video_url = entry_url.get()
    try:
        yt = YouTube(video_url)

        if selected_format == "mp3":
            video = yt.streams.get_audio_only()
            output_path = "./download/mp3"
        elif selected_format == "mp4":
            video = yt.streams.get_highest_resolution()
            output_path = "./download/mp4"
        else:
            title_label2.config(text="Invalid Format", fg="red")


        if video:
            directoty = os.getcwd()
            full_path = os.path.join(directoty, "download")
            video.download(output_path=output_path)
            status_label.config(text="Download concluído!")
            directory_label.config(text=f"Saved at: {full_path}")
        else:
            title_label2.config(text="Invalid Format or URL", fg="red")

    except Exception:
        title_label2.config(text="Invalid Format or URL", fg="red")

    selected_format = None

#-----------------------------------------------------------------------


# Labels
logo_label = Label(root, image=logo_photo)
logo_label.pack()
url_label = Label(text="Enter video URL:", font=("Arial", 16, "bold"))
url_label.pack()
entry_url = Entry(width=39, borderwidth=2, relief=SOLID, highlightbackground="black", font=("Arial", 10))
entry_url.bind("<Return>", search_video)
entry_url.place(x=10, y=140)


title_label = Label(text="Title:", font=("Arial", 12, "bold"))
title_label.place(x=6, y=170)
title_label2 = Label(text='"Example of video title"', font=("Arial", 12, "bold"), fg="#7d7d7d")
title_label2.place(x=50, y=170)


status_label = Label(root, text="", font=("Arial", 12, "bold"))
status_label.place(x=8, y=240)
directory_label = Label(root, text="")
directory_label.place(x=8, y=260)
directory_label.config(wraplength=380)

thumb_label = Label(root, image=example_thumb, borderwidth=3, relief=SOLID, highlightbackground="black")
thumb_label.place(x=30, y=300)


# Buttons
search_button = Button(text="Search", padx=6, borderwidth=1, bg="#3d2a91", fg="white", relief=SOLID, command=search_video)
search_button.place(x=290, y=139)

choose_format_button = Button(text="Choose Format", font=("Arial", 12, "bold"), padx=10, command=choose_format, state="disabled")
choose_format_button.place(x=30, y=199)

download_button = Button(text="Download", font=("Arial", 12, "bold"), padx=25, bg="#3d2a91", fg="white", command=download_video, state="disabled")
download_button.place(x=195, y=199)



root.mainloop()
