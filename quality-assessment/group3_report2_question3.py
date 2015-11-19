'''
Usage: python group3_report2_question3.py pathtofast5directory flag
flag can be 2D or 1D
'''

import sys
import os
import datetime
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date

#find the modification date
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

#find the data and make the graph
def makeGraph(path, flag):
	fast5Files = glob(path + '/*.fast5')
	times = []
	if flag=="2D":
		s_type = flag
	else:
		s_type = "fwd,rev"
	for fp in fast5Files:
		#find the base pairs and the modification date for a file
		os.system("poretools stats --type " +s_type+ " " + fp + " > text.txt")
		with open("text.txt", "r") as f:
			if(len(f.readline())!=0):
				times.append(((int(f.readline().split('\t')[1].rstrip('\n'))*2), modification_date(fp)))
	print "creating graph"
	#sort entries by datetime
	times.sort(key=lambda tup: tup[1])
	#split entries into two lists
	nucleotides, timestamp = zip(*times)
	#find the cumulative values of the nucleotides
	c_nuc = np.cumsum(np.asarray(nucleotides))

	#create graph
	fig, ax1 = plt.subplots()
	ax1.plot(np.asarray(timestamp), c_nuc)
	plt.title("Cumulative Nucleotides Over Time")
	plt.ylabel("Cumulative Nucleotides")
	plt.xlabel("Time")
	fig.autofmt_xdate()
	plt.savefig(flag+'.png')

if __name__ == '__main__':
	path = sys.argv[1] #the path to the fast5 directory
	flag = sys.argv[2] #2D or 1D
	makeGraph(path, flag)