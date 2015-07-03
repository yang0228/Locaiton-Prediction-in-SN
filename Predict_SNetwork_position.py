#	file: Predict_SNetwork_position.py
#	team members: Qingyang Hong(629379)
#	Purpose: features selection and location prediction
import csv
import re
import sys
import math
from sklearn.neighbors import KNeighborsRegressor

def getTraindata(testId, graph):
	friendary = graphDict[testId]
	x = []
	lat = []
	lon = []
	with open('train_delete_nonlocation.csv', 'rb') as train:
		reader = csv.reader(train, delimiter=',')
		for frd in reader:
			if frd[0] in friendary:
				x.append([float(frd[1]),float(frd[2]),float(frd[3])])
				lat.append(float(frd[4]))
				lon.append(float(frd[5]))
	
	train.close()
	return x,lat,lon


#graph that stores whole social network relationship
graphDict = {} 
tmpFriends = []
# initial nowtesId is the ID of first record in graph.txt, records need to be sorted!!!
nowtestId = 1

with open('graph.txt', 'rb') as graph:
	readergraph = csv.reader(graph, delimiter='\t')
	for row in graph:
		row1 = re.search('^[0-9]+\s',row)
		row2 = re.search('\s[0-9]+',row)

		if nowtestId == row1.group(0).strip():
			tmpFriends.append(row2.group(0).strip())
		else:
			graphDict.update({nowtestId:tmpFriends})
			tmpFriends = [row2.group(0).strip()]
		nowtestId = row1.group(0).strip()
graph.close()



with open('submit_train_retrieved_00.csv', 'wb') as submit, open('posts-test-x.txt', 'rb') as test:
	spamwriter = csv.writer(submit, delimiter=',',
		quotechar='|', quoting=csv.QUOTE_MINIMAL)
	reader = csv.reader(test, delimiter=',')
	for index,value in enumerate(reader):
		latitude = 0.0
		longitude = 0.0
		if index > 0:
			x,lat,lon = getTraindata(value[0], graphDict)
			if len(x) == 0:
				pass
			else:
				latmodel = KNeighborsRegressor(n_neighbors=int(math.sqrt(len(x))))
				lonmodel = KNeighborsRegressor(n_neighbors=int(math.sqrt(len(x))))
				latmodel.fit(x, lat) 
				latitude = latmodel.predict([[value[1],value[2],value[3]]])
				lonmodel.fit(x, lon) 
				longitude = lonmodel.predict([[value[1],value[2],value[3]]])
			spamwriter.writerow([value[0], latitude, longitude])
		else:
			spamwriter.writerow(["IdLatLon"])
submit.close()
test.close()