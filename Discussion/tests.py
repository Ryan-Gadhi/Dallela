
text = 'what is the closest offset wellwhat is the closest offset wellwhat is the closest offset wellwhat is the closest offset wellwhat is the closest offset wellwhat is the closest offset wellwhat is the closest offset wellwhat is the closest offset wellwhat is the closest offset well'


words = text.split()
temp = ''
limit = 5
if len(words) > limit:
    i = 0
    for word in words:
        if(i< limit):
            temp += " " + word
        else:
            temp += '\n'
            i=0
        i+=1
else:
    temp = text

print(temp)