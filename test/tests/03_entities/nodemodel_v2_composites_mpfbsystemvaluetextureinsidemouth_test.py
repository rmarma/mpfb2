import bpy, os
from pytest import approx
from mpfb.services.objectservice import ObjectService
from mpfb.services.nodeservice import NodeService
from mpfb.entities.nodemodel.v2.composites.nodewrappermpfbsystemvaluetextureinsidemouth import NodeWrapperMpfbSystemValueTextureInsideMouth

def test_composite_is_available():
    assert NodeWrapperMpfbSystemValueTextureInsideMouth

def test_composite_can_create_instance():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = NodeWrapperMpfbSystemValueTextureInsideMouth.create_instance(node_tree)
    assert node
    assert node.node_tree.name == "NodeWrapperMpfbSystemValueTextureInsideMouth"
    assert "RGB to BW" in node.node_tree.nodes
    assert "Texture Coordinate" in node.node_tree.nodes
    assert "Group Output" in node.node_tree.nodes
    assert "Group Input" in node.node_tree.nodes
    assert "System texture" in node.node_tree.nodes
    has_link_to_output = False
    for link in node.node_tree.links:
        if link.to_node.name == "Group Output":
            has_link_to_output = True
    assert has_link_to_output
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_composite_validate_tree():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = NodeWrapperMpfbSystemValueTextureInsideMouth.create_instance(node_tree)
    assert NodeWrapperMpfbSystemValueTextureInsideMouth.validate_tree_against_original_def()
    node_tree.nodes.remove(node)
    NodeService.destroy_node_tree(node_tree)

def test_correct_filename():
    node_tree_name = ObjectService.random_name()
    node_tree = NodeService.create_node_tree(node_tree_name)
    node = NodeWrapperMpfbSystemValueTextureInsideMouth.create_instance(node_tree)
    group_tree = node.node_tree
    imgtex = NodeService.find_first_node_by_type_name(group_tree, "ShaderNodeTexImage")
    assert imgtex
    assert imgtex.image
    assert os.path.basename(imgtex.image.filepath) == "mpfb_inside-mouth.jpg"
    assert os.path.exists(imgtex.image.filepath)