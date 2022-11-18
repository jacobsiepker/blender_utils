import bpy

class MESH_OT_cleanup(bpy.types.Operator):
    bl_idname = 'mesh.cleanup_mesh'
    bl_label = 'Apply basic operations to clean up the mesh'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            pass
        
        for obj in selectionObjects:
            obj.set_select(True)

        return {'FINISHED'}

class MESH_OT_copy_origin(bpy.types.Operator):
    bl_idname = 'mesh.copy_origin'
    bl_label = 'Copy the origin of the active object to all selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectionObjects = []
        #get active object
        #get active object origin
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            pass
            #set the origin
        
        for obj in selectionObjects:
            obj.set_select(True)

        return {'FINISHED'}

class MESH_OT_bring_to_active(bpy.types.Operator):
    bl_idname = 'mesh.bring_to_active'
    bl_label = 'Move each selected object to the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectionObjects = []
        #get active object
        #get active object origin
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            pass
            #move objects to this object
        
        for obj in selectionObjects:
            obj.set_select(True)

        return {'FINISHED'}