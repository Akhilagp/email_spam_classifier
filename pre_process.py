import sys
import csv
import re

def pre_proc(f):
	s=''
	sub=''
	l=[]
	l_s=''
	filename=f
	with open(filename,'r') as f:
	    r=csv.reader(f)
	    l=list(r)
	sub=l[0][0]+'\n\n'
	del l[0]
	for i in l:
	    if i!=[]:
	        l_s=''
	        for l_i in i:
	            if l_i!='':
	                l_i=re.sub('\n',' ',l_i)
	                l_s=l_s+l_i+' '
	        s=s+l_s+' '
	sub=sub+s
	with open(filename,'w+') as f:
	    f.write("{0}".format(sub))
