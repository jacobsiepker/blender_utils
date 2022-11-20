import bpy
from . import fileNamingConventions

class MESH_OT_export_fbx(bpy.types.Operator):
    bl_idname = 'mesh.export_fbx'
    bl_label = 'Export FBX'
    bl_options = {'REGISTER', 'UNDO'}

    file_path: bpy.props.StringProperty(
        name = "Output Location",
        description = "The filepath of the FBX"
    )

    def execute(self, context):
        filePath = self.file_path
        defaultPath = "S:/FloatingOrigin/local_source/temp_fbx_output"

        selectionObjects = []

        if filePath == None or filePath == '':
            filePath = defaultPath
        if filePath[-1] != '/':
            filePath += '/'

        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            tempObjects = []
            i = 0

            if obj.data.shape_keys == None:
                obj.shape_key_add(from_mix=False, name="Basis")
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.data.uv_layers.active.name = "Basis"

            stopIter = False
            i=0
            keyList = []
            while not stopIter:
                #Get names of all key shapes
                obj.active_shape_key_index = i
                if obj.active_shape_key == None:
                    stopIter = True
                else:
                    keyList.append(obj.active_shape_key.name)
                    i+=1

            for keyName in keyList:
                #Set current key as active
                index = obj.data.shape_keys.key_blocks.find(keyName)
                obj.active_shape_key_index = index

                #Set obj as Selected and Active
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                #Duplicate Object, Rename Copy
                bpy.ops.object.duplicate()
                obj2 = bpy.context.object
                if keyName.lower() != "basis":
                    obj2.name = f"{obj.name}_blend_{keyName}"
                else:
                    obj2.name = f"{obj.name}_Basis"
                i+=1

                #Remove Shape Keys that Do Not Match
                #May need to get list of items to remove on first pass, then call remove
                for shapeKeyRemove in keyList:
                    if shapeKeyRemove != keyName:
                        index = obj2.data.shape_keys.key_blocks.find(shapeKeyRemove)
                        obj2.active_shape_key_index = index
                        obj2.shape_key_remove(key=obj2.active_shape_key)

                #Remove UV Maps that do no match
                #Currently not implemented, not necessary
                #Could save some object disc size

                #Bring to Origin, Apply Transforms
                obj2.location[0] = 0
                obj2.location[1] = 0
                obj2.location[2] = 0

                with bpy.context.temp_override(active_object=obj2):
                    bpy.ops.object.transform_apply(location=True, rotation = True, scale = True)
                    bpy.ops.object.convert(target='MESH', keep_original=False)

                tempObjects.append(obj2)

            #Select all temp objects
            bpy.ops.object.select_all(action='DESELECT')
            for tempObj in tempObjects:
                tempObj.select_set(True)
            outputFile = filePath + obj.name + ".fbx" 
            bpy.ops.export_scene.fbx(filepath=outputFile, use_mesh_edges=True, use_selection=True, object_types={'ARMATURE', 'EMPTY', 'MESH'})

            #Delete Temp Objects
            bpy.ops.object.delete(use_global=False, confirm=False)

        return {'FINISHED'}


#TODO: Make a seperate "update name" operator to change a name one param at a time

#TODO: Make this function only create new names, you can choose to include each element and what it is, no option to keep existing name. Auto index
class MESH_OT_batch_name(bpy.types.Operator):
    bl_idname = 'mesh.batch_name'
    bl_label = 'Name'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    newName: bpy.props.StringProperty(
        name = "New Object Name",
        description = "The name that will be given to all objects, with appended index")
    setIndex: bpy.props.IntProperty(
        name = "Index of Set" #-1 for none
    )
    lod: bpy.props.IntProperty(
        name = "LOD Level" #-1 for none
        )
    disableAutoIndex: bpy.props.BoolProperty(
        name = "Disable Auto Indexing")
    internal: bpy.props.BoolProperty(
        name = "Is Internal")
    collider: bpy.props.BoolProperty(
        name = "Is Collider")
    modifiers: bpy.props.BoolProperty(
        name = "Is Modifiers")

    #TODO: auto indexing not appearing
    def execute(self, context):
        selectionObjects = []

        for obj in context.selected_objects:
            selectionObjects.append(obj)

        i = False
        if not self.disableAutoIndex:
            i = 1

        for obj in selectionObjects:
            if self.setIndex < 0:
                self.setIndex = False

            if self.lod < 0:
                self.lod = -1

            obj.name = fileNamingConventions.updateName(objectName=self.newName, setIndex=self.setIndex, lodIndex=self.lod, objectIndex=i, internal=self.internal, collider=self.collider, modifiers=self.modifiers)
            
            if not self.disableAutoIndex:
                i+=1

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}