"""
Usage: (python) group3_report1_question7.py <FOLDER PATH>
Finds the longest read for each category using poretools util. 
Winner finds the longest read for forward (template), reverse
(complement), and 2D (2D).
"""

import subprocess
import sys

def findLongest(command):
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc.stdout.readline() # throw away first line
	longest = len(proc.stdout.readline())
	print longest

path = sys.argv[1] # file path for pass reads

# Winner of Complement
print "Longest read for 2D in folder of reads:"
poretools_command = "poretools winner --type 2D " + path
findLongest(poretools_command)