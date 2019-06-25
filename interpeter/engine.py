import os 
import json
from adapt.engine import IntentDeterminationEngine

class Engine:
    eng = None  # engine object (singleton)
    skills = [] # list contains Skill objects
    handlers = [] # contains a list of Handlers
     
    def __init__(self):
        if not Engine.eng:
            self.eng = IntentDeterminationEngine()
<<<<<<< HEAD
            self.__loadSkills()     
            self.__loadHandlers()   
            self.__registerEngEntities()
            self.__registerEngIntents()
||||||| merged common ancestors
<<<<<<<<< Temporary merge branch 1
            for folder in os.listdir("skills"):
                if not folder.startswith("Daleelah_"): continue
                self.skills.append(__import__("skills." + folder, fromlist=['']) )
||||||||| merged common ancestors
            for folder in os.listdir("skills"):
                if not folder.startswith("Daleelah_"): continue
                self.skills.append( __import__("skills." + folder, fromlist=['']) )
=========
            self.__loadSkills()     
            self.__loadHandlers()   
>>>>>>>>> Temporary merge branch 2
            self.__registerEngEntities()
            self.__registerEngIntents()
=======
            self.__load_skills()     
            self.__load_handlers()   
            self.__register_eng_entities()
            self.__register_eng_intents()
>>>>>>> abdo


    
    def __load_skills(self):
        """
            Dynamically loads (imports) all the skills located in the folder Skills
        """
        
        for folder in os.listdir("skills"):
            if not folder.startswith("Daleelah_"): continue # To avoid any other folder not related to the skills
            print("skills." + folder)
            module = __import__("interpeter.skills." + folder, fromlist=['']) # import a skill module
            self.skills.append( getattr(module, "getSkill")() ) # getting a skill object
       
        print(str(len(self.skills)), " skills has been loaded") 

    def __register_eng_entities(self):
        """ 
            Collects all entities from all skills and register them in the engine
        """
        entities = {}
        reg_entities = []
        for skill in self.skills:
            entities.update( skill.getEntities )
<<<<<<< HEAD
||||||| merged common ancestors
>>>>>>>>> Temporary merge branch 2
=======
            reg_entities += skill.getRegexEntities

        for reg_entity in reg_entities:
            self.eng.register_regex_entity(reg_entity)
>>>>>>> abdo

        for entity, keywords in entities.items():
            for keyword in keywords:
                self.eng.register_entity(keyword, entity)
    
    
    def __load_handlers(self):
        """ 
            Collects all handlers from Skill modules
        """
        for skill in self.skills:
            self.handlers += ( skill.getMap )
        print(str(len(self.handlers)), " handlers has been loaded")


    def __register_eng_intents(self):
        """ 
            Collects all intents and register them in the engine
        """
        for handler in self.handlers :
                self.eng.register_intent_parser(handler.intent)
    
    def __get_correct_intents(self, txt):
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

    def __get_correct_handler(self, correct_intent):
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
        correct_intenets = self.__get_correct_intents(txt) # gets the intents that matches the text
        if correct_intenets: # if there is intents that matches the user's text
            best_intent = max(correct_intenets, key=lambda intent: intent['confidence']) # gets the highest intent
            best_intent_handler = self.__get_correct_handler(best_intent)
            return best_intent_handler.execute(best_intent) # running handler's function
            # print(json.dumps(best_intent, indent=4))

        else:
            #TODO: handle unhandeled text, maybe search in duckduckgo or something
            print("I DO NOT UNDERSTAND")
<<<<<<< HEAD
||||||| merged common ancestors
>>>>>>>>> Temporary merge branch 2
=======
            return None
>>>>>>> abdo


if __name__ == "__main__":
    e = Engine()
<<<<<<< HEAD
    e.compute("What is the weather in Tokyo ?")
||||||| merged common ancestors
<<<<<<<<< Temporary merge branch 1
    e.compute("What is the weather in Tokyo? ")

||||||||| merged common ancestors
    e.compute("What is the weather in Dammam ? ")
    
    
=========
    e.compute("What is the weather in Tokyo ?")
=======
    print( e.compute("how many active services with bhge ?") )



>>>>>>> abdo
    
    
