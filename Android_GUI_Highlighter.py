# Invokation: CLI python my_script <path_to_dir>
# -> outputs a dir in the same location this script is w/ annotated images
# XML Parsing: use xml.etree.elementTree ..... consider using the XPath support it has
# -> Need error handling for broken XML tags
# Drawing: create duplicate pngs with designated names
# -> Use Pillow (PIL fork) for drawing, pulling coords from XML
# Misc logic
# -> for each XML and PNG pair, have a check that both exist.

import sys
import os
from PIL import Image
import xml.etree.ElementTree as ET


'''
    Execution of script. Returns exit status. 
'''
def execute_script() -> bool:

    # get path to input from CLI
    if len(sys.argv) > 2:
        print("****** Incorrect invokation. Please use the following format: py Android_GUI_Highlighter.py <path_to_input_dir> *******")
        return False
    
    try:
        
        # setup input, output dirs
        input_dir = os.listdir(sys.argv[1])
        input_dir.sort()

        output_path = os.getcwd()
        output_dir = "Android_GUI_Highlighter_output"

        # clean output folder
        if output_dir in os.listdir(output_path):
            print("**** Output directory exists, cleaning. ****")

            for png in os.listdir(output_dir):
                to_del = os.path.join(output_dir, png)
                os.remove(to_del)
        else:
            print("**** Creating output directory. ****")
            os.mkdir(output_dir)

        print(f"**** Output directory created at: {os.path.join(output_path, output_dir)} ****")
        #iterate over files
        for file in input_dir:
            # print(file)

            if file[-4:] == ".xml": #is xml
                print("file is xml:", file)

                # copy new picture 
                png_name = file[:-4]
                #TODO: parse the xml for each png -> get the dict
                #TODO: make the new file in the output dir, and give it as well as the dict of coords to the draw_boxes funct


                

        return True

    except Exception as err:
        print("Encountered exception: ", err, "\nExiting program.")


'''
    Parses the XML metadata files.
    
    Input: the XML filename
    Output: dictionary of coordinates of form {1:[x1, y1, x2, y2], 2:[x1, y1, x2, y2], 3:[]}
'''
def parse_xml(filename: str) -> dict:
    tree = ET.parse()
    

'''
    Draws boxes on the pngs based on the metadata in their XMLs.

    Input: dictionary of coordinates to draw, and a path to the file in which to edit
    Output: boolean indicating success/failure
'''
def draw_boxes(coords: dict, file_to_draw: str) -> bool:
    #TODO: draw boxes on the image see ImageDraw.recatngle
    pass


def main():
    out = execute_script()
    print(f"****** Script executed successfully with exit code: { 1 if out else 0 }. Exiting... *******")
    exit(out)


if __name__ == "__main__":
    main()
