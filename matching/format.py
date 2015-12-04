import sys

def method1():
	infile = sys.argv[1]
	outfile = sys.argv[2]
	target = open(outfile, 'w')
	with open(infile, 'r') as fp:
	    for line in fp:
	        data = line.split('\t')
	        reformat = [data[6], data[1], data[2], data[3]+data[4]]
	        new_line = '\t'.join(reformat)
	        new_line = new_line + '\n'
	        target.write(new_line)

def method2():
	infile = sys.argv[1]
	outfile = sys.argv[2]
	target = open(outfile, 'w')
	with open(infile, 'r') as fp:
	    for line in fp:
	        data = line.split('\t')
	        reformat = [data[10][:-1], data[0], data[1], data[3].replace("/","")]
	        new_line = '\t'.join(reformat)
	        new_line = new_line + '\n'
	        target.write(new_line)

method2()