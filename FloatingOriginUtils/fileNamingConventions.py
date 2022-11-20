def updateName(objName='', objectName=None, objectIndex=None, setIndex=None, internal=None, collider=None, modifiers=None, lodIndex=None, shapeKey=None):
    newName = ''

    if objectName:
        newName += objectName
    else:
        fromName = getFromName(objName, "OBJECT_NAME")
        if fromName:
            newName += fromName
    
    if setIndex:
        newName += '_set' + str(setIndex)
    else:
        fromName = getFromName(objName, "SET_INDEX")
        if fromName:
            newName += '_set' + str(fromName)
    
    if objectIndex:
        newName += '_' + str(objectIndex)
    else:
        fromName = getFromName(objName, "OBJECT_INDEX")
        if fromName:
            newName += '_' + str(fromName)
    
    if internal:
        newName += '_internal'
    if internal==None:
        fromName = getFromName(objName, "INTERNAL")
        if fromName:
            newName += '_internal'
    
    if collider:
        newName += '_collider'
    if collider==None:
        fromName = getFromName(objName, "COLLIDER")
        if fromName:
            newName += "_collider"
    
    if modifiers:
        newName += '_modifiers'
    if modifiers==None:
        fromName = getFromName(objName, "MODIFIERS")
        if fromName:
            newName += "_modifiers"
    
    if lodIndex or lodIndex == 0:
        if (0 <= lodIndex < 10):
            newName += '_lod' + str(lodIndex)
    else:
        fromName = getFromName(objName, "LOD")
        if fromName and 0 <= fromName < 10:
            newName += '_lod' + str(fromName)

    if shapeKey:
        if shapeKey.lower()=="basis":
            newName += '_' + shapeKey
        else:
            newName += '_blend_' + shapeKey
    if shapeKey==None:
        fromName = getFromName(objName, "SHAPE_KEY")
        if fromName:
            if fromName.lower()=="basis":
                newName += '_' + fromName
            else:
                newName += '_blend_' + fromName
    return newName


def getFromName(objName, getType):
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"
    if objName=='':
        return False

    objName = objName.split(".")[0]

    objNameSplit = objName.split('_')

    if getType == "OBJECT_NAME":
        return objNameSplit[0]

    if getType == "SHAPE_KEY":
        if objNameSplit[-1].lower() == "basis" or objNameSplit[-2].lower() == "blend":
            return objNameSplit[-1]
        return False

    for i in range(len(objNameSplit)):
        if objNameSplit[i][:3].lower()=='set':
            if getType=="OBJECT_INDEX":
                if objNameSplit[i+1].isnumeric():
                    return eval(objNameSplit[i+1])
                return False
            elif getType=="SET_INDEX":
                if objNameSplit[i][3:].isnumeric():
                    return eval(objNameSplit[i][3:])
                return False
        if getType=="INTERNAL" and objNameSplit[i].lower()=='internal':
            return True
        
        if getType=="COLLIDER" and objNameSplit[i].lower()=='collider':
            return True
        
        if getType=="MODIFIERS" and objNameSplit[i].lower()=='modifiers':
            return True
        
        if getType=="LOD" and objNameSplit[i][:3].lower()=='lod':
            return eval(objNameSplit[i][-1])
    
    return False