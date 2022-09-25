#!/usr/bin/env python
#
#
#                      imageTransformer.py
#        https://github.com/originates/the-amari-project/
# 
#
# ---------------------------------------------------------------------------
#
#  Preprocess all images in a directory to be used for textual inversion.
#
#  copies images in a directory
#  crops images to 512x512 and saves them to outImages directory
#
# ---------------------------------------------------------------------------
#
#  usage:
#
#  python imagecrop.py '/path/to/input/images/' '/path/to/output/images/'
#
# ---------------------------------------------------------------------------


# import required libraries
import torch
import torchvision.transforms as T
from PIL import Image
import uuid
import os, random
import numpy as np
import sys
import time
import string

#--------------------------------------------------------------------------------------------
#------------------------------- Defining Functions -----------------------------------------
#--------------------------------------------------------------------------------------------

def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ").casefold()
    return (reply == "y")

#--------------------------------------------------------------------------------------------

def confirmed_Transform(img_input, img_output):

    try:
    
        #random_files = np.random.choice(files, int(len(files)))

        for file_name in os.listdir(img_input):

            thefile = os.path.join(img_input,file_name)
            thenewfile = os.path.join(img_output,file_name) 

            print(thefile)

            img = Image.open(thefile)
            img_ext = img.format
        
            #get image width and height
            img_width = img.size[0]
            img_height = img.size[1]
            
            
            #the square that will be cropped is determined by the size of the image
            #with the max size being the smaller of width and height
            if img_width > img_height:
                square_max = img_height
            else:
                square_max = img_width
            

            if square_max <= 512:
                #set a static size for the image if height is less than 512px
                img_sq = square_max
            else:   
                #otherwise generate a number between 512 and img_height
                #to determine the size of the square size to crop
                #this hopefully will allow for finer details to be
                #included into the trained model
                img_sq = random.randint(512,square_max)

            print("?")
            #define a Transform command to crop a square image 
            #in a random location with size img_sq x img_sq
            transform = T.RandomCrop((img_sq,img_sq))
            #perform transformation
            img = transform(img)
            #define resize transformation
            resize = T.Resize((512,512))

            #perform resize transformation
            img = resize(img)
            print("?")
            #saves newly transformed image into the output directory
            #defined in the user commandline argument
            img.save(thenewfile)

        #let your computer take a breather; it deserves it.
        time.sleep(0.5)
        
        os.chdir(img_output)
	
        for count, f in enumerate(os.listdir()):
            randName = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=9))
            f_name, f_ext = os.path.splitext(f)
            f_name = randName
            new_name = f'{f_name}{f_ext}'
            os.rename(f, new_name)


        #previous command where python is used to call a bash command to rename files
        #bashRename = 'wait; for file in "' + img_output + '/"*; do ext=${file##*.}; mv -- "$file" "$(mktemp --dry-run "' + img_output + '/XXXXXXXXXXX.$ext")"; done'
        #run bash command
        #os.system(bashRename)

        print("\nImage transformations complete.\nTransformed images can be found in: " + img_output)
        print(exit_script())
                    
    except:
        
        #exiting script: 
        print("Error: During transformation step.")
        print("Please verify that your directories and/or files exist")
        print("and/or remove non-image files")
        print(exit_script())      

#--------------------------------------------------------------------------------------------

def exit_script():

    return "\nuser has 'gracefully' exited imageTransformer.py!\n"

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

inImages=sys.argv[1]
outImages=sys.argv[2]

userinputs = [inImages, outImages];

for userinput in range(len(userinputs)):
    if userinputs[userinput][-1] == "/":
        userinputs[userinput] = userinputs[userinput][:-1]

print("\n----------------------------------------")
print("\n   Input file directory  :  " + userinputs[0])
print("  Output file directory  :  " + userinputs[1])
print("\n----------------------------------------\n")

#allow user to reverse a potential user error
reply = confirm_prompt("Please confirm your input and output directories. Enter 'y' to proceed ")

if reply != False:

    confirmed_Transform(userinputs[0], userinputs[1])

else:

    print(exit_script())

