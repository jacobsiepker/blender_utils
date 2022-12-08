import bpy


class MESH_OT_export_fbx(bpy.types.Operator):
    bl_idname = "mesh.export_fbx"
    bl_label = "Export FBX"
    bl_options = {"REGISTER", "UNDO"}

    file_path: bpy.props.StringProperty(
        name="Output Location", description="The filepath of the FBX"
    )

    def execute(self, context):
        filePath = self.file_path
        defaultPath = "S:/FloatingOrigin/local_source/temp_fbx_output"

        if filePath == None or filePath == "":
            filePath = defaultPath
        if filePath[-1] != "/":
            filePath += "/"

        # Find all objects with same name prefix
        exportObjects = []
        # firstObj = context.selected_objects[0]
        for obj in context.selected_objects:
            # if obj.name.split("_")[0] == firstObj.name.split("_")[0]:
            exportObjects.append(obj)

        # While selectionObjects isn't empty
        # while len(selectionObjects) > 0:

        tempObjects = []
        refObjects = []
        # Separate shape keys for each object
        # Adds shape key to tempObjects
        for obj in exportObjects:

            # Add Basis Shape Key if none exists
            if obj.data.shape_keys == None:
                obj.shape_key_add(from_mix=False, name="Basis")
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.data.uv_layers.active.name = "Basis"

            stopIter = False
            i = 0
            keyList = []

            # Duplicate Object, Add to refObjects
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.duplicate()
            refObj = bpy.context.object
            refObj.name = f"{obj.name}_ref"
            refObjects.append(refObj)

            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.quads_convert_to_tris()
            bpy.ops.object.editmode_toggle()

            # Set Normals to Smooth
            bpy.ops.object.shade_smooth()

            # Bring to Origin
            refObj.location[0] = 0
            refObj.location[1] = 0
            refObj.location[2] = 0

            # Apply Transformations
            bpy.ops.object.transform_apply( location=True, rotation=True, scale=True )
            bpy.ops.object.convert(target="MESH", keep_original=False)

            # Get list of all shape keys
            while not stopIter:
                refObj.active_shape_key_index = i
                if refObj.active_shape_key == None:
                    stopIter = True
                else:
                    keyList.append(refObj.active_shape_key.name)
                    i += 1

            # Iterate through shape keys
            for keyName in keyList:
                # Set current key as active
                index = refObj.data.shape_keys.key_blocks.find(keyName)
                refObj.active_shape_key_index = index

                # Set refObj as Selected and Active
                bpy.ops.object.select_all(action="DESELECT")
                refObj.select_set(True)
                bpy.context.view_layer.objects.active = refObj

                # Duplicate Object, Rename Copy
                bpy.ops.object.duplicate()
                obj2 = bpy.context.object
                if keyName.lower() != "basis":
                    obj2.name = f"{obj.name}_blend_{keyName}"
                else:
                    obj2.name = f"{obj.name}_Basis"

                # Remove Shape Keys that Do Not Match
                for shapeKeyRemove in keyList:
                    if shapeKeyRemove != keyName:
                        index = obj2.data.shape_keys.key_blocks.find(shapeKeyRemove)
                        obj2.active_shape_key_index = index
                        obj2.shape_key_remove(key=obj2.active_shape_key)

                bpy.ops.object.select_all(action="DESELECT")
                obj2.select_set(True)

                tempObjects.append(obj2)

        # Select all temp objects
        bpy.ops.object.select_all(action="DESELECT")
        for tempObj in tempObjects:
            tempObj.select_set(True)

        # Set output file name
        fileName = obj.name.split("_")[0]
        # append set and item index from the original name
        for namePart in obj.name.split("_")[1:]:
            if namePart[0] == "s" or namePart[0] == "i":
                if namePart[1].isdigit():
                    fileName += "_" + namePart


        outputFileFBX = filePath + fileName + ".fbx"

        bpy.ops.export_scene.fbx( filepath=outputFileFBX, use_mesh_edges=True, use_selection=True, object_types={"ARMATURE", "EMPTY", "MESH"} )

        # Delete Temp Objects
        for tempObj in tempObjects:
            bpy.ops.object.select_all(action="DESELECT")
            bpy.context.view_layer.objects.active = tempObj
            tempObj.select_set(True)

            bpy.ops.object.delete(use_global=False, confirm=False)
        
        # Delete Ref Objects
        for refObj in refObjects:
            bpy.ops.object.select_all(action="DESELECT")
            bpy.context.view_layer.objects.active = refObj
            refObj.select_set(True)

            bpy.ops.object.delete(use_global=False, confirm=False)

        return {"FINISHED"}
