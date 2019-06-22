import os 
import json
from adapt.engine import IntentDeterminationEngine

class Engine:
<<<<<<< HEAD
    eng = None   # engine object (singleton)
    skills = []  # list of skills
    mapper = {}  # maps intents to functions
=======
    eng = None  # engine object (singleton)
    skills = [] # list contains Skill objects
    handlers = [] # contains a list of Handlers
>>>>>>> 798b7037805111a35b5be29c523dae41fb62fefb
     
    def __init__(self):
        if not Engine.eng: # if not None means if not initialized
            self.eng = IntentDeterminationEngine()
<<<<<<< HEAD
            for folder in os.listdir("skills"):
                if not folder.startswith("Daleelah_"): continue
                self.skills.append(__import__("skills." + folder, fromlist=['']) )
=======
            self.__loadSkills()     
            self.__loadHandlers()   
>>>>>>> 798b7037805111a35b5be29c523dae41fb62fefb
            self.__registerEngEntities()
            self.__registerEngIntents()


    
    def __loadSkills(self):
        """
            Dynamically loads (imports) all the skills located in the folder Skills
        """
        for folder in os.listdir("skills"):
            if not folder.startswith("Daleelah_"): continue # To avoid any other folder not related to the skills
            module = __import__("skills." + folder, fromlist=['']) # import a skill module
            self.skills.append( getattr(module, "getSkill")() ) # getting a skill object
        
        print(str(len(self.skills)), " skills has been loaded") 

    def __registerEngEntities(self):
        """ 
            Collects all entities from all skills and register them in the engine
        """
        entities = {}
        for skill in self.skills:
<<<<<<< HEAD
            entities.update(getattr(skill, "getEntities")())
=======
            entities.update( skill.getEntities )
>>>>>>> 798b7037805111a35b5be29c523dae41fb62fefb

        for entity, keywords in entities.items():
            for keyword in keywords:
                self.eng.register_entity(keyword, entity)
    
<<<<<<< HEAD
    def __registerEngIntents(self):
        for skill in self.skills:
            for intent in getattr(skill, "getIntents")():
                 self.eng.register_intent_parser(intent)
=======
>>>>>>> 798b7037805111a35b5be29c523dae41fb62fefb
    
    def __loadHandlers(self):
        """ 
            Collects all handlers from Skill modules
        """
        for skill in self.skills:
<<<<<<< HEAD
            self.mapper.update(getattr(skill, "getMap")())

    def compute(self, txt):
        for intent in self.eng.determine_intent(txt):
            if intent.get('confidence') > 0:
                self.mapper.get(intent.get('intent_type') ) ()
                print(json.dumps(intent, indent=4))
=======
            self.handlers += ( skill.getMap )
        
        print(str(len(self.handlers)), " handlers has been loaded")


    def __registerEngIntents(self):
        """ 
            Collects all intents and register them in the engine
        """
        for handler in self.handlers :
                self.eng.register_intent_parser(handler.intent)
    
    def __getCorrectIntents(self, txt):
        """
        Given a natrual text, returns a list of intents that match the text
        Args:
            txt(String): The text to be understood.
        Returns:
            list: The intents that match a text with a confidence > 0
        """
        return [
            intent 
            for intent in self.eng.determine_intent(txt) 
            if intent.get('confidence') > 0 ] or None

    def __getCorrectHandler(self, correct_intent):
        print(correct_intent)
        """
        Given a correct intent searches and returns the handler of that intent
        Args:
            correct_intent(intent): an intent to be matched with a handler
        Returns:
            handler: the matched handler with a specific intent
        """
        return next( h for h in self.handlers 
        if h.intent.name == correct_intent["intent_type"] )

    def compute(self, txt):
        """
            Given a txt(String) finds the best intent and execute its function

            Args:
                txt(String): The text to be understood
            Returns:
                String: The answer of the text based on an intent
        """
        correct_intenets = self.__getCorrectIntents(txt) # gets the intents that matches the text
        if correct_intenets: # if there is intents that matches the user's text
            best_intent = max(correct_intenets, key=lambda intent: intent['confidence']) # gets the highest intent
            best_intent_handler = self.__getCorrectHandler(best_intent)
            best_intent_handler.execute() # running handler's function
            print(json.dumps(best_intent, indent=4))
        else:
            #TODO: handle unhandeled text, maybe search in duckduckgo or something
            print("I DO NOT UNDERSTAND")
>>>>>>> 798b7037805111a35b5be29c523dae41fb62fefb


if __name__ == "__main__":
    e = Engine()
<<<<<<< HEAD
    e.compute("What is the weather in Tokyo? ")

=======
    e.compute("What is the weather in Tokyo ?")
    
    
>>>>>>> 798b7037805111a35b5be29c523dae41fb62fefb
