import bpy

# from . import fileNamingConventions


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

        selectionObjects = []

        if filePath == None or filePath == "":
            filePath = defaultPath
        if filePath[-1] != "/":
            filePath += "/"

        for obj in context.selected_objects:
            selectionObjects.append(obj)

        # While selectionObjects isn't empty
        while len(selectionObjects) > 0:

            refObj = selectionObjects[0]
            exportObjects = []

            # Find all objects with same name prefix
            for obj in selectionObjects:
                if obj.name.split("_")[0] == refObj.name.split("_")[0]:
                    # add to exportObjects
                    exportObjects.append(obj)
                    # pop from selectionObjects
                    selectionObjects.remove(obj)


            tempObjects = []
            # Separate shape keys for each object
            # Adds shape key to tempObjects
            for obj in exportObjects:
                if obj.data.shape_keys == None:
                    obj.shape_key_add(from_mix=False, name="Basis")
                    bpy.context.view_layer.objects.active = obj
                    bpy.context.object.data.uv_layers.active.name = "Basis"

                stopIter = False
                i = 0
                keyList = []

                while not stopIter:
                    # Get names of all key shapes
                    obj.active_shape_key_index = i
                    if obj.active_shape_key == None:
                        stopIter = True
                    else:
                        keyList.append(obj.active_shape_key.name)
                        i += 1

                for keyName in keyList:
                    # Set current key as active
                    index = obj.data.shape_keys.key_blocks.find(keyName)
                    obj.active_shape_key_index = index

                    # Set obj as Selected and Active
                    bpy.ops.object.select_all(action="DESELECT")
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj

                    # Duplicate Object, Rename Copy
                    bpy.ops.object.duplicate()
                    obj2 = bpy.context.object
                    if keyName.lower() != "basis":
                        obj2.name = f"{obj.name}_blend_{keyName}"
                    else:
                        obj2.name = f"{obj.name}_Basis"

                    # Remove Shape Keys that Do Not Match
                    # May need to get list of items to remove on first pass, then call remove
                    for shapeKeyRemove in keyList:
                        if shapeKeyRemove != keyName:
                            index = obj2.data.shape_keys.key_blocks.find(shapeKeyRemove)
                            obj2.active_shape_key_index = index
                            obj2.shape_key_remove(key=obj2.active_shape_key)

                bpy.ops.object.select_all(action="DESELECT")
                obj2.select_set(True)

                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.mesh.quads_convert_to_tris()
                bpy.ops.object.editmode_toggle()

                # shade smooth
                bpy.ops.object.shade_smooth()

                # Bring to Origin, Apply Transforms
                obj2.location[0] = 0
                obj2.location[1] = 0
                obj2.location[2] = 0

                with bpy.context.temp_override(active_object=obj2):
                    bpy.ops.object.transform_apply(
                        location=True, rotation=True, scale=True
                    )
                    bpy.ops.object.convert(target="MESH", keep_original=False)

                tempObjects.append(obj2)

            # Select all temp objects
            bpy.ops.object.select_all(action="DESELECT")
            for tempObj in tempObjects:
                tempObj.select_set(True)

            outputFile = filePath + obj.name + ".fbx"

            # Export selection as FBX for unity
            # bpy.ops.export_scene.fbx(filepath=outputFile, \
            #  use_mesh_edges=True, use_selection=True, object_types={'ARMATURE', 'EMPTY', 'MESH'}, use_mesh_modifiers=True, use_tspace=True, use_custom_props=True, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, bake_anim=False, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')

            bpy.ops.export_scene.fbx(
                filepath=outputFile,
                use_mesh_edges=True,
                use_selection=True,
                object_types={"ARMATURE", "EMPTY", "MESH"},
            )

            # Export selection as FBX keeping the vertex count and order deterministic
            # bpy.ops.export_scene.fbx(filepath=outputFile, use_mesh_edges=True, use_selection=True, object_types={'ARMATURE', 'EMPTY', 'MESH'}, use_mesh_modifiers=True, use_tspace=True, use_custom_props=True, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, bake_anim=False, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')

            # Delete Temp Objects
            bpy.ops.object.delete(use_global=False, confirm=False)

        return {"FINISHED"}