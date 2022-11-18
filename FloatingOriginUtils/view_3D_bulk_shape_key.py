import bpy

class MESH_OT_prep_for_shapekey(bpy.types.Operator):
    bl_idname = 'mesh.prep_for_shapekey'
    bl_label = 'Prep for Shape Key'
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        selectionObjects = []
        duplicateObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)

            with bpy.context.temp_override(active_object=obj):
                bpy.ops.object.convert(target='MESH', keep_original=True)
            duplicateObjects.append(context.active_object)
            obj.name = obj.name + "_modifiers"
            obj.hide_set(True)

        for obj in duplicateObjects:
            obj.name = obj.name[:-4]
            obj.shape_key_add(from_mix=False, name="Basis")

            bpy.context.view_layer.objects.active = obj
            bpy.context.object.data.uv_layers.active.name = "Basis"
            obj.select_set(True)

        return {'FINISHED'}


class MESH_OT_add_shape_key(bpy.types.Operator):
    bl_idname = 'mesh.add_shape_key'
    bl_label = 'Add Shape Key'
    bl_options = {'REGISTER', 'UNDO'}

    key_name: bpy.props.StringProperty(
        name = "Shape Key Name",
        description = "The name of the shape key that will be applied to all selected objects"
    )

    def execute(self, context):
        shapeKeyName = self.key_name

        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)

            obj.shape_key_add(from_mix=False, name=shapeKeyName)
            index = obj.data.shape_keys.key_blocks.find(shapeKeyName)
            obj.active_shape_key_index = index

            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.mesh.uv_texture_add()
            bpy.context.object.data.uv_layers.active.name = shapeKeyName


        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_remove_shape_key(bpy.types.Operator):
    bl_idname = 'mesh.remove_shape_key'
    bl_label = 'Remove Shape Key'
    bl_options = {'REGISTER', 'UNDO'}

    key_name: bpy.props.StringProperty(
        name = "Shape Key Name",
        description = "The name of the shape key that will be deleted from all selected objects"
    )
    delete_all: bpy.props.BoolProperty(
        name = "Delete All",
        description = "Enable to destry all non-basis shape keys"
    )

    def execute(self, context):
        shapeKeyName = self.key_name
        deleteAll = self.delete_all

        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)
            
        for obj in selectionObjects:
            if not deleteAll:
                index = obj.data.shape_keys.key_blocks.find(shapeKeyName)  ##THROWS ERROR WHEN NO SHAPE KEY EXISTS ON OBJECT
                obj.active_shape_key_index = index
                if obj.active_shape_key != None:
                    obj.shape_key_remove(key=obj.active_shape_key)
            else:
                i = 0
                while True:
                    obj.active_shape_key_index = i
                    
                    if obj.active_shape_key == None:
                        break
                    
                    if obj.active_shape_key.name != "Basis":
                        obj.shape_key_remove(key=obj.active_shape_key)
                    
                    else:
                        i += 1

        return {'FINISHED'}


class MESH_OT_test_shape_key(bpy.types.Operator):
    bl_idname = 'mesh.test_shape_key'
    bl_label = 'Test Shape Keys'
    bl_options = {'REGISTER', 'UNDO'}

    key_name: bpy.props.StringProperty(
        name = "Shape Key Name",
        description = "The name of the shape key that will be modified for all selected objects"
    )
    value: bpy.props.FloatProperty(
        name = "Value",
        description = "The value to be set on all matching shape keys"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)
        
        for obj in selectionObjects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            if obj.data.shape_keys != None:
                index = obj.data.shape_keys.key_blocks.find(self.key_name)  ##THROWS ERROR WHEN NO SHAPE KEY EXISTS ON OBJECT
                obj.active_shape_key_index = index
                if obj.active_shape_key != None:
                    obj.active_shape_key.value = self.value

        
        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}