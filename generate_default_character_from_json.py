import bpy
import json
from mathutils import Vector

# Function to create a cylinder aligned between two bones
def create_limb(name, start, end, radius, segments=16):
    length = (Vector(end) - Vector(start)).length
    mid_point = (Vector(start) + Vector(end)) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments, radius=radius, depth=length, location=mid_point)
    limb = bpy.context.object
    limb.name = name
    
    # Align cylinder with the bone's direction
    direction = Vector(end) - Vector(start)
    limb.rotation_mode = 'QUATERNION'
    limb.rotation_quaternion = direction.to_track_quat('Z', 'Y')  # Align to Z-axis
    
    return limb

# Function to create a sphere for hands/feet/head and set the origin at the base, aligned to the bone's direction
def create_sphere_aligned(name, bone_data, radius):
    start = Vector(bone_data['head_local'])
    end = Vector(bone_data['tail_local'])
    mid_point = (start + end) / 2
    
    # Create the sphere at the mid-point
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=mid_point)
    sphere = bpy.context.object
    sphere.name = name
    
    # Align the sphere with the bone's direction
    direction = end - start
    sphere.rotation_mode = 'QUATERNION'
    sphere.rotation_quaternion = direction.to_track_quat('Z', 'Y')  # Align to Z-axis
    
    # Move the origin to the head of the bone (base of the sphere)
    bpy.context.scene.cursor.location = start
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    return sphere

# Remove Head.001 if it exists before starting
if "Head.001" in bpy.data.objects:
    print("Removing Head.001...")
    bpy.data.objects.remove(bpy.data.objects["Head.001"], do_unlink=True)

# Load the armature data from JSON
json_path = bpy.path.abspath("//armatures_data.json")
with open(json_path, 'r') as file:
    data = json.load(file)

# Define body parts and limb sizes
limb_sizes = {
    "arm": 5.0,
    "leg": 8.0,
    "torso": 10.0,
    "head": 12.0,
    "hand_foot": 6.0,
    "neck": 4.0  # Neck size remains
}

# Updated: Removing "Head" from the limb array to avoid it being created as a cylinder
limbs = {
    "Left Arm": ["character_rig:LeftArm", "character_rig:LeftForeArm"],
    "Right Arm": ["character_rig:RightArm", "character_rig:RightForeArm"],
    "Left Leg": ["character_rig:LeftUpLeg", "character_rig:LeftLeg"],
    "Right Leg": ["character_rig:RightUpLeg", "character_rig:RightLeg"],
    "Torso": ["character_rig:Spine", "character_rig:Spine2"],
    "Neck": ["character_rig:Neck", "character_rig:Neck"]  # Neck now spans only the Neck bone
}

# Create limbs (excluding Head to avoid creating Head.001 as a cylinder)
for armature, bones in data.items():
    for limb_name, (start_bone, end_bone) in limbs.items():
        start = bones[start_bone]['head_local']
        end = bones[end_bone]['tail_local']
        
        # Create a limb using the correct size based on the type (e.g., arm, leg, neck, etc.)
        if "Arm" in limb_name:
            radius = limb_sizes["arm"]
        elif "Leg" in limb_name:
            radius = limb_sizes["leg"]
        elif "Torso" in limb_name:
            radius = limb_sizes["torso"]
        elif "Neck" in limb_name:
            radius = limb_sizes["neck"]  # Neck spans only the Neck bone
        
        create_limb(name=limb_name, start=start, end=end, radius=radius)

# Ensure Head.001 is still not present before creating spheres
if "Head.001" in bpy.data.objects:
    print("Re-removing Head.001...")
    bpy.data.objects.remove(bpy.data.objects["Head.001"], do_unlink=True)

# Generate spheres for hands, feet, and head, aligned to bones
hands_feet_and_head = {
    "Right Foot": "character_rig:RightFoot",
    "Left Foot": "character_rig:LeftFoot",
    "Right Hand": "character_rig:RightHand",
    "Left Hand": "character_rig:LeftHand",
    "Head": "character_rig:Head"
}

for body_part, bone_name in hands_feet_and_head.items():
    bone_data = data["Armature"][bone_name]
    if "Foot" in body_part or "Hand" in body_part:
        radius = limb_sizes["hand_foot"]
    else:
        radius = limb_sizes["head"]
    
    create_sphere_aligned(name=body_part, bone_data=bone_data, radius=radius)

print("Finished creating limbs and aligned spheres. Ensured Head.001 is not created as a cylinder.")