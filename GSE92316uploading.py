import pandas as pd
import synapseclient
import synapseutils
syn = synapseclient.login()

GSE = "GSE92316"
gseMetadata = "%s-geo-metadata.tsv" % GSE
parentId = "syn12976510"

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


newTsv['tumorType'] = "Adenocarcinoma"

newTsv['assay'] = "rnaSeq"


newTsv['dataSubtype'] = "raw" 
newTsv['dataType'] = "geneExpression"
newTsv['fileFormat'] = "raw"
newTsv['resourceType'] = "experimentalData"

newTsv['cellType'] = "epithelial"
newTsv['diagnosis'] = "Breast Cancer"

newTsv['isCellLine'] = True
newTsv['isPrimaryCell'] = False #Coming from human / animal

newTsv['tissue'] = "mammary gland"
newTsv['organ'] = "breast"


newTsv['species'] = "Human"
newTsv['sex'] = "female"
#Some specimens could come from one individual
newTsv['specimenID'] = tsv['title']
newTsv['individualID'] = [spec.split(" ")[0] for spec in tsv['title']]

newTsv['platform'] = "HiSeq3000" #??

newTsv['consortium'] = "CSBC"
newTsv['fundingAgency'] = "NIH-NCI"

##### ADD supplemental file

supp = tsv[["geo_accession", "supplementary_file_1"]]

## Handle requirements of sync_manifest.py:
## (1) the column holding the URL must be called path to be recognized by sync_manifest.py
## (2) synapseStore should be FALSE to indicate we are linking to URLs rather than uploading files
## (3) parent should be the Synapse ID of the container in Synapse that will hold the links.  Here we will
##     use a container called bulk-upload-annotation (Synapse ID: syn10002942)
## (4) used should indicate any input data used to derive the annotations.  We will ignore by setting to NA.
## (5) executed should indicate any scripts/binaries/etc used to derive the annotations.  We will ignore by setting to NA.
supp.columns = ["geo_accession", "path"]
supp['synapseStore'] = "FALSE"
supp['parent'] = parentId
supp['used'] = float('nan')
supp['executed'] = float('nan')


supp['tumorType'] = "Adenocarcinoma"

supp['assay'] = "rnaSeq"


supp['dataSubtype'] = "processed" 
supp['dataType'] = "geneExpression"
supp['fileFormat'] = "tsv"
supp['resourceType'] = "experimentalData"

supp['cellType'] = "epithelial"
supp['diagnosis'] = "Breast Cancer"

supp['isCellLine'] = True
supp['isPrimaryCell'] = False #Coming from human / animal

supp['tissue'] = "mammary gland"
supp['organ'] = "breast"


supp['species'] = "Human"
supp['sex'] = "female"
#Some specimens could come from one individual
supp['specimenID'] = tsv['title']
supp['individualID'] = [spec.split(" ")[0] for spec in tsv['title']]

supp['platform'] = "HiSeq3000" #??

supp['consortium'] = "CSBC"
supp['fundingAgency'] = "NIH-NCI"

newTsv = newTsv.append(supp)
## Output the re-annotated data
newTsv.to_csv("%s-manifest.tsv" % GSE, sep="\t", index=False)


synapseutils.syncToSynapse(syn, "%s-manifest.tsv" % GSE)
