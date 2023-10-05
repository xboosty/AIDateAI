import os
import openai
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, request
import numpy as np
#import json
sys.path.append("../..")
from models.OpenAI.Whisper.transcriber import Transcriber
#from llm import LLM
#from weather import Weather
#from tts import TTS
#from pc_command import PcCommand

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    #Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    text = Transcriber().transcribe(audio)
    return {"result":"ok","text":text}