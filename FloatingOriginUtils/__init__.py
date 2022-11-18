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
from . import view_3D_LOD_manager
from . import view_3D_bulk_shape_key
from . import scene_management
from . import mesh_management

#######################_DRAW_UI_#######################
class VIEW3D_PT_floating_origin_tools_shape_key(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floating Origin Tools'
    bl_label = 'Shape Keys'

    def draw (self, context):
        self.layout.operator('mesh.prep_for_shapekey')
        self.layout.operator('mesh.add_shape_key')
        self.layout.operator('mesh.remove_shape_key')
        self.layout.operator('mesh.select_shape_key')
        self.layout.operator('mesh.test_shape_key')

class VIEW3D_PT_floating_origin_tools_lod(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floating Origin Tools'
    bl_label = 'LOD'

    def draw (self, context):
        self.layout.operator('mesh.add_lod')
        self.layout.operator('mesh.decimate_meshes')
        self.layout.operator('mesh.select_lod')
        self.layout.operator('mesh.deselect_lod')

class VIEW3D_PT_floating_origin_tools_scene_management(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floating Origin Tools'
    bl_label = 'Scene Management'

    def draw (self, context):
        self.layout.operator('mesh.batch_rename')
        self.layout.operator('mesh.export_fbx')

class VIEW3D_PT_floating_origin_tools_mesh_management(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Floating Origin Tools'
    bl_label = 'Mesh Management'

    def draw (self, context):
        self.layout.operator('mesh.batch_uv_unwrap')
        self.layout.operator('mesh.build_collider')
        self.layout.operator('mesh.copy_origin')
        # self.layout.operator('mesh.split_sharp_edges')


#######################_REGISTER_CLASSES_#######################
def register():
        bpy.utils.register_class(VIEW3D_PT_floating_origin_tools_shape_key)
        bpy.utils.register_class(VIEW3D_PT_floating_origin_tools_lod)
        bpy.utils.register_class(VIEW3D_PT_floating_origin_tools_scene_management)
        bpy.utils.register_class(VIEW3D_PT_floating_origin_tools_mesh_management)
        bpy.utils.register_class(view_3D_bulk_shape_key.MESH_OT_prep_for_shapekey)
        bpy.utils.register_class(view_3D_bulk_shape_key.MESH_OT_add_shape_key)
        bpy.utils.register_class(view_3D_bulk_shape_key.MESH_OT_remove_shape_key)
        bpy.utils.register_class(view_3D_bulk_shape_key.MESH_OT_select_shape_key)
        bpy.utils.register_class(view_3D_bulk_shape_key.MESH_OT_test_shape_key)
        bpy.utils.register_class(scene_management.MESH_OT_export_fbx)
        bpy.utils.register_class(scene_management.MESH_OT_rename)
        bpy.utils.register_class(view_3D_LOD_manager.MESH_OT_add_lod)
        bpy.utils.register_class(view_3D_LOD_manager.MESH_OT_select_all_lod)
        bpy.utils.register_class(view_3D_LOD_manager.MESH_OT_deselect_all_lod)
        bpy.utils.register_class(view_3D_LOD_manager.MESH_OT_decimate_meshes)
        bpy.utils.register_class(mesh_management.MESH_OT_copy_origin)
        # bpy.utils.register_class(mesh_management.MESH_OT_split_sharp_edges)
        bpy.utils.register_class(mesh_management.MESH_OT_build_collider)
        bpy.utils.register_class(mesh_management.MESH_OT_smart_uv_unwrap)

def unregister():
        bpy.utils.unregister_class(VIEW3D_PT_floating_origin_tools_shape_key)
        bpy.utils.unregister_class(VIEW3D_PT_floating_origin_tools_lod)
        bpy.utils.unregister_class(VIEW3D_PT_floating_origin_tools_scene_management)
        bpy.utils.unregister_class(VIEW3D_PT_floating_origin_tools_mesh_management)
        bpy.utils.unregister_class(view_3D_bulk_shape_key.MESH_OT_prep_for_shapekey)
        bpy.utils.unregister_class(view_3D_bulk_shape_key.MESH_OT_add_shape_key)
        bpy.utils.unregister_class(view_3D_bulk_shape_key.MESH_OT_remove_shape_key)
        bpy.utils.unregister_class(view_3D_bulk_shape_key.MESH_OT_select_shape_key)
        bpy.utils.unregister_class(view_3D_bulk_shape_key.MESH_OT_test_shape_key)
        bpy.utils.unregister_class(scene_management.MESH_OT_export_fbx)
        bpy.utils.unregister_class(scene_management.MESH_OT_rename)
        bpy.utils.unregister_class(view_3D_LOD_manager.MESH_OT_add_lod)
        bpy.utils.unregister_class(view_3D_LOD_manager.MESH_OT_select_all_lod)
        bpy.utils.unregister_class(view_3D_LOD_manager.MESH_OT_deselect_all_lod)
        bpy.utils.unregister_class(view_3D_LOD_manager.MESH_OT_decimate_meshes)
        bpy.utils.unregister_class(mesh_management.MESH_OT_copy_origin)
        # bpy.utils.unregister_class(mesh_management.MESH_OT_split_sharp_edges)
        bpy.utils.unregister_class(mesh_management.MESH_OT_build_collider)
        bpy.utils.unregister_class(mesh_management.MESH_OT_smart_uv_unwrap)
