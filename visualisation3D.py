import bpy
import math
from mathutils import Vector, Euler

# ========== DANE Z GENERATION 299 ==========
positions = [
    (99, 42, 34),
    (97, 97, 55),
    (96, 79, 23),
    (89, 1, 20)
]

candels = [1000, 1000, 1000, 1000]
angles = [48, 25, 29, 31]

# ========== USUŃ WSZYSTKO ==========
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)



# comment




for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)
for light in bpy.data.lights:
    bpy.data.lights.remove(light)

print("\n" + "="*60)
print("TWORZENIE SCENY...")
print("="*60 + "\n")

# ========== 1. PODŁOGA ==========
bpy.ops. mesh.primitive_plane_add(size=200, location=(50, 50, 0))
ground = bpy.context.active_object
ground.name = "GROUND"

mat_ground = bpy.data.materials.new(name="Mat_Ground")
mat_ground.use_nodes = True
bsdf = mat_ground.node_tree. nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
bsdf.inputs["Roughness"].default_value = 0.9

ground.data.materials.append(mat_ground)
print("✓ Podłoga")

# ========== 2. ŻÓŁTE KULE ==========
for i, pos in enumerate(positions):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=3, location=pos)
    sphere = bpy.context.active_object
    sphere.name = f"MARKER_{i}"
    
    mat = bpy.data.materials.new(name=f"Mat_Marker_{i}")
    mat.use_nodes = True
    nodes = mat.node_tree. nodes
    
    nodes.remove(nodes["Principled BSDF"])
    
    emission = nodes. new(type="ShaderNodeEmission")
    emission.inputs["Color"].default_value = (1.0, 1.0, 0.0, 1.0)
    emission.inputs["Strength"].default_value = 200.0
    
    output = nodes["Material Output"]
    mat.node_tree.links.new(emission.outputs[0], output.inputs["Surface"])
    
    sphere.data.materials.append(mat)
    print(f"✓ Kula {i} na pozycji {pos}")

# ========== 3. FUNKCJA TWORZENIA STOŻKA-KLOSZA  ==========
def create_cone_shade(name, position, angle_deg, height=50):
    """
    Tworzy stożek-klosz:  wierzchołek u góry (przy świetle), podstawa na dole
    """
    # Oblicz promień podstawy (dolnej, szerokiej części)
    radius = height * math.tan(math.radians(angle_deg))
    
    # Utwórz stożek - domyślnie wierzchołek u góry
    bpy.ops.mesh.primitive_cone_add(
        vertices=32,
        radius1=radius,  # Promień podstawy (dół)
        radius2=0,        # Wierzchołek (góra)
        depth=height,
        location=position
    )
    
    cone = bpy.context.active_object
    cone.name = name
    
    # BRAK OBROTU - stożek już ma wierzchołek u góry! 
    # Domyślna orientacja: wierzchołek +Z, podstawa -Z
    
    # Przesuń w dół, żeby wierzchołek był w pozycji światła
    cone.location = (position[0], position[1], position[2] - height/2)
    
    # Usuń górną ścianę (wierzchołek) - światło musi wyjść
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    mesh = cone.data
    for face in mesh.polygons:
        vertices = [mesh.vertices[v] for v in face. vertices]
        avg_z = sum(v.co.z for v in vertices) / len(vertices)
        # Usuń górny wierzchołek (max Z w local space)
        if avg_z > height/2 - 0.1: 
            face.select = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh. delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Materiał
    mat = bpy. data.materials.new(name=f"Mat_{name}")
    mat.use_nodes = True
    nodes = mat.node_tree. nodes
    
    bsdf = nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.8
    bsdf.inputs["Metallic"].default_value = 0.3
    
    cone.data.materials.append(mat)
    cone.visible_shadow = True
    
    return cone

# ========== 4. ŚWIATŁA + STOŻKI ==========
for i, (pos, intensity, ang) in enumerate(zip(positions, candels, angles)):
    # Światło
    bpy.ops. object.light_add(type='SPOT', location=pos)
    light_obj = bpy.context.active_object
    light_obj. name = f"LIGHT_{i}"
    
    light_data = light_obj.data
    light_data.energy = intensity * 2000.0
    
    full_cone_angle = ang * 2.0
    light_data.spot_size = math.radians(full_cone_angle)
    light_data.spot_blend = 0.15
    light_data.color = (1.0, 1.0, 1.0)
    light_data.use_contact_shadow = True
    light_data.contact_shadow_distance = 5.0
    
    # Skieruj w dół
    light_obj.rotation_euler = Euler((math.radians(180), 0, 0))
    
    # Stożek-klosz
    cone_height = min(pos[2] - 1, 40)
    create_cone_shade(f"CONE_SHADE_{i}", pos, ang, height=cone_height)
    


# ========== 5. KAMERA ==========
bpy.ops.object.camera_add(location=(200, -200, 120))
camera = bpy.context. active_object
camera.name = "CAMERA"

look_at = Vector((50, 50, 30))
direction = look_at - camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat. to_euler()

bpy.context.scene.camera = camera


# ========== 6. EEVEE ==========
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

bpy.context.scene.eevee.use_volumetric_lights = True
bpy.context. scene.eevee.volumetric_start = 0.1
bpy.context.scene. eevee.volumetric_end = 200
bpy. context.scene.eevee. volumetric_tile_size = '8'
bpy.context. scene.eevee.volumetric_samples = 64

bpy.context.scene.eevee.use_bloom = True
bpy.context. scene.eevee.bloom_intensity = 0.5

bpy.context.scene.eevee.use_shadows = True
bpy.context. scene.eevee.use_shadow_high_bitdepth = True
bpy.context.scene.eevee.shadow_cube_size = '1024'
bpy.context.scene.eevee.shadow_cascade_size = '2048'

bpy.context. scene.eevee.use_gtao = True

world = bpy.context.scene.world
world.use_nodes = True
bg_node = world.node_tree.nodes["Background"]
bg_node.inputs["Color"].default_value = (0.02, 0.02, 0.02, 1.0)
bg_node.inputs["Strength"].default_value = 0.05


# ========== 7. WIDOK ==========
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'
                    space.overlay.show_extras = True

# Weryfikacja
print("LISTA OBIEKTÓW:")
for obj in bpy.data.objects:
    if "CONE_SHADE" in obj.name:
        print(f"  • {obj.name} - rotation={obj.rotation_euler}")
    else:
        print(f"  • {obj.name} ({obj.type})")