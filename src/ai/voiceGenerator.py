from gtts import gTTS
from enum import Enum
import os
import config
from faster_whisper import WhisperModel
import pysubs2

configXML = config.Configuration()

class EnglishAccent(Enum):
    """Enum of tld options for the Google TextToSpeech. The tld parameter controls the accent of the test to speech output.
    """
    UnitedStates = "us"
    Australian = "com.au"
    British = "co.uk"
    Canadian = "ca"
    Indian = "co.in"
    Irish = "ie"
    SouthAfrican = "co.za"

class VoiceGenerator():
    def __init__(self, script, tld=EnglishAccent.UnitedStates, slow=False) -> None:
        """This function initializes the TTS API interface for TTS

        Args:
            script (str): the script that you want TTS to narrate.
            tld (EnglishAccent, optional): controls the accent of TTS output using a top-level-domain from the EnglishAccent Enum. Defaults to UnitedStates. 
            slow (bool, optional): whether to slow the speech for the output. Defaults to False.
        """
        self.gTTS = gTTS(script, tld.value, "en", slow)
    
    def generateSRTFile(pathToAudio: str):
        model = WhisperModel("small")
        segments, _ = model.transcribe(pathToAudio)
        results = []
        for segment in segments:
            results.append({'start':segment.start,'end':segment.end,'text':segment.text})
        pysubs2.load_from_whisper(results).save(pathToAudio.replace(".mp3",".srt"))

    def save(self, filePath):
        """This function generates the TTS voice file given a script.

        Args:
            filePath (str): the file path that you want save the result to. 
        """
        # Create the directory if needed
        if os.path.exists(configXML.PathToMediaOutput) == False:
            os.mkdir(configXML.PathToMediaOutput)
        
        savePath = configXML.PathToMediaOutput + filePath

        self.gTTS.save(savePath)
        VoiceGenerator.generateSRTFile(savePath)
