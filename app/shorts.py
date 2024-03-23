# Import everything
from dotenv import load_dotenv
import random
import os
import openai
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
load_dotenv()

# Ask for video info
title = "helloworld"

# Generate content using OpenAI API
theme = "generate a short 2 question quiz. No other text, just the questions."

### MAKE .env FILE AND SAVE YOUR API KEY ###
openai.api_key = os.environ["OPENAI_API"]
response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",
    prompt=f"Generate content on - \"{theme}\"",
    temperature=0.7,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
print(response.choices[0].text)

# Create the directory
if os.path.exists('generated') == False:
    os.mkdir('generated')

# Generate speech for the video
speech = gTTS(text=content, lang='en', tld='ca', slow=False)
speech.save("generated/speech.mp3")
audio_clip = AudioFileClip("generated/speech.mp3")

if (audio_clip.duration + 1.3 > 58):
    print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
    exit()

print('\n')

### VIDEO EDITING ###

# Trim a random part of minecraft gameplay and slap audio on it
video_clip = VideoFileClip("media/input/BackgroundVideo.mp4").subclip(0, 0 + audio_clip.duration + 1.3)
final_clip = video_clip.set_audio(audio_clip)

# Resize the video to 9:16 ratio
w, h = final_clip.size
target_ratio = 1080 / 1920
current_ratio = w / h

if current_ratio > target_ratio:
    # The video is wider than the desired aspect ratio, crop the width
    new_width = int(h * target_ratio)
    x_center = w / 2
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center)
else:
    # The video is taller than the desired aspect ratio, crop the height
    new_height = int(w / target_ratio)
    x_center = w / 2
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center)

# Write the final video
final_clip.write_videofile("generated/" + title + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)