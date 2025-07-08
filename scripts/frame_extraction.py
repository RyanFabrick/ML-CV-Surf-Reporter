import os
import subprocess
from yt_dlp import YoutubeDL
from win10toast import ToastNotifier


#create downloads/ and frames/ folders
os.makedirs('downloads', exist_ok=True)
os.makedirs('frames', exist_ok=True)

vid_urls = ['https://www.youtube.com/watch?v=6ZPM4t5Oiio']

ydl_options = {

    #best vid quality, mp4 format
    'format': 'bestvideo[ext=mp4]',
    #file saved with title as filename
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    #progress in terminal
    'quiet': False,
    #no warnings unless errors
    'no_warnings': True,

    #for HLS download since I need livestream frames currently
    #'hls_prefer_native': True
}

with YoutubeDL(ydl_options) as ydl:
    for url in vid_urls:
        #stores metadata as 'info', downloads video
        info = ydl.extract_info(url, download=True)
        #names file afte video title, else name is 'video'
        vid_title = info.get('title', 'video')
        #builds file path
        filename = os.path.join('downloads', f'{vid_title}.mp4')
        #FFmpeg - names each image frame
        frame_pattern = os.path.join('frames', f'{vid_title}_%04d.jpg')

        start_time = '00:00:00'
        duration = '00:01:06' 

        command = [
            'ffmpeg',
            #start time
            '-ss', start_time,
            #duration extraction
            '-t', duration,
            #input video
            '-i', filename,
            #extracts frames at .5 fps
            '-vf', 'fps=0.5',
            frame_pattern
        ]

        #runs FFmpeg command, error if fails
        subprocess.run(command, check=True)

#After download and frame extraction --> notification sent
toaster = ToastNotifier()
toaster.show_toast("Vid Downloaded, Frame Extraction Complete", duration=20)