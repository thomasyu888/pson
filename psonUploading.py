gseMetadata = "GSE89107-metadata.tsv"
parentId = "syn12576666"

## Read in the metadata extracted from GEO above.
tsv <- read.table(gseMetadata, sep="\t", header=TRUE, comment.char = "")

## Extract the GEO accession number and URL from the GEO metadata.
new.tsv <- tsv[,c("geo_accession", "url")]

## Handle requirements of sync_manifest.py:
## (1) the column holding the URL must be called path to be recognized by sync_manifest.py
## (2) synapseStore should be FALSE to indicate we are linking to URLs rather than uploading files
## (3) parent should be the Synapse ID of the container in Synapse that will hold the links.  Here we will
##     use a container called bulk-upload-annotation (Synapse ID: syn10002942)
## (4) used should indicate any input data used to derive the annotations.  We will ignore by setting to NA.
## (5) executed should indicate any scripts/binaries/etc used to derive the annotations.  We will ignore by setting to NA.
colnames(new.tsv) <- c("geo_accession", "path")
new.tsv$synapseStore <- "FALSE"
new.tsv$parent <- parentId
new.tsv$used <- NA
new.tsv$executed <- NA

## Extract the specimen ID and cell type from the GEO metadata.
new.tsv$specimenID <- unlist(lapply(tsv$characteristics_ch1, function(x) gsub(".*subject: (.+)", "\\1", x)))
new.tsv$cellType <- unlist(lapply(tsv$characteristics_ch1, function(x) gsub(".*tissue: ([^;]+).*", "\\1", x)))

## Fill in a bunch of annotations based on our understanding of the data and reading of the manuscript
new.tsv$assay <- "rnaSeq"
new.tsv$runType <- "pairedEnd"
## These data use the Ovation library, which is not stranded.
new.tsv$isStranded <- FALSE
new.tsv$dataSubtype <- "raw"
new.tsv$dataType <- "geneExpression"
new.tsv$readLength <- 150
new.tsv$consortium <- "CSBC"
new.tsv$fileFormat <- "fastq"
new.tsv$platform <- "HiSeq4000"
new.tsv$species <- "Human"
new.tsv$tumorType <- "Acute Myeloid Leukemia"
new.tsv$isCellLine <- grepl(new.tsv$specimenID, pattern="line")
new.tsv$isPrimaryCell <- !new.tsv$isCellLine
new.tsv$fileName <- rep(NA, nrow(new.tsv))
new.tsv$tumorType <- "Acute Myeloid Leukemia"
is.engrafted <- grepl(pattern="engrafted", new.tsv$cellType, ignore.case=TRUE)
new.tsv$transplantationType <- rep(NA, nrow(new.tsv))
new.tsv$transplantationDonorSpecies <- rep(NA, nrow(new.tsv))
## The transpnantation donor tissue is always AML Blasts
new.tsv$transplantationDonorTissue <- rep(NA, nrow(new.tsv))
new.tsv$transplantationType[is.engrafted] <- "xenograft"
new.tsv$transplantationDonorSpecies[is.engrafted] <- "Human"
new.tsv$transplantationDonorTissue[is.engrafted] <- "Blast"
## Let's remove "cell line" from the specimenID
new.tsv$specimenID <- unlist(lapply(new.tsv$specimenID, function(x) gsub(" cell line", "", x)))
new.tsv$individualID <- new.tsv$specimenID
## Both of the patients are female
## Just make sure we don't label the cell lines
new.tsv$sex <- rep(NA, nrow(new.tsv))
new.tsv$sex[new.tsv$isPrimaryCell] <- "female"

## There may be multiple ;-delimited URLs per row.  Separate each into a separate row.
final.tsv <- c()
for(i in 1:nrow(new.tsv)) {
    urls <- unlist(strsplit(as.character(new.tsv$path[i]), split=";[ ]*"))
    for(url in urls) {
        row <- new.tsv[i,]
        row$path <- url
        row$fileName <- unlist(lapply(as.character(url), function(x) tail(unlist(strsplit(x, split="/")), n=1)))
        final.tsv <- rbind(final.tsv, row)
    }
}

## Output the re-annotated data
write.table(file="GSE89777-manifest.tsv", final.tsv, sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)