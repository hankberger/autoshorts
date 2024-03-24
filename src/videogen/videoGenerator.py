
from dotenv import load_dotenv
import random
import os
import openai
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
from ..config import config

configXML = config.Configuration()

class VideoGenerator:
    def __init__():
        return
    
    def generate(script, speech, title):
        # Create the directory
        if os.path.exists(configXML.PathToMediaOutput) == False:
            os.mkdir(configXML.PathToMediaOutput)

        # Get Audio file
        audio_clip = AudioFileClip(f"{configXML.PathToMediaOutput}/{title}.mp3") # get the generated audio file

        if (audio_clip.duration + 1.3 > 58):
            print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
            exit()

        print('\n')

        ### VIDEO EDITING ###

        # Trim a random part of minecraft gameplay and slap audio on it
        video_clip = VideoFileClip(f"{configXML.PathToMediaInput}/BackgroundVideo.mp4").subclip(0, 0 + audio_clip.duration + 1.3)
        video_clip = video_clip.set_audio(audio_clip)
        # Create a text clip (you can customize the font, size, color, etc.)
        text = TextClip(script, fontsize=70, color='white')

        # Set the position of the text in the center and duration to be the same as the video
        text = text.set_pos('center').set_duration(video_clip.duration)

        # Overlay the text on your video
        video_clip = CompositeVideoClip([video_clip, text])

        # # Resize the video to 9:16 ratio
        # w, h = final_clip.size
        # target_ratio = 1080 / 1920
        # current_ratio = w / h

        # if current_ratio > target_ratio:
        #     # The video is wider than the desired aspect ratio, crop the width
        #     new_width = int(h * target_ratio)
        #     x_center = w / 2
        #     y_center = h / 2
        #     final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center)
        # else:
        #     # The video is taller than the desired aspect ratio, crop the height
        #     new_height = int(w / target_ratio)
        #     x_center = w / 2
        #     y_center = h / 2
        #     final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center)

        # Write the final video
        video_clip.write_videofile(f"{configXML.PathToMediaOutput}/{title}.mp4")