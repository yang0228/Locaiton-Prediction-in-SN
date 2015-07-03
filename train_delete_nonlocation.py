#	file: train_retrieve.py
#	team: M&Y
#	team members: Qingyang Hong(629379), Anchalee Laiprasert(617544)
#	Purpose: delete training data records with latitude, lon are 0.0

import csv
import re

with open('train_delete_nonlocation.csv', 'wb') as train_re, open('posts-train.txt', 'rb') as train:
	spamwriter = csv.writer(train_re, delimiter=',',
		quotechar='|', quoting=csv.QUOTE_MINIMAL)
	reader = csv.reader(train, delimiter=',')
	for row in reader:
		if float(row[4])!=0.0 and float(row[5])!=0.0:
			spamwriter.writerow(row)
train_re.close()
train.close()