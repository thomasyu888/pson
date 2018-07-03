import pandas as pd
import subprocess
import synapseclient
import os
syn = synapseclient.login()

gse = pd.read_csv("GSEstudies.csv",header=None)

for i in gse[0]:
	datasets = i.replace(" ","").split(",")
	for data in datasets:
		print("\n\n\n\n\n" + data + "\n\n\n\n\n")
		command = ['Rscript','get-geo-annotations.R','--gse=%s' % data.split("=")[1], '--output-file=%s-geo-metadata.tsv' % data.split("=")[1]]
		try:
			subprocess.check_call(command)
			syn.store(synapseclient.File('%s-geo-metadata.tsv' % data.split("=")[1], parentId = "syn12972855"))
		except Exception as e:
			print("ERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERROR\n")
			print(e)