import bpy

class MESH_OT_add_lod(bpy.types.Operator):
    bl_idname = 'mesh.add_lod'
    bl_label = 'Add LOD'
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        selectionObjects = []
        lodObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            #Set selection
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            #Duplicate Object, Rename Copy
            bpy.ops.object.duplicate()
            obj2 = bpy.context.object

            #Naming Convention
            collectionName = obj.name
            if obj.name[-5:-1].lower() == "_lod":
                level = eval(collectionName[-1])
                obj2.name = collectionName[:-1] + str(level+1)
            else:
                obj.name = collectionName + "_lod0"
                obj2.name = collectionName + "_lod1"
            
            lodObjects.append(obj2)

            bpy.ops.object.select_all(action='DESELECT')

            #Could add LOD levels to a collection with the same object name here

            obj.hide_set(True)

        for obj in lodObjects:
            obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_select_all_lod(bpy.types.Operator):
    bl_idname = 'mesh.select_lod'
    bl_label = 'Select All LOD'
    bl_options = {'REGISTER', 'UNDO'}

    select_colliders: bpy.props.BoolProperty(
        name = "Include Colliders",
        description = "Enable to select collider."
    )
    select_modifiers: bpy.props.BoolProperty(
        name = "Include Modifiers",
        description = "Enable to include mesh with modifiers"
    )

    def execute(self, context):
        selectionPrefix = []
        for obj in context.selected_objects:
            nameSplit = obj.name.split('_')
            thisSelectionPrefix = ''
            for namePart in nameSplit:
                if namePart != nameSplit[-1]:
                    thisSelectionPrefix += namePart + '_'
            selectionPrefix.append(thisSelectionPrefix)

        activeObject = None
        for obj in bpy.data.objects:

            matches = False
            matchingPrefix = None
            for prefix in selectionPrefix:
                if prefix in obj.name:
                    matches = True

            if matches:
                select = False
                if obj.name.split('_')[-1].lower() == 'modifiers' and self.select_modifiers:
                    select = True
                elif obj.name.split('_')[-1].lower() == 'collider' and self.select_colliders:
                    select = True
                elif obj.name.split('_')[-1].lower()[:3] == 'lod':
                    select = True

                if select:
                    obj.hide_set(False)
                    obj.select_set(True)
                    activeObject = obj

        bpy.context.view_layer.objects.active = activeObject

        return {'FINISHED'}

class MESH_OT_deselect_all_lod(bpy.types.Operator):
    bl_idname = 'mesh.deselect_lod'
    bl_label = 'Select Mesh Version'
    bl_options = {'REGISTER', 'UNDO'}

    keepSelected: bpy.props.IntProperty(
        name = "LOD to Keep",
        description = "The LOD to keep visible and selected"
    )

    def execute(self, context):
        selectionPrefix = []
        for obj in context.selected_objects:
            nameSplit = obj.name.split('_')
            thisSelectionPrefix = ''
            for namePart in nameSplit:
                if namePart != nameSplit[-1]:
                    thisSelectionPrefix += namePart + '_'
            selectionPrefix.append(thisSelectionPrefix)

        keep_selected = self.keepSelected
        if self.keepSelected == -1:
            keep_selected = "collider"
        elif self.keepSelected == -2:
            keep_selected = "modifiers"
        else:
            keep_selected = "lod" + str(self.keepSelected)

        activeObject = None
        for obj in bpy.data.objects:

            matches = False
            for prefix in selectionPrefix:
                if prefix in obj.name:
                    matches = True

            if matches and obj.name.split('_')[-1].lower() == keep_selected:
                obj.hide_set(False)
                obj.select_set(True)
                activeObject = obj

            elif matches:
                obj.hide_set(True)
                obj.select_set(False)

        bpy.context.view_layer.objects.active = activeObject
        return {'FINISHED'}

class MESH_OT_decimate_meshes(bpy.types.Operator):
    bl_idname = 'mesh.decimate_meshes'
    bl_label = 'Decimate All Meshes'
    bl_options = {'REGISTER', 'UNDO'}

    ratio: bpy.props.FloatProperty(
        name = "Ratio",
        description = "The ratio of decimation"
    )

    def execute(self, context):
        selectedObjects = []
        for obj in context.selected_objects:
            selectedObjects.append(obj)

        for obj in selectedObjects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.decimate(ratio=self.ratio)
            bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in selectedObjects:
            obj.select_set(True)

        return {'FINISHED'}
