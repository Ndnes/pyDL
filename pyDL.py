from pytube import YouTube
from pytube import helpers as pytube_helpers
import math
import tkinter as tk
from tkinter import filedialog
import os

# Callback to get progress updates while downloading.
def on_progress(
    file,
    chunk,
    bytes_remaining
):
    total_size = file.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = math.floor(bytes_downloaded / total_size * 100)
    totalsz = (total_size/1024)/1024
    totalsz = round(totalsz, 1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    print(f'\rDownload Progress: {percentage_of_completion}%, Total Size: {totalsz} MB, Remaining: {remain} MB')


while True:

    print("Please enter the url of the YouTube video you would lik to download.")

    url = input("YouTube url: ")

    try:
        yt = YouTube(url)
    except:
        print("Error parsing the url. Exiting.")
        break

    if yt is None:
        print("Could not find the video. Exiting.")
        break


    print(f"Do you wish to download \"{yt.title}\"?")
    q = input("y / n: ")

    if not (
        q.upper() == "Y" or 
        q.upper() == "YES" or 
        q.upper() == "YEAH" or 
        q.upper() == "YE"
    ):
        print("Exiting")
        break

    yt.register_on_progress_callback(on_progress)

    query = yt.streams.filter(type='video').order_by('resolution')

    print("\nVideo is available in the following formats:")
    video_formats = ""
    for index, stream in enumerate(query):
        video_formats += f"{index}: {stream.resolution}, {stream.fps} fps, {stream.mime_type}\n"
    
    print(video_formats)
    print("Please choose the format you would like to download. (1, 2, 3 etc.)")
    while(True):
        choice = input()
        try:
            i = int(choice)
            if not (i < 0 or i > len(query) - 1):
                break
            else:
                print("Please enter an integer within the range of options.")
        except:
            print("Please enter a valid integer corresponding to the stream you wish to download.")

    print(f"The file size for the selected stream is {round( query[i].filesize / 1.0e9, ndigits=3)} Gb. (plus audio?) Do you wish to proceed?")

    q = input("y / n: ")

    if not (
        q.upper() == "Y" or 
        q.upper() == "YES" or 
        q.upper() == "YEAH" or 
        q.upper() == "YE"
    ):
        print("Exiting")
        break

    print("Choose save location from dialogue box.")

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()

    print(f"Downloading to: {path}")

    savepath_vid = None
    savepath_audio = None
    progressive = True
    if path:
        filename = pytube_helpers.safe_filename(query[i].title)
        filename = filename.replace(' ', '_')
        filename = filename.replace('&', 'and')
        savepath_vid = query[i].download(output_path = path, filename=filename)
        # If stream is not progressive, it uses DASH and audio must be downloaded separately.
        if(not query[i].is_progressive):
            progressive = False
            # Find the corresponding audio stream of highest bitrate to selected video stream.
            type, mime = query[i].mime_type.split('/')
            audio = yt.streams.filter(mime_type=f"audio/{mime}").order_by('abr').last()
            savepath_audio = audio.download(output_path = path, filename=filename, filename_prefix = 'audio_')

    if not progressive:
        print('\n\n Combining video and audio file using ffmpeg. \n\n')
        savepath_vid = savepath_vid.replace('/', '\\')
        savepath_audio = savepath_audio.replace('/', '\\')
        os.system(f"ffmpeg -i {savepath_vid} -i {savepath_audio} -c copy {savepath_vid}_combined.{mime}")

    print("Done")
    break

    # USEFUL FFMPEG CUT COMMAND
    # ffmpeg -i input.extension -ss 16:18:03 -to 39:88:74 -c copy output.extension
