# -*- coding: utf-8 -*-
from main_ui import XmlEditorGUI

def test():
    xml_editor = XmlEditorGUI()
    xml_editor.loadSpecificationXml()
    assert xml_editor.specification_xml_path is not None
    assert xml_editor.specification_xml_structure is not None

    xml_editor.loadDataXml()
    assert xml_editor.data_xml_path is not None

    initial_text = xml_editor.textEdit.toPlainText()
    xml_editor.saveDataXml()
    with open(xml_editor.data_xml_path, 'r') as file:
        saved_text = file.read()
    assert initial_text == saved_text


    print("All tests passed successfully.")

if __name__ == "__main__":
    test()