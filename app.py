from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import random
import os
import openai
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/createvideo', methods=['POST'])
def create_video():
    # Here, you can add logic to handle video creation.
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
    content = response.choices[0].text

    # Create the directory
    if os.path.exists('media/output') == False:
        os.mkdir('media/output')

    # Generate speech for the video
    speech = gTTS(text=content, lang='en', tld='ca', slow=False)
    speech.save("media/output/speech.mp3")
    audio_clip = AudioFileClip("media/output/speech.mp3")

    if (audio_clip.duration + 1.3 > 58):
        print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
        exit()

    print('\n')

    ### VIDEO EDITING ###

    # Trim a random part of minecraft gameplay and slap audio on it
    video_clip = VideoFileClip("media/input/BackgroundVideo.mp4").subclip(0, 0 + audio_clip.duration + 1.3)
    video_clip = video_clip.set_audio(audio_clip)
    # Create a text clip (you can customize the font, size, color, etc.)
    text = TextClip(content, fontsize=70, color='white')

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
    video_clip.write_videofile("media/output/" + title + ".mp4")
    # Example response
    response = {
        "status": "success",
        "message": "Video creation initiated."
    }
    return jsonify(response), 200

@app.route('/posttest', methods=['POST'])
def posttest():
    title = request.form.get('title')
    prompt = request.form.get('prompt')

    print(f"Title: {title}")
    print(f"Prompt: {prompt}")

    return "Form data received and printed to console."

if __name__ == '__main__':
    app.run()