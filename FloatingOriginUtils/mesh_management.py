import bpy
import bmesh

class MESH_OT_batch_cleanup(bpy.types.Operator):
    bl_idname = 'mesh.batch_cleanup'
    bl_label = 'Cleanup'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')

                bpy.ops.mesh.remove_doubles()

                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)

                #deselect all edges
                bpy.ops.mesh.select_all(action='DESELECT')
                #select edges marked sharp
                #for each edge, if it is marked sharp, select it. Using bmesh.
                bm = bmesh.from_edit_mesh(obj.data)
                for e in bm.edges:
                    if not e.smooth:
                        e.select = True
                bmesh.update_edit_mesh(obj.data)
                
                #split edges
                bpy.ops.mesh.edge_split()

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.shade_smooth()
                bpy.ops.object.select_all(action='DESELECT')
            else:
                obj.select_set(False)

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

class MESH_OT_bring_to_active(bpy.types.Operator):
    bl_idname = 'mesh.bring_to_active'
    bl_label = 'Bring to Active'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #Get selected objects
        selectedObjects = []
        activeObj = bpy.context.view_layer.objects.active

        for obj in context.selected_objects:
            selectedObjects.append(obj)

        #Set each objects location
        for obj in selectedObjects:
            obj.location = activeObj.location
        
        return {'FINISHED'}

class MESH_OT_smart_uv_unwrap(bpy.types.Operator):
    bl_idname = 'mesh.batch_uv_unwrap'
    bl_label = 'Smart UV Unwrap'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectionObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            #Set selection
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            #Apply scale and rotation before unwrapping
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            #Unwrap
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.uv.smart_project(island_margin=0.005)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
        
        for obj in selectionObjects:
            obj.select_set(True)

        return {'FINISHED'}

class MESH_OT_build_collider(bpy.types.Operator):
    bl_idname = 'mesh.build_collider'
    bl_label = 'Build Collider'
    bl_options = {'REGISTER', 'UNDO'}

    decimate_ratio: bpy.props.FloatProperty(
        name = "Decimate Ratio",
        description = "The ratio of decimation"
    )

    disolve_angle: bpy.props.FloatProperty(
        name = "Disolve Angle",
        description = "The ratio of decimation"
    )

    def execute(self, context):
        selectionObjects = []
        colliderObjects = []
        for obj in context.selected_objects:
            selectionObjects.append(obj)

        for obj in selectionObjects:
            #Set selection
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            #Duplicate Object
            bpy.ops.object.duplicate()
            obj2 = bpy.context.object

            #Naming Convention
            obj.name = obj.name.split('.')[0]
            objNameSplit = obj.name.split('_')
            if objNameSplit[-1][:3] == 'lod':
                obj2.name = obj.name[:-4] + 'collider'
            else:
                obj2.name = obj.name + "_collider"
            
            colliderObjects.append(obj2)

            bpy.ops.object.mode_set(mode = 'EDIT')

            #Perform geometry operations
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.mesh.dissolve_limited(angle_limit=self.disolve_angle)
            bpy.ops.mesh.decimate(ratio=self.decimate_ratio)
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            bpy.ops.object.mode_set(mode = 'OBJECT')

            bpy.ops.object.select_all(action='DESELECT')            

            obj.hide_set(True)

        for obj in colliderObjects:
            obj.select_set(True)


        return {'FINISHED'}