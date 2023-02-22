# version 2.0
# keeps useful ApplicationReflineMeasures (line 38)
# RefLineMeasStkOffset absolute value (line 58)
# working version, not test

import os.path as op
import xml.etree.ElementTree as ET
from math import pi, tan, atan
from pandas import DataFrame as df
from tkinter import Tk, filedialog
from pathlib import Path

# file handling -- dialog and filename
tkroot = Tk()
tkroot.withdraw()
file_path = filedialog.askopenfilename()
filename = Path(file_path).stem

# parse XML file
tree = ET.parse(file_path)
root = tree.getroot()

punktlist = [] 		# list of table rows
punktindex = 0 		# row counter for index column	
punktindexlist = []	# list of indexes
hghthodict = {}		# dictionary [point_id, hghthO]

for child in root:
	if child.tag.endswith('HexagonLandXML'):
	    for elem in child.iter():
	    	
	    	# get all hghthO's in highthodict, key: uniqueID
	    	if elem.tag.endswith('Point'):
	    		for subelem in elem.iter():
	    			if subelem.tag.endswith('Grid'):
	    				hghthodict[elem.attrib['uniqueID']] = subelem.attrib['hghthO']
	    	
	    	# build punktlist, row by row
	    	if elem.tag.endswith('ApplicationReflineMeasure'):
	    		if 'Line' in elem.attrib['RefLine_ID']:		# keep only usefull ApplicationReflineMeasures 
		    		punktindex += 1
		    		punktindexlist.append(punktindex)
		    		row = {}

		    		# original table vars
		    		punktid = elem.attrib['RefLineMeasPointID']
		    		hoehe = float(hghthodict[punktid])		# connect ApplicationReflineMeasures with Points
		    		linie = elem.attrib['RefLine_ID']
		    		dist_entlang_linie = float(elem.attrib['RefLineMeasStkChainage'])

		    		row["Punkt"] = punktid 
		    		row["Höhe"] = hoehe
		    		row["Linie"] = linie
		    		row["Dist. entlang Linie"] = dist_entlang_linie

		    		# calculated table vars
		    		rldsr = float(elem.attrib['RefLineDesignSlopeRatio'])
		    		rlmsho = float(elem.attrib['RefLineMeasStkHtOffset'])
		    		rlmso = abs(float(elem.attrib['RefLineMeasStkOffset']))
		    		rlbpmsho = hoehe - float(elem.attrib['RefLineBasePointHeight'])
		    		rlbpdho = tan(float(elem.attrib['RefLineDesignSlopeRatio'])) * rlmso

		    		row["Böschung Verhältnis Neugrad"] = rldsr * 200 / pi
		    		row["Böschung Verhältnis aktuell Neugrad"] = atan(rlmsho/rlmso) * 200 / pi
		    		row["Böschung Höhendifferenz"] = rlbpmsho - rlbpdho
		    		row["Böschung HD Differenz"] = ((rlbpmsho - rlbpdho) * rlmso) / rlbpdho

					# append row dict to punktlist
		    		punktlist.append(row)
		    		
# # check Points
# for key in hghthodict:
# 	print(key, hghthodict[key])
# 
# print('\n','------','\n')

# # check ApplicationReflineMeasures
# print(*punktlist, sep = "\n")

# output
def uniquify(path):
    filename, extension = op.splitext(path)
    counter = 1

    while op.exists(path):
        path = filename + "-" + str(counter) + extension
        counter += 1

    return path

df = df(punktlist, index = punktindexlist) 
try:
    df.to_csv(filename + '_Böschung.csv', mode='x')
except FileExistsError:
    df.to_csv(uniquify(filename + '_Böschung.csv'))


