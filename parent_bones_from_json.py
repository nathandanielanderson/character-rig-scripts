import bpy
import json

# Load the armature data from JSON
json_path = bpy.path.abspath("//armatures_data.json")
with open(json_path, 'r') as file:
    data = json.load(file)

# Define body parts and corresponding bone names
limb_bones = {
    "Left Arm": "character_rig:LeftArm",
    "Right Arm": "character_rig:RightArm",
    "Left Leg": "character_rig:LeftUpLeg",
    "Right Leg": "character_rig:RightUpLeg",
    "Torso": "character_rig:Spine",
    "Head": "character_rig:Head",
    "Left Hand": "character_rig:LeftHand",
    "Right Hand": "character_rig:RightHand",
    "Left Foot": "character_rig:LeftFoot",
    "Right Foot": "character_rig:RightFoot"
}

# Get the armature object
armature = bpy.data.objects['Armature']

# Iterate through the generated limb objects and parent them to their corresponding bones
for limb_name, bone_name in limb_bones.items():
    # Find the generated limb object by name
    limb_object = bpy.data.objects.get(limb_name)
    if limb_object is None:
        print(f"Limb object {limb_name} not found, skipping...")
        continue
    
    # Set the parent of the limb to the armature and the corresponding bone
    limb_object.parent = armature
    limb_object.parent_type = 'BONE'
    limb_object.parent_bone = bone_name

print("Finished parenting limbs to bones.")