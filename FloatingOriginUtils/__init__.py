bl_info = {
    "name": "Floating Origin Utils",
    "author": "Jacob Siepker",
    "version": (0, 0, 1),
    "blender": (3, 30, 0),
    "location": "View3D",
    "description": "Custom tools for Floating Origin production",
    "warning": "Too good to handle",
    "doc_url": "",
    "category": "Tools",
}

import bpy

#######################_DEFINE_OPERATORS_#######################
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

        i = 0
        for obj in selectionObjects:

            #Set obj as Selected and Active
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            #Duplicate Object, Rename Copy
            bpy.ops.object.duplicate()
            obj2 = bpy.context.object
            obj2.name = "TEMP_EXPORT_OBJECT_" + str(i)
            i+=1

            #Bring to Origin, Apply Transforms
            obj2.location[0] = 0
            obj2.location[1] = 0
            obj2.location[2] = 0

            bpy.ops.object.transform_apply(location=True, rotation = True, scale = True)

            ##REWORK EVERYTHING FROM HERE, TO THE RETURN

            objVariants = []
            #For each shape key (by name, get UV Map too)
            for shapeKey in obj2.data.shape_keys:
                bpy.context.view_layer.objects.active = obj2
                bpy.ops.object.duplicate()
                #Duplicate
                #Remove all other Shape Keys/UV's
                #append _ShapeKeyName to mesh
                #add to objVariants
            #Export
            #For each obj in objVariants. delete


            #Export FBX File
            bpy.ops.object.select_all(action='DESELECT')
            obj2.select_set(True)
            outputFile = filePath + obj.name + ".fbx" 
            bpy.ops.export_scene.fbx(filepath=outputFile, use_selection=True, object_types={'ARMATURE', 'EMPTY', 'MESH'})

            #Delete Copy
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

    def execute(self, context):

        selectionObjects = []

        for obj in context.selected_objects:
            selectionObjects.append(obj)

        i = 0
        for obj in selectionObjects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            obj.name = self.newName + "_" + str(i)
            i += 1

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

#######################_DRAW_UI_#######################
class VIEW3D_PT_floating_origin_tool_ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floating Origin Tools'
    bl_label = 'Pipeline Scripts'

    def draw (self, context):
        self.layout.operator('mesh.prep_for_shapekey')
        self.layout.operator('mesh.add_shape_key')
        self.layout.operator('mesh.remove_shape_key')
        self.layout.operator('mesh.export_fbx')
        self.layout.operator('mesh.batch_rename')

#######################_REGISTER_CLASSES_#######################
def register():
    bpy.utils.register_class(VIEW3D_PT_floating_origin_tool_ui)
    bpy.utils.register_class(MESH_OT_prep_for_shapekey)
    bpy.utils.register_class(MESH_OT_add_shape_key)
    bpy.utils.register_class(MESH_OT_remove_shape_key)
    bpy.utils.register_class(MESH_OT_export_fbx)
    bpy.utils.register_class(MESH_OT_rename)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_floating_origin_tool_ui)
    bpy.utils.unregister_class(MESH_OT_prep_for_shapekey)
    bpy.utils.unregister_class(MESH_OT_add_shape_key)
    bpy.utils.unregister_class(MESH_OT_remove_shape_key)
    bpy.utils.unregister_class(MESH_OT_export_fbx)
    bpy.utils.unregister_class(MESH_OT_rename)