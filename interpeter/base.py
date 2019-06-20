from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Abstract class used to glue an intent, its function and the answers
    """
    def __init__(self, intent, func, answer):
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
    Abstract class for a skill, providing common methods and behavriour to all the skills
    """
    def __init__(self, handlers, entities, regex_entities, skill_name=None):
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
    


    

