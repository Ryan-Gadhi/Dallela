from adapt.intent import IntentBuilder
import json

entities_map = {}

def loadJSON():
    with open('WeatherIntent.json') as jsonFile:
        raw_intent = json.loads( jsonFile.read() )
        #print(raw_intent)
        intent = IntentBuilder( raw_intent.get("name") )
        loadEntities(intent, raw_intent.get('entities', None) )
        loadRegexEntities(intent, raw_intent.get('regex_entities', None))
        print(intent)


def addEntityToIntent(intent, entity_name, importance):
        #TODO: finding a way to write this in a clean way!
        if importance == "require":
                intent.require(entity_name)
        elif importance == "one_of":
                intent.require(entity_name)
        else:
                intent.optionally(entity_name)

def loadEntities(intent, entities):
        if not entities : return
        for entity in entities:
                entity_name = entity.get("name")
                entity_contents = entity.get("contents")
                entity_importance = entity.get("importance")
                
                entities_map.update( {entity_name : entity_contents} )
                addEntityToIntent(intent, entity_name, entity_importance)
                
def loadRegexEntities(intent, reg_entities):
        #TODO: way to implement this!
        pass




if __name__ == "__main__":
    loadJSON()

