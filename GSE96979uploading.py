import pandas as pd
import synapseclient
import synapseutils
syn = synapseclient.login()

GSE = "GSE94883"
gseMetadata = "%s-geo-metadata.tsv" % GSE
parentId = 

## Read in the metadata extracted from GEO above.
tsv = pd.read_csv(gseMetadata, sep="\t")

## Extract the GEO accession number and URL from the GEO metadata.
newTsv = tsv[["geo_accession", "url"]]

## Handle requirements of sync_manifest.py:
## (1) the column holding the URL must be called path to be recognized by sync_manifest.py
## (2) synapseStore should be FALSE to indicate we are linking to URLs rather than uploading files
## (3) parent should be the Synapse ID of the container in Synapse that will hold the links.  Here we will
##     use a container called bulk-upload-annotation (Synapse ID: syn10002942)
## (4) used should indicate any input data used to derive the annotations.  We will ignore by setting to NA.
## (5) executed should indicate any scripts/binaries/etc used to derive the annotations.  We will ignore by setting to NA.
newTsv.columns = ["geo_accession", "path"]
newTsv['synapseStore'] = "FALSE"
newTsv['parent'] = parentId
newTsv['used'] = float('nan')
newTsv['executed'] = float('nan')


newTsv['tumorType'] = 

newTsv['assay'] = 


newTsv['dataSubtype'] = 
newTsv['dataType'] = 
newTsv['fileFormat'] = 
newTsv['resourceType'] = 

newTsv['cellType'] = 
newTsv['diagnosis'] = 

newTsv['isCellLine'] = 
newTsv['isPrimaryCell'] =  #Coming from human / animal

newTsv['tissue'] =  
newTsv['organ'] = 


newTsv['species'] = 
newTsv['sex'] = 
#Some specimens could come from one individual
newTsv['specimenID'] = 
newTsv['individualID'] = 

newTsv['platform'] = 

newTsv['consortium'] = 
newTsv['fundingAgency'] = 


## Output the re-annotated data
newTsv.to_csv("%s-manifest.tsv" % GSE, sep="\t", index=False)


synapseutils.syncToSynapse(syn, "%s-manifest.tsv" % GSE)
