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

    def execute(self, context):
        selectionPrefix = []
        for obj in context.selected_objects:
            selectionPrefix.append(obj.name[:-5])

        for obj in bpy.data.objects:
            if obj.name[:-5] in selectionPrefix:
                obj.hide_set(False)
                obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_deselect_all_lod(bpy.types.Operator):
    bl_idname = 'mesh.deselect_lod'
    bl_label = 'Deselect All LODs'
    bl_options = {'REGISTER', 'UNDO'}

    keepSelected: bpy.props.IntProperty(
        name = "LOD to Keep",
        description = "The LOD to keep visible and selected"
    )

    def execute(self, context):
        selectionPrefix = []
        for obj in context.selected_objects:
            selectionPrefix.append(obj.name[:-5])

        for obj in bpy.data.objects:
            if obj.name[:-5] in selectionPrefix and obj.name[-5:].lower() == "_lod"+str(self.keepSelected):
                obj.hide_set(False)
                obj.select_set(True)
            elif obj.name[:-5] in selectionPrefix:
                obj.hide_set(True)
                obj.select_set(False)

        return {'FINISHED'}