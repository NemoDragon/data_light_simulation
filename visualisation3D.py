import bpy
import re
import math
from mathutils import Vector, Euler


file_path = "C:/Users/Adam/Pulpit/STUDIA/SEM7/LightGeneticsResultsPython/pythonProject/results/v4/ga4_exp016_1.txt" 



def load_last_generation(path):
    with open(path, "r") as f:
        text = f.read()

    generations = re.findall(
        r"Generation (\d+): Best fitness = .*?Individual positions:(.*?)Individual candel values:(.*?)Individual angle values:(.*?)(?:Generation|\Z)",
        text,
        re.S
    )

    if not generations:
        raise ValueError("Nie znaleziono generacji w pliku")

    gen_id, pos_block, candel_block, angle_block = generations[-1]

    positions = re.findall(r"\[(\d+)\s+(\d+)\s+(\d+)\]", pos_block)
    positions = [(float(x), float(y), float(z)) for x, y, z in positions]

    candels = re.findall(r"([\d\.]+)", candel_block)
    candels = [float(v) for v in candels]

    angles = re.findall(r"(\d+)", angle_block)
    angles = [float(a) for a in angles]

    return positions, candels, angles



def create_spotlight(name, position, intensity, angle_deg):

    bpy.ops.object.light_add(type='SPOT', location=position)
    light = bpy.context.object
    light.name = name

    light.data.energy = intensity / 2.0   

    light.data.spot_size = math.radians(angle_deg)

    light.rotation_euler = Euler((math.radians(90), 0, 0))

    return light



def add_volumetrics():
    bpy.ops.mesh.primitive_cube_add(size=200, location=(50, 50, 50))
    cube = bpy.context.object
    cube.name = "VOLUME_BOX"

    mat = bpy.data.materials.new(name="VolumeMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    for n in nodes:
        nodes.remove(n)

    output = nodes.new(type="ShaderNodeOutputMaterial")
    volume = nodes.new(type="ShaderNodeVolumeScatter")

    volume.inputs["Density"].default_value = 0.03
    volume.inputs["Anisotropy"].default_value = 0.0

    mat.node_tree.links.new(volume.outputs[0], output.inputs["Volume"])

    cube.data.materials.append(mat)



positions, candels, angles = load_last_generation(file_path)

print(f"Załadowano światła: {len(positions)}")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

add_volumetrics()

for i, (pos, intensity, ang) in enumerate(zip(positions, candels, angles)):
    create_spotlight(f"Light_{i}", pos, intensity, ang)

print("Wszystkie światła dodane do sceny.")



bpy.ops.object.camera_add(location=(150, -150, 150))
camera = bpy.context.object
camera.rotation_euler = Euler((math. radians(60), 0, math.radians(45)))
bpy.context.scene.camera = camera


bpy.context. scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128


for area in bpy.context.screen.areas:
    if area. type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space. shading.type = 'RENDERED'