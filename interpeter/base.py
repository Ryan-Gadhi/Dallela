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
            raw_intent = json.loads( jsonFile.read() )  # @Ryan raw intent = json file
            raw_intents.append(raw_intent)
    return raw_intents
    



def add_entity_to_intent(intent, entity_name, importance):
        #TODO: finding a way to write this in a clean way!
        if importance == "require":
                intent.require(entity_name)
        elif importance == "one_of":
                intent.one_of(entity_name)
        else:
                intent.optionally(entity_name)

def load_entities(intent, entities):
    """
        loads entity names into an intent, and maps the entities to the names
        @Ryan, loads entity names into an intent, and maps the entities data to the intent

        Args:
            intent(intent): the intent 
            entities(list[dict]): list of dictionaries contains meta-data about an entity 
        Returns:
            dict: mapping names and content of an entity
    """
    entities_map = {}
    if not entities : return entities_map # if there are no entities then don't continue
    for entity in entities:
            entity_name = intent.name + "_" + entity.get("name")
            entity_contents = entity.get("contents")
            entity_importance = entity.get("importance")
            
            entities_map.update( {entity_name : entity_contents} )  # @Ryan, update method for dic
            add_entity_to_intent(intent, entity_name, entity_importance)
    return entities_map # @Ryan, each entity now belongs to an intent
                
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
    joined_entities = []
    for reg_entity in reg_entities:
       
        apply_to = reg_entity.get("apply_to", []) #e.g: at, in, around
        apply_to_right = reg_entity.get("apply_to_right", []) #e.g: at, in, around

        entity_name = intent.name + "_" + reg_entity.get("entity_name") #e.g: intentName_Location
        reg_pattren = reg_entity.get("regex_pattren") #e.g: .*
        entity_importance = reg_entity.get("importance") #e.g: require
        reg_pattren_named = '(?P<{}>{})'.format(entity_name, reg_pattren) #e.g: (?P<intentName_Location>.*)
        
        add_entity_to_intent(intent, entity_name, entity_importance)
        
        joined_entities += [kwd + reg_pattren_named for kwd in apply_to] #e.g: in (?P<Location>.*), at (?P<Location>.*)...
        joined_entities += [reg_pattren_named + kwd for kwd in apply_to_right] #e.g (?P<Duration>\d*) Days, Weeks...
    return joined_entities

class Answer(ABC):
    """
    Abstract class used to handle answers
    @Ryan, violates abstract structure. should be normal class {delete ABC}

    """
    def __init__(self, answers=[]):
        self.answers = answers
    
    def format_response(self, response):
        """ 
        randomly chooses a template and subtitute the response (variables) into that template
        variables could be a function output or user's captured keywords
        Args:
            response(dict): dictionary contains variables along with their names
        Returns:
            (str): a randomly generated response based on some variables (if any)
        """
        random_template = random.choice(self.answers) #e.g: 'The weather in {location} is {deg}{unit}' 
        answer = random_template.format(**response)
        return answer #format is a python function, google that for more info


class Handler(ABC):
    """
    Abstract class used to glue an intent, its function and the answers
    @Ryan, violates abstract structure. should be normal class {delete ABC}
    """
    def __init__(self, intent, answer=None, func=None,):
        self.intent = intent
        self.func = func
        self.answer = answer
    
    def execute(self, response): # @Ryan, response is the Adapt engine output
        """
            Executes the predefined function associated with an intents
            @Ryan, returns one of answers randomly
        """
        # remove the intent name from the beginning of each keyword
        modified_response = {}
        for key, val in response.items():
            original_key = key.replace(self.intent.name + "_", '')
            modified_response[original_key]  = val

        if self.func:
            func_output = self.func(modified_response)
            modified_response.update(func_output) # update user info with function info, to pass it to answer
        else:
            print("NO FUNCTION ?..................")
    


        print(modified_response)
        return( # printable
        self.answer.format_response(modified_response)
        )

        

class Skill(ABC):
    """
    Abstract class for a skill, providing common methods and behavior to all the skills
    @Ryan, violates abstract structure. should be normal class {delete ABC}

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
        
    def __initilaize(self): # @Ryan recom: redundant method. same as __init__
        """
            loads and instantiate all intents from a json file
        """
        path = os.path.dirname(sys.modules[self.__class__.__module__].__file__ ) # absolute path for a child class
        raw_intents = load_raw_intents(path)
        for raw_intent in raw_intents:
            intent = IntentBuilder( raw_intent.get("name") ) # @Ryan, getting json 'name' element, now we have an intent
            self.entities.update( load_entities(intent, raw_intent.get('entities', None)) ) # @Ryan, returns a dic: entites->intent
            self.regex_entities += load_regex_entities( intent, raw_intent.get("regex_entities", []) )
            self.handlers.append( Handler( 
                intent.build(), 
                Answer( raw_intent.get("answers", None) )
                 ) ) # @Ryan, making a new object of Handler to connect intents to answers, fun = None for now

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
    


    

