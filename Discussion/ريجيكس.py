import re

#Check if the string starts with "The" and ends with "Spain":

#txt = "hello The rain in Spain JolieJolieJolie a f f s Spain Spain"
txt = 'The Jolie Jolie Spain'
x = re.findall("The (Jolie)* Spain", txt)
y = re.search("The.*(Jolie )*Spain", txt)




if (x or y):
  print('findall:')
  print(x)
  print('search:')
  print(y)
  print("YES! We have a match!")
else:
  print("No match")
