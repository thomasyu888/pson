import pandas as pd
import synapseclient
import synapseutils
syn = synapseclient.login()

gseMetadata = "GSE94883-metadata.tsv"
parentId = "syn12685522"

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


newTsv['tumorType'] = "Not Applicable"

newTsv['assay'] = "scrnaSeq"


newTsv['dataSubtype'] = "raw"
newTsv['dataType'] =  "geneExpression"
newTsv['fileFormat'] = "raw"
newTsv['resourceType'] = "experimentalData"

newTsv['cellType'] = "motor neuron"
newTsv['diagnosis'] = "Not Applicable"

newTsv['isCellLine'] = False
newTsv['isPrimaryCell'] = True #Coming from human / animal

newTsv['tissue'] =  "Not Applicable"
newTsv['organ'] = "brain"



newTsv['species'] = "Mouse"
newTsv['sex'] = float('nan')
#Some specimens could come from one individual
newTsv['specimenID'] = tsv['title']
newTsv['individualID'] = [i.split("_")[0] for i in tsv['title']]

newTsv['platform'] = "HiSeq2500" #Create new GAII

newTsv['consortium'] = "PSON"
newTsv['fundingAgency'] = "NIH-NCI"



## Output the re-annotated data
newTsv.to_csv("GSE89107-manifest.tsv", sep="\t", index=False)


synapseutils.syncToSynapse(syn, "GSE89107-manifest.tsv")
