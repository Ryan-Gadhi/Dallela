import json

with open('sampleQuery.json') as file:
	data = file.read()
	data = json.loads(data)
	print(data['rowCount'])

	# for row in data['rows']:
	# 	print(row['index'])

	row1 = data['rows'][0]
	#print(row1)
	print(row1['ProdLine'])


