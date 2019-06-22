import json
import os
from abc import ABC, abstractmethod
from adapt.intent import IntentBuilder


def loadRawIntents():
    raw_intents = []
    for f in os.listdir("skills/Daleelah_WeatherSkill/intents/"):
        if not f.endswith(".json") : continue
        with open("skills/Daleelah_WeatherSkill/intents/" + f) as jsonFile:
            raw_intent = json.loads( jsonFile.read() )
            raw_intents.append(raw_intent)
    return raw_intents
    



def addEntityToIntent(intent, entity_name, importance):
        #TODO: finding a way to write this in a clean way!
        if importance == "require":
                intent.require(entity_name)
        elif importance == "one_of":
                intent.require(entity_name)
        else:
                intent.optionally(entity_name)

def loadEntities(intent, entities):
    """
        loads entity names into an intent, and maps the entities to the names 
        Args:
            intent(intent): the intent 
            entities(list[dict]): list of dictionaries contains meta-data about an entity 
        Returns:
            dict: mapping names and content of an entity
    """
    entities_map = {}
    if not entities : return entities_map # if there are no entities then don't continue 
    for entity in entities:
            entity_name = entity.get("name")
            entity_contents = entity.get("contents")
            entity_importance = entity.get("importance")
            
            entities_map.update( {entity_name : entity_contents} )
            addEntityToIntent(intent, entity_name, entity_importance)
    return entities_map
                
def loadRegexEntities(intent, reg_entities):
        #TODO: way to implement this!
        pass

class Handler(ABC):
    """
    Abstract class used to glue an intent, its function and the answers
    """
    def __init__(self, intent, func=None, answer=None):
        self.intent = intent
        self.func = func
        self.answer = answer
    
    def execute(self):
        """
            Executes the predefined function attached to an intent 
        """
        self.func()

    
    def execAnswer(self, *args, **kwargs):
        #TODO: given an output of a function, substitute that output to a predefined answer 
        pass
        

class Skill(ABC):
    """
    Abstract class for a skill, providing common methods and behavior to all the skills
    """
    def __init__(self, entities={}, regex_entities=[], handlers=[], skill_name=None):
        """
        Constructor

        Args:
            skill_name(str): name of the skill
            handlers(list): list of handlers used in that skill
            entities(dict)
            regex_entities(list)
        """
        self.skill_name = skill_name or self.__class__.__name__
        self.handlers = handlers
        self.entities = entities
        self.regex_entities = regex_entities
        self.__initilaize()
        
    def __initilaize(self):
        """
            loads and instantiate all intents from a json file
        """
        raw_intents = loadRawIntents()
        for raw_intent in raw_intents:
            intent = IntentBuilder( raw_intent.get("name") )
            self.entities.update( loadEntities(intent, raw_intent.get('entities', None)) )    
            self.handlers.append( Handler(intent.build()) )

    @property
    def getEntities(self):
        """
        Returns:
                Dict: a list of all entities in that skill
        """
        return self.entities
    
    
 
    @property
    def getRegexEntities(self):
        """
        Returns:
                Dict: a list of all Regular expression entities in that skill
        """
        return self.regex_entities
    
    @property
    def getMap(self):
        """
        Returns:
                list: all the handlers in that skill
        """
        return self.handlers
    


    

