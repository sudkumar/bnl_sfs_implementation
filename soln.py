#!/usr/bin/python

import time
import math



class Tuples():
	"""Handles Tuples"""
	# get the global dimension for skylines
	global dimensions
	# initialize the tuple
	def __init__(self, tupleItem, timeStamp):
		self.tuple = tupleItem[1:]
		self.id = int(tupleItem[0])
		self.timeStamp = timeStamp

	# compare the time stamp	
	def compareTimeStamp(self, tupleItem):
		return self.timeStamp < tupleItem.timeStamp

	# compare for the full values for the tuple	
	def campareFull(self, inputTuple):
		global comparisions
		comparisions += 1
		isLess = isGreater = False
		for dim in dimensions:
			if self.tuple[dim-1] <= inputTuple.tuple[dim-1]:
				isLess = True
			else:
				isGreater = True

		if isLess and not isGreater:
			# inputTuple is dominated	
			return 0
		elif (isGreater and not isLess):
			# currTuple is dominates
			return 1
		else:
			# no relations between them
			return 2
				
								
			

class Window():
	"""This class handles for window operations"""
	def __init__(self, size):
		self.size = size
		self.objects = [];

	def add(self, tupleItem):
		tupleItem.timeStamp = time.clock()
		self.objects.append(tupleItem);		

	def isFull(self):
		return len(self.objects) >= self.size	

	def remove(self, obj):
		self.objects.remove(obj)

	# compare full tuples and return 
	# true, if tupleObject is dominated 	
	# false, if we have to insert the tupleObject in the window	
	def removeLessTime(self, tupleObject):
		skylines = []
		i = 0
		while i < len(self.objects):
			obj = self.objects[i]
			isBefore = obj.compareTimeStamp(tupleObject)
			if(isBefore):
				# obj is before the tupleObject
				# so remove it from the window and print it
				self.remove(obj)
				skylines.append(obj)
				# print str(obj.id)+"\t"+'\t'.join(map(str, obj.tuple))
				i -= 1
			i += 1	
		return skylines
	# compare full tuples and return 
	# true, if tupleObject is dominated 	
	# false, if we have to insert the tupleObject in the window
	def removeDominated(self, tupleObject):
		i = 0
		while i < len(self.objects):
			obj = self.objects[i]
			campResult = obj.campareFull(tupleObject)
			if(campResult == 0):
				# obj dominates the tupleObject
				return True
			elif (campResult == 1):
				# tupleObject dominates the obj
				# so remove the current window element
				self.remove(obj)
				i -= 1
			i += 1
		return False			



def BNL(inputFileObject):
# start the BNL algorithm
	skylines = []
	tmpOutputFile = open('tmpOutPutFile0.txt', 'w')
	for eachLine in inputFileObject:
		inputTuple = Tuples( map(float, eachLine.split()), time.clock())
		if(not window.removeDominated(inputTuple)):
			# we need to add the current item
			if(not window.isFull()):
				# now compare with window elements and add if necessary 
				window.add(inputTuple)	
			else:
				# window is full, so put it into a tmp file
				printLine = str(inputTuple.timeStamp)+"\t"+str('\t'.join(eachLine.split()))+"\n"
				tmpOutputFile.write(printLine)	
	tmpOutputFile.close()

	# now get the elements from temporary file
	# temOutputFile will contain the next input from which we want to read
	tmpOutputFile = open('tmpOutPutFile0.txt', 'r')
	first_char = tmpOutputFile.read(1) #get the first character
	i = 1
	if first_char:
		tmpOutputFile.seek(0) #first character wasn't empty, return to start of file.
		# tempOutputFile1 will be out holder for data for next interation
		tmpOutputFile1 = open('tmpOutPutFile'+str(i)+'.txt', 'w')
		for eachLine in tmpOutputFile:
			line = eachLine.split()
			# parse the line to get id, timeStamp, tupleData
			timeStamp = float(line[0])
			tupleData = map(float, line[1:])	
			inputTuple = Tuples(tupleData, timeStamp)

			# now remove element from window which have less time stamp
			skylines  = skylines +  window.removeLessTime(inputTuple)

			# now iterate in window for dominance
			if(not window.removeDominated(inputTuple)):
				# we need to add this element to window
				window.add(inputTuple)
			else:
				printLine = str(inputTuple.timeStamp)+"\t"+str('\t'.join(eachLine.split()))+"\n"
				tmpOutputFile1.write(printLine)
		tmpOutputFile1.close()
		tmpOutputFile.close()
		tmpOutputFile = open('tmpOutPutFile'+str(i)+'.txt')
		i = (i+1) % 2
		# temOutputFile will contain the next input from which we want to read
		first_char = tmpOutputFile.read(1)
	tmpOutputFile.close()
	# print the window at last

	for obj in window.objects:
		skylines.append(obj)
	# close the necessary files
	tmpOutputFile.close()
	return skylines
######## END OF BNL FUNCTION


def SFS(inputFileObject):
	data = []
	for line in inputFileObject:
		attrs = map(float, line.split())
		attrs[0] = int(attrs[0])
		tuples = attrs[1:]
		entropy = 0
		# calculate the entropy
		for dimn in dimensions:
			entropy += math.log(tuples[dimn-1])

		data.append([attrs, entropy])	
	data.sort(key=lambda item: item[1])
	
	sfsFile = open("sfs.txt", "w")
	for row in data:
		sfsFile.write(" ".join(map(str, row[:-1][0]))+"\n")
	sfsFile.close()

	# read from output of sfs file for BNL
	sfsFile = open("sfs.txt", "r")
	skylines = BNL(sfsFile)
	sfsFile.close()
	return skylines

def printSkylins(skylines):
	for skyline  in skylines:
		print str(skyline.id)

queryFile = raw_input("Enter the query file name: ") or "query1.txt"
sampleData = raw_input("Enter the data file name: ") or "sample1.txt"

# take the sample query
# extract the first line and get the dimensions
queryData = open(queryFile, 'r')
i = 0
for line in queryData:
	if i == 0:
		dimensions = map(int, line.split())
	if i == 1:
		window_size = int(line.split()[0])
	i= i + 1		
# create a window object of tuples with with a size of window_size
window = Window(window_size);


# Take the input file
inputData = open(sampleData, 'r')

# run the bnl algorithm
comparisions = 0
startTime = time.time()
skylines = BNL(inputData)
print "Time by SFS: "+ str((time.time()  - startTime)*1000)+"ms"
print "Number of skylines: "+ str(len(skylines))
# printSkylins(skylines)
print "comparisions: "+ str(comparisions)
print "\n"
inputData.close()

inputData = open(sampleData, 'r')
window = Window(window_size);
# run SFS algorithm
comparisions = 0
startTime = time.time()
skylines =SFS(inputData)
print "Time by SFS: "+ str((time.time()  - startTime)*1000)+"ms"
print "Number of skylines: "+ str(len(skylines))
# printSkylins(skylines)
print "comparisions: "+ str(comparisions)

inputData.close()