

weather_keyword = [
    "What",
    "How",
    "rig"
]



for wk in weather_keyword:
    engine.register_entity(wk, "WeatherKeyword")

weather_types = [
    "closest",
    "sunny",
    "wind",
    "sleet",
    "sun"
]

for wt in weather_types:
    engine.register_entity(wt, "WeatherType")

locations = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]

for loc in locations:
    engine.register_entity(loc, "Location")

weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .build()


engine.register_intent_parser(weather_intent)

hello_keyword = [
    "hello world",
    "hello",
    "rig"
]

for hk in hello_keyword:
    engine.register_entity(hk, "HelloKeyword")


hello_intent = IntentBuilder("HelloIntent")\
    .require("HelloKeyword")\
    .build()

engine.register_intent_parser(hello_intent)

intent_dict = {
    "HelloIntent" : helloFun,
    "WeatherIntent" : weatherFun
}

if __name__ == "__main__":
    for intent in engine.determine_intent(' '.join(sys.argv[1:])) :
        if intent.get('confidence') > 0:
            intent_dict.get(intent.get('intent_type'))()
            print(json.dumps(intent, indent=4))

