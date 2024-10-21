import bpy
import json
import os

# Function to collect bone information
def collect_bone_info(armature):
    bones_data = {}
    
    # Loop through all bones in the armature
    for bone in armature.bones:
        bone_info = {
            "name": bone.name,
            "head_local": list(bone.head_local),
            "tail_local": list(bone.tail_local),
            "parent": bone.parent.name if bone.parent else None
        }
        bones_data[bone.name] = bone_info
    
    return bones_data

# Collect all armature data
all_armatures_data = {}

# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    # Check if the object is an armature
    if obj.type == 'ARMATURE':
        armature_data = obj.data
        
        # Switch to pose mode to ensure we're capturing the correct bone info
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='POSE')
        
        # Collect bone data
        bones_data = collect_bone_info(armature_data)
        all_armatures_data[obj.name] = bones_data
        
        # Switch back to object mode after collecting
        bpy.ops.object.mode_set(mode='OBJECT')

# Define the path where the JSON file will be saved (current Blender project directory)
output_path = os.path.join(bpy.path.abspath("//"), "armatures_data.json")

# Save the armature data to a JSON file
with open(output_path, 'w') as json_file:
    json.dump(all_armatures_data, json_file, indent=4)

print(f"Armature data saved to {output_path}")