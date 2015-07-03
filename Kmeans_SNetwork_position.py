#	file: Kmeans_SNetwork_position.py
#	team members: Qingyang Hong(629379)
#	Purpose: features selection and location prediction
import csv
import re
import sys
import math
from sklearn.cluster import KMeans

def getTraindata(testId, graph):
	friendary = graphDict[testId]
	position = []
	with open('train_delete_nonlocation.csv', 'rb') as train:
		reader = csv.reader(train, delimiter=',')
		for frd in reader:
			if frd[0] in friendary:
				position.append([float(frd[4]),float(frd[5])])
	
	train.close()
	return position


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
			position = getTraindata(value[0], graphDict)
			if len(position) < 4 and len(position) > 0:
				for pos in position:
					latitude+=pos[0]
					longitude+=pos[1]
				latitude /= len(position)
				longitude /= len(position)
			elif len(position) <= 0:
				pass
			else:
				kmeans = KMeans(n_clusters=4)
				kmeans.fit(position)
				clustersDict = {}
				for pos in position:
					pred = kmeans.predict(pos)
					if clustersDict.has_key(pred[0]) == True:
						tmpLocList = clustersDict[pred[0]]
						tmpLocList.append(pos)
						clustersDict.update({pred[0]:tmpLocList})
					else:
						clustersDict[pred[0]] = [pos]

				mostFriendsCluster = 0
				maxfriendsCount = 0
				for key, loca in clustersDict.iteritems():
					if len(loca) > maxfriendsCount:
						maxfriendsCount = len(loca)
						mostFriendsCluster = key

				for pos in clustersDict[mostFriendsCluster]:
					latitude+=pos[0]
					longitude+=pos[1]
				latitude /= len(clustersDict[mostFriendsCluster])
				longitude /= len(clustersDict[mostFriendsCluster])

			spamwriter.writerow([value[0], latitude, longitude])
		else:
			spamwriter.writerow(["Id,Lat,Lon"])
submit.close()
test.close()