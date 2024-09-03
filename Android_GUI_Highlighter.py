# py .\Android_GUI_Highlighter.py Programming-Assignment-Data
import sys
import os
from PIL import Image, ImageDraw
from lxml import etree
import re
import shutil

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

            if file[-4:] == ".xml":
                print("*** Working on file: ", file)

                # copy the associated picture into output directory
                png_name = str(file[:-4] + ".png")
                shutil.copy2(os.path.join(sys.argv[1], png_name), os.path.join(output_path, output_dir))

                # get coordinates and then draw on them
                xml_coords = parse_xml(os.path.join(sys.argv[1], file))
                draw_boxes(xml_coords, os.path.join(output_path, output_dir, png_name))

                print("*** File complete. ***")

        return True

    except Exception as err:
        print("Encountered exception: ", err, "\nExiting program.")


'''
    Parses the XML metadata files.
    
    Input: the XML filename
    Output: list of coordinates of form [[x1, y1, x2, y2], [x1, y1, x2, y2]]
'''
def parse_xml(filename: str) -> list:
    try:
        # recover tag helps with broken XML tags
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(filename, parser)

        # get coords from xml attribute
        clickable_list = tree.findall(".//node[@clickable='true']")
        coords = []
        
        # turn str of form '[x1,y1][x2,y2]' into [x1,y1,x2,y2]
        for elem in clickable_list:
            str_coords = elem.attrib['bounds']

            points = re.findall(r'\d+', str_coords) #god I hate regex
            coordinates = [int(num) for num in points]

            coords.append(coordinates)
        
        return coords

    except Exception as err:
        print(err)
        print("Encountered exception ", err, " while parsing xml. Exiting program.")
        exit(1)


'''
    Draws boxes on the pngs based on the metadata in their XMLs.

    Input: dictionary of coordinates to draw, and a path to the file in which to edit
    Output: boolean indicating success/failure
'''
def draw_boxes(coords: list, file_to_draw: str):
    try:
        print("** Drawing on file: ", file_to_draw)

        img = Image.open(file_to_draw)
        draw = ImageDraw.Draw(img) 

        # draw each rectangle
        for item in coords:
            draw.rectangle(xy = item, 
                           outline = (255, 255, 0), 
                           width = 10)
            
        img.save(file_to_draw)
        img.close()

    except Exception as err:
        print(err)
        print("Encountered exception ", err, " while drawing boxes. Exiting program.")
        exit(1)


def main():
    out = execute_script()
    print(f"****** Script executed with exit code: { 0 if out else 1 }. Exiting... *******")
    exit(out)


if __name__ == "__main__":
    main()
