import bpy
import json
import os

# Function to create a bone with parent
def create_bone(armature, bone_name, head, tail, parent=None):
    bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit mode
    bone = armature.edit_bones.new(bone_name)
    bone.head = head
    bone.tail = tail
    if parent:
        bone.parent = parent
    return bone

# Load armature data from JSON
json_path = os.path.join(bpy.path.abspath("//"), "armatures_data.json")
with open(json_path, 'r') as json_file:
    armatures_data = json.load(json_file)

# Re-create armatures
for armature_name, bones_data in armatures_data.items():
    # Create a new armature
    bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0))
    armature = bpy.context.object.data
    armature_obj = bpy.context.object
    armature.name = armature_name

    # Delete the default bone called 'Bone'
    default_bone = armature.edit_bones.get('Bone')
    if default_bone:
        armature.edit_bones.remove(default_bone)

    # Create all bones from the JSON data
    bones_dict = {}  # Store references to bones by name
    for bone_name, bone_data in bones_data.items():
        head = bone_data['head_local']
        tail = bone_data['tail_local']
        parent_name = bone_data['parent']
        
        # Parent the bone if it has a parent
        parent_bone = bones_dict.get(parent_name) if parent_name else None
        bone = create_bone(armature, bone_name, head, tail, parent=parent_bone)
        bones_dict[bone_name] = bone
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

print("Armatures regenerated from JSON without extraneous bones.")