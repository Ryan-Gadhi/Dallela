from adapt.intent import IntentBuilder

# what is the closest offset well
# where is the closest offset well

begin_keywords = [  # list of key words
    'what',
    'where',
    'how',
    'who'
]

middle_keywords = [
    'number',
    'count',
    'many'  # how + many
]

active_keywords = [
    'active',
    'live',
    'current'
]

last_keywords = [
    'rig',
    'well',
    'jobs'
]

ignored_regex_keywords = ['{} (?P<Ignored>.*)'.format(keyword)
                       for keyword in last_keywords]


active_intent = IntentBuilder('LocationNatureIntent')\
    .optionally('Begin')\
    .require('Middle')\
    .require('Adjective')\
    .require('Last')\
    .optionally('Ignored')\
    .build()


entities = {  # making a dic for entities
  'Begin': begin_keywords,
  'Middle': middle_keywords,
    'Last': last_keywords,
    'Adjective' : active_keywords
}
multi_regex_entities = [ignored_regex_keywords]

intents = [active_intent]  # adding intent to a new list

name = ['active']

def sql():
    sql_query = 'Select Middle from Last'

