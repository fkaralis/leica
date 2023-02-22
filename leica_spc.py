import xml.etree.ElementTree as ET
import math
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import pathlib

# file handling -- dialog and filename
tkroot = tk.Tk()
tkroot.withdraw()
file_path = filedialog.askopenfilename()
filename = pathlib.Path(file_path).stem

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
		    		rlbpdho = math.tan(float(elem.attrib['RefLineDesignSlopeRatio'])) * rlmso

		    		row["Böschung Verhältnis Neugrad"] = rldsr * 200 / math.pi
		    		row["Böschung Verhältnis aktuell Neugrad"] = math.atan(rlmsho/rlmso) * 200 / math.pi
		    		row["Böschung Höhendifferenz"] = rlbpmsho - rlbpdho
		    		row["Böschung HD Differenz"] = ((rlbpmsho - rlbpdho) * rlmso) / rlbpdho

					# append row dict to punktlist
		    		punktlist.append(row)
# # check Points
# for key in hghthodict:
# 	print(key, hghthodict[key])
# print('\n','------','\n')
# # check ApplicationReflineMeasures
# print(*punktlist, sep = "\n")

# output
df = pd.DataFrame(punktlist, index = punktindexlist) 
df.to_csv(filename + '_Böschung.csv')
# df.to_excel(filename + '_excel.xlsx')
