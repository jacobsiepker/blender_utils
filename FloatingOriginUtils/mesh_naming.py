import bpy
from . import fileNamingConventions

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


class MESH_OT_update_object_name(bpy.types.Operator):
    bl_idname = 'mesh.update_object_name'
    bl_label = 'Object Name'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    newName: bpy.props.StringProperty(
        name = "New Object Name",
        description = "The name that will be given to all objects, with appended index"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, objectName=self.newName)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

#TODO: Changing set index destorys tags following it
class MESH_OT_update_set_index(bpy.types.Operator):
    bl_idname = 'mesh.update_set_index'
    bl_label = 'Set Index'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    setIndex: bpy.props.IntProperty(
        name = "Index of Set"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        if self.setIndex < 1:
            self.setIndex = False

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, setIndex=self.setIndex)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}


class MESH_OT_update_object_index(bpy.types.Operator):
    bl_idname = 'mesh.update_object_index'
    bl_label = 'Object Index'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    objectIndex: bpy.props.IntProperty(
        name = "Index of Object"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        if self.objectIndex < 1:
            self.objectIndex = False

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, objectIndex=self.objectIndex)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

#TODO: Setup versioning support
# class MESH_OT_update_object_version(bpy.types.Operator):
#     bl_idname = 'mesh.update_object_version'
#     bl_label = 'Object Version'
#     bl_options = {'REGISTER', 'UNDO'}
#    # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

#     objectVersion: bpy.props.IntProperty(
#         name = "Index of Version"
#     )

#     def execute(self, context):
#         selectionObjects = []
#         for obj in context.selected_objects:
#             selectionObjects.append(obj)

#         for obj in selectionObjects:
#             obj.name = fileNamingConventions.updateName(obj.name, objectVersion=self.objectVersion)

#         for obj in selectionObjects:
#             obj.select_set(True)

#         return {'FINISHED'}

class MESH_OT_update_internal(bpy.types.Operator):
    bl_idname = 'mesh.update_internal'
    bl_label = 'Internal'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    internal: bpy.props.BoolProperty(
        name = "Set Internal"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, internal=self.internal)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_update_collider(bpy.types.Operator):
    bl_idname = 'mesh.update_collider'
    bl_label = 'Collider'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    collider: bpy.props.BoolProperty(
        name = "Set Collider"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, collider=self.collider)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_update_modifiers(bpy.types.Operator):
    bl_idname = 'mesh.update_modifiers'
    bl_label = 'Modifiers'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    modifiers: bpy.props.BoolProperty(
        name = "Set Modifiers"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, modifiers=self.modifiers)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_update_lod(bpy.types.Operator):
    bl_idname = 'mesh.update_lod'
    bl_label = 'LOD'
    bl_options = {'REGISTER', 'UNDO'}
   # "OBJECT_NAME", "OBJECT_INDEX", "SET_INDEX", "INTERNAL", "COLLIDER", "MODIFIERS", "LOD", "SHAPE_KEY"

    lodIndex: bpy.props.IntProperty(
        name = "Set LOD"
    )

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            obj.name = fileNamingConventions.updateName(obj.name, lodIndex=self.lodIndex)

        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}