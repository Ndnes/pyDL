# pyDL
Python script to download videos from YouTube using pyTube. Can download all resolutions and convert/combine separate video/audio streams with ffmpeg. (download ffmpeg separately)

# Note on DASH streaming method.
Since YouTube uses Dynamic Adaptive Streaming over HTTP the video and audio files must be downloaded separately for videos
with a resolution greater than 720p. This CLI will handle that automatically, but to merge the separate files back to one
file with both video and audio ffmpeg is used. All that is needed to handle this is to download ffmpeg and put the executable
named ffmpeg.exe in the root folder of this project. For videos with a resolution greater than 720p you will get three files,
the bare video, the bare audio and the merged file. This way you can still manually merge the audio and video in case something goes wrong with the ffmpeg conversion.