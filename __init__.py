from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

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

    @intent_handler(IntentBuilder("").require("IHaveAQuestion"))
    def handle_i_have_a_question_intent(self, message):
        self.speak_dialog("i.have.a.question")

        question = self.get_response(dialog="i.have.a.question")
        with open("/home/pi/test.question", "w") as fl:
            fl.write(question)

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return AntoniaSkill()
