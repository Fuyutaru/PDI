import xml.etree.ElementTree as ET
import os

def compare_xml_structure(file1, file2):
    # Parse XML files
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)

    # Get root elements
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # Compare the structures recursively
    return compare_elements(root1, root2)

def compare_elements(elem1, elem2):
    # Check if elements have the same tag
    if elem1.tag != elem2.tag:
        return False

    # Check if elements have the same number of children
    if len(elem1) != len(elem2):
        return False

    # Recursively compare children
    for child1, child2 in zip(elem1, elem2):
        if not compare_elements(child1, child2):
            return False

    return True

# Test the function
current_directory = os.path.dirname(os.path.realpath(__file__))
rpath = "example/FullSpecif.xml"
dpath = "example/Data_FullSpecif.xml"
file1 = os.path.join(current_directory, rpath)
file2 = os.path.join(current_directory, dpath)

if compare_xml_structure(file1, file2):
    print("XML files have the same structure.")
else:
    print("XML files do not have the same structure.")
