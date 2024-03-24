from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import random
import os
import openai
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
from config import config
from ai import scriptGenerator, voiceGenerator
from videogen import videoGenerator

load_dotenv()
app = Flask(__name__)

configXML = config.Configuration()

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/createvideo', methods=['POST'])
def create_video():
    # Get stuff from client
    title = request.form.get('title')
    prompt = request.form.get('prompt')

    # Gen a script
    scriptGen = scriptGenerator.ScriptGenerator()
    script = scriptGen.prompt(prompt)

    # Gen TTS
    voiceGen = voiceGenerator.VoiceGenerator(script)
    voiceGen.save(title + ".mp3")

    # Gen Video
    videoGen = videoGenerator.VideoGenerator()

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