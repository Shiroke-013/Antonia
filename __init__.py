from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.skills.audioservice import AudioService

import json # This library make us able to convert text to json.
import os # This library make us be able to execute Os commands
import time
import speech_recognition as sr

class AntoniaSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor.
    def __init__(self):
        super(AntoniaSkill, self).__init__("AntoniaSkill")
        # Initialize working variables used within the skill.
        self.count = 0
        # This will be the json to send to the server.
        self.jsonTest = {
            "user": "Antonia",
        }

        # Config variables
        self.JSON_PATH = '/home/pi/Antonia/assets/json/request.json'
        self.AUDIO_PATH ="/home/pi/answer/answer.mp3"
        self.REQUEST_JSON = 'request.json'
        self.NGROK_ROUTE = 'https://projectantonia.ngrok.io/test/message'

    # Creating I have a question intent.
    def initialize(self):
        i_have_a_question = IntentBuilder("IHaveAQuestion").require("IHaveAQuestion").build()
        self.register_intent(i_have_a_question, self.handle_i_have_a_question_intent)
        self.audio_service = AudioService(self.bus)
        
        
    @intent_handler(IntentBuilder("").require("IHaveAQuestion"))
    def handle_i_have_a_question_intent(self, message):
        self.speak_dialog("i.have.a.question")
        recognizer = sr.Recognizer()
        source = sr.Microphone()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration = 1) # nivela el microfono segun el ruido del ambiente
            audio = recognizer.listen(source, timeout = None)
            question = recognizer.recognize_google(audio, language = "es-ES")

        add_atributes_to_json(question)
        generate_json()
        execute_curl(self.REQUEST_JSON, self.NGROK_ROUTE)
        play_mp3(self.AUDIO_PATH)
        os.remove(self.AUDIO_PATH)
        
    def add_atributes_to_json(self, request):
        self.jsonTest["text"] = request

    def generate_json(self):
        with open(self.JSON_PATH, 'w') as outfile:
            json.dump(self.jsonTest, outfile)

    def execute_curl(self, jsonName, tunnelUrl):
        os.system('curl -H "Content-Type: application/json" -d @/home/pi/Antonia/assets/json/' + jsonName + ' ' + tunnelUrl)

    def play_mp3(self, audio_path):
        while not os.path.exists(audio_path):
            time.sleep(3)
        self.audio_service.play(audio_path)
        os.system('mpg123 ' + audio_path)
        
# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return AntoniaSkill()
