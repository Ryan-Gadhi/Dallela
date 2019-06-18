import os 
import json
from adapt.engine import IntentDeterminationEngine

class Engine:
    eng = None  # engine object (singleton)
    skills = [] # list of skills
    mapper = {} # maps intents to functions
     
    def __init__(self):
        if not Engine.eng:
            self.eng = IntentDeterminationEngine()
            for folder in os.listdir("skills"):
                if not folder.startswith("Daleelah_"): continue
                self.skills.append( __import__("skills." + folder, fromlist=['']) )
            self.__registerEngEntities()
            self.__registerEngIntents()
            self.__mapper()

    
    def __registerEngEntities(self):
        entities = {}
        for skill in self.skills:
            entities.update( getattr(skill, "getEntities")() )

        for entity, keywords in entities.items():
            for keyword in keywords:
                self.eng.register_entity(keyword, entity)
    
    def __registerEngIntents(self):
        for skill in self.skills:
            for intent in getattr(skill, "getIntents")() :
                 self.eng.register_intent_parser(intent)
    
    def __mapper(self):
        for skill in self.skills:
            self.mapper.update( getattr(skill, "getMap")() )

    def compute(self, txt):
        for intent in self.eng.determine_intent(txt):
            if intent.get('confidence') > 0:
                self.mapper.get( intent.get('intent_type') ) ()
                print(json.dumps(intent, indent=4))


if __name__ == "__main__":
    e = Engine()
    e.compute("What is the weather in Dammam ? ")
    
    
