import bpy

#TODO: Mesh Cleanup
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
    bl_label = 'Copy Origin'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        #Get selected objects and active object
        selectedObjects = []
        activeObj = bpy.context.view_layer.objects.active
        for obj in context.selected_objects:
            selectedObjects.append(obj)

        for obj in selectedObjects:
            #Set object selection
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            #Get object locations
            activeObjLocation = activeObj.location
            objLocation = obj.location
            
            #Calculate location differeance
            locDiff = []
            for i in range(len(activeObjLocation)):
                locDiff.append(  -(activeObjLocation[i] - objLocation[i])  )

            #Move verticies away from origin by negative location differance
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.translate(value=(locDiff[0], locDiff[1], locDiff[2]))
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            #Move origin by location differance
            for i in range(len(obj.location)):
                obj.location[i] -= locDiff[i]

        for obj in selectedObjects:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = activeObj

        return {'FINISHED'}


#TODO: Bring to Active
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


class MESH_OT_split_sharp_edges(bpy.types.Operator):
    bl_idname = 'mesh.split_sharp_edges'
    bl_label = 'Split Sharp Edges'
    bl_options = {'REGISTER', 'UNDO'}

    selectByAngle: bpy.props.BoolProperty(
        name = "Select By Angle",
        description = "Enable to keep previously established numbering scheme in form '_#_'"
    )

    angleCutoff: bpy.props.FloatProperty(
        name = "Angle Cutoff",
        description = "The minimum angle that will be split"
    )


    def execute(self, context):
        #Get selected objects
        selectedObjects = []
        activeObj = bpy.context.view_layer.objects.active
        for obj in context.selected_objects:
            selectedObjects.append(obj)

        for obj in selectedObjects:
            #Set object selection
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')

            #TODO: Will not select just sharp edges when trying to deselect prev selection

            for e in obj.data.edges:
                # e.select = False
                if e.use_edge_sharp:
                    e.select = True

            bpy.ops.object.mode_set(mode = 'EDIT')
            #TODO: Fix the following code block - Sharp Edges are not selected by angle
            if self.selectByAngle:
                bpy.ops.mesh.edges_select_sharp(sharpness=self.angleCutoff)
            
            #TODO: Edge split does not succeed or throw error
            bpy.ops.mesh.edge_split()
            bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in selectedObjects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = activeObj

        return {'FINISHED'}


class MESH_OT_remove_doubles(bpy.types.Operator):
    bl_idname = 'mesh.remove_doubles'
    bl_label = 'Remove Doubles'
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

#TODO: Smart UV Unwrap
class MESH_OT_smart_uv_unwrap(bpy.types.Operator):
    bl_idname = 'mesh.smart_uv_unwrap'
    bl_label = 'Smart UV Unwrap'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectionObjects = []
        #get active object
        #get active object origin
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            pass
            #Enter edit mode, call smart UV project on each object
        
        for obj in selectionObjects:
            obj.set_select(True)

        return {'FINISHED'}


        #MODEL MESH
        #PREP FOR SHAPE KEY
        #SETUP SHAPE KEYS

        #TODO: SET NORMALS
        #TODO: REMOVE DOUBLES
        #SELECT SHARP EDGES -> BEVEL
        #SMART UV PROJECT
        #MARK SHARP EDGES (Not necessarily splitting every level)
            #ADD LOD
            #DECIMATE
        #SPLIT SHARP EDGES
        
