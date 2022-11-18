import bpy

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

class MESH_OT_rename(bpy.types.Operator):
    bl_idname = 'mesh.batch_rename'
    bl_label = 'Rename'
    bl_options = {'REGISTER', 'UNDO'}

    newName: bpy.props.StringProperty(
        name = "New Object Name",
        description = "The name that will be given to all objects, with appended index"
    )

    keepNumbering: bpy.props.BoolProperty(
        name = "Keep Numbering",
        description = "Enable to keep previously established numbering scheme in form '_#_'"
    )

    def execute(self, context):

        selectionObjects = []

        for obj in context.selected_objects:
            selectionObjects.append(obj)

        i = 0
        for obj in selectionObjects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            name_split = obj.name.split("_")
            nameEnding = ''

            for namePart in name_split:
                if namePart[:9].lower() == "modifiers":
                    nameEnding += "_modifiers"
                    
                elif namePart[:3].lower() == "lod":
                    nameEnding += '_' + namePart
                
                elif self.keepNumbering:
                    try:
                        if -1 < eval(namePart) < 1000:
                            nameEnding+= "_" + namePart
                    except:
                        pass
            
            #increment if last ending was different
            if nameEnding == '' or not self.keepNumbering:
                obj.name = self.newName + '_' + str(i) + nameEnding
                i+=1
            else:
                obj.name = self.newName + nameEnding


        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}