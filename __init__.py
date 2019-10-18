from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.skills.audioservice import AudioService

import json # This library make us able to convert text to json.
import os # This library make us be able to execute Os commands

JSON_PATH = 'assets/json/request.json'

 # This will be the json to send to the server.
jsonTest = {
    "user": "Antonia",
}

class AntoniaSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor.
    def __init__(self):
        super(AntoniaSkill, self).__init__("AntoniaSkill")
        # Initialize working variables used within the skill.
        self.count = 0

    def initialize(self):
        # Creating I have a question intent.
        i_have_a_question = IntentBuilder("IHaveAQuestion").require("IHaveAQuestion").build()
        self.register_intent(i_have_a_question, self.handle_i_have_a_question_intent)
        self.audio_service = AudioService(self.bus)
        
        
    @intent_handler(IntentBuilder("").require("IHaveAQuestion"))
    def handle_i_have_a_question_intent(self, message):
        
        question = self.get_response(dialog="i.have.a.question")
        add_atributes_to_json(question)
        generate_json()
        execute_curl('request.json', 'https://projectantonia.ngrok.io/test/message')
       #added:
        mp3(self, "/home/pi/answer")
        
    def add_atributes_to_json(request):
        jsonTest["text"] = request

    def generate_json():
        with open(JSON_PATH, 'w') as outfile:
            json.dump(jsonTest, outfile)

    def execute_curl(jsonName, tunnelUrl):
        os.system('curl -H "Content-Type: application/json" -d @assets/json/' + jsonName + ' ' + tunnelUrl)


        #added:
    def mp3(self, audio_path):
        while os.path.exist(audio_path):
            self.audio_service.play(audio_path)
            os.remove("answer.mp3")
        
# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return AntoniaSkill()
