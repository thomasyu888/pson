import synapseclient
syn = synapseclient.login()
synProjectId = "syn7349742"
name = "Temp Project 1"
studyName = "Nora-2017"

geoProjectEnt = syn.store(synapseclient.Folder(name, parentId = synProjectId))
dataEnt = syn.store(synapseclient.Folder("Data", parentId = geoProjectEnt.id))
publicationsEnt = syn.store(synapseclient.Folder("Publications", parentId = geoProjectEnt.id))
studyEnt =  syn.store(synapseclient.Folder(studyName, parentId = publicationsEnt.id))
samplesEnt = syn.store(synapseclient.Folder("Samples", parentId = geoProjectEnt.id))
toolsEnt = syn.store(synapseclient.Folder("Tools", parentId = geoProjectEnt.id))

print(studyEnt.id)

# **Reference**

#Title
#Authors
#[Journal/Publishing dat](Link)
 
# **Abstract**

