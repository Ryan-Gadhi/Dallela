import json, os, random, sys
from abc import ABC, abstractmethod
from adapt.intent import IntentBuilder
""" this module contains Handler, Skill, Answer  classes and basic loading functions """

def load_raw_intents(path):
    """
        Retrive all json intents within a skill & returns a list of raw intent objects
        Args:
            path(str): path to the intent folder
        Returns:
            list: unprocessed json object intents
    """
    #TODO: handle file errors
    raw_intents = []
    intents_folder = os.path.join(path, "intents") # skill_path/intents

    for f in os.listdir(intents_folder):
        if not f.endswith(".json") : continue # if file is not json then skip
        json_path = os.path.join(intents_folder, f)

        with open( json_path ) as jsonFile:
            raw_intent = json.loads( jsonFile.read() )
            raw_intents.append(raw_intent)
    return raw_intents
    



def add_entity_to_intent(intent, entity_name, importance):
        #TODO: finding a way to write this in a clean way!
        if importance == "require":
                intent.require(entity_name)
        elif importance == "one_of":
                intent.require(entity_name)
        else:
                intent.optionally(entity_name)

def load_entities(intent, entities):
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
            add_entity_to_intent(intent, entity_name, entity_importance)
    return entities_map
                
def load_regex_entities(intent, reg_entities):
    """
    given an intent and a list of reg_entities register them in that intent
    and apply the regex to a list of strings 
    Args:
        intent(intent): the unbuilt intent
        reg_entities(list): containing a list of reg_entities JSON objects
    Returns: (list): of parsed regex strings 
    """
    if not reg_entities: return []
    for reg_entity in reg_entities:
       
        apply_to = reg_entity.get("apply_to", []) #e.g: at, in, around
        entity_name = reg_entity.get("entity_name") #e.g: Location
        reg_pattren = reg_entity.get("regex_pattren") #e.g: .*
        entity_importance = reg_entity.get("importance") #e.g: require
        reg_pattren_named = '(?P<{}>{})'.format(entity_name, reg_pattren) #e.g: (?P<Location>.*)
        
        add_entity_to_intent(intent, entity_name, entity_importance)
        
        joined_entities = [kwd + reg_pattren_named for kwd in apply_to] #e.g: in (?P<Location>.*), at (?P<Location>.*)...

    return joined_entities

class Answer(ABC):
    """
    Abstract class used to handle answers
    """
    def __init__(self, answers=[]):
        self.answers = answers
    
    def format_response(self, response):
        """ 
        randomely chooses a template and subtitute the response (variables) into that template
        variables could be a function output or user's captured keywords
        Args:
            response(dict): dictionary contains variables along with their names
        Returns:
            (str): a randomly generated response based on some variables (if any)
        """
        random_template = random.choice(self.answers) #e.g: 'The weather in {location} is {deg}{unit}' 
        print(response)
        return random_template.format(**response) #format is a python function, google that for more info


class Handler(ABC):
    """
    Abstract class used to glue an intent, its function and the answers
    """
    def __init__(self, intent, answer=None, func=None,):
        self.intent = intent
        self.func = func
        self.answer = answer
    
    def execute(self, response):
        """
            Executes the predefined function associated with an intent 
        """
        if self.func:
            func_output = self.func(response) 
            response.update(func_output) # update user info with function info, to pass it to answer
        print(
        self.answer.format_response(response)
        )

        

class Skill(ABC):
    """
    Abstract class for a skill, providing common methods and behavior to all the skills
    """
    def __init__(self, entities=None, regex_entities=None, handlers=None, skill_name=None):

        """
        Constructor

        Args:
            skill_name(str): name of the skill
            handlers(list): list of handlers used in that skill
            entities(dict): name of an entity that maps with a list of keywords 
            regex_entities(list)
        """
        self.skill_name = skill_name or self.__class__.__name__
        self.entities = entities or {}
        self.regex_entities = regex_entities or []
        self.handlers = handlers or []
        self.__initilaize()
        
    def __initilaize(self):
        """
            loads and instantiate all intents from a json file
        """
        path = os.path.dirname(sys.modules[self.__class__.__module__].__file__ ) #absoulute path for a child class
        raw_intents = load_raw_intents(path)
        for raw_intent in raw_intents:
            intent = IntentBuilder( raw_intent.get("name") )
            self.entities.update( load_entities(intent, raw_intent.get('entities', None)) )  
            self.regex_entities += load_regex_entities( intent, raw_intent.get("regex_entities", []) )
            self.handlers.append( Handler( 
                intent.build(), 
                Answer( raw_intent.get("answers", None) )
                 ) )

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
    


    

