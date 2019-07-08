from adapt.intent import IntentBuilder

# what is the closest offset well
# where is the closest offset well

question_begin_keywords = [  # list of key words
    'what',
    'where',
    'how',
    'who'
]

location_keywords = [
    'closest',
    'nearest',
    'furthest'
]

nature_keywords = [
    'rig',
    'well',
    'of sitwell',
    'aramco office'
]

ignored_regex_keywords = ['{} (?P<Ignored>.*)'.format(keyword)
                       for keyword in nature_keywords]


location_nature_intent = IntentBuilder('LocationNatureIntent')\
    .optionally('QuestionBegin')\
    .require('Location')\
    .require('Nature')\
    .optionally('Ignored')\
    .build()


entities = {  # making a dic for entities
  'QuestionBegin': question_begin_keywords,
  'Location': location_keywords,
    'Nature': nature_keywords
}
multi_regex_entities = [ignored_regex_keywords]

intents = [location_nature_intent]  # adding intent to a new list


