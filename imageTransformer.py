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
#
#  this script runs a bash command to rename the files to random characters.
#
# ---------------------------------------------------------------------------

import torch
import torchvision.transforms as T
from PIL import Image
import uuid
import os, random
import numpy as np
import sys
import time


# Defining Functions
# ---------------------------------------------------------------------------

def confirm_prompt(question: str) -> bool:
    reply = None
    while reply not in ("continue", "exit"):
        reply = input(f"{question} (continue/exit): ").casefold()
    return (reply == "continue")


def confirmed_Transform(img_input, img_output):
    files = os.listdir(img_input)
    random_files = np.random.choice(files, int(len(files)))

    for x in random_files:
        thefile = (img_input + f'/{x}')
        print(thefile)
        img = Image.open(thefile)

    #-----------------------------------------------

    #if you want your images to be randomly resized and then cropped use
        #transform = T.RandomResizedCrop((512,512))

        transform = T.RandomCrop((512,512))

    #-----------------------------------------------

        img = transform(img)
        img.save(userinputs[1] + f"/{x}")

    time.sleep(0.5)

    # if not using png images: change 'png' to the image extension you are working with in the following command to rename images that aren't pngs.
    # (or modify to work with any image extension if you are so bold)
    bashRename = 'wait; for file in "' + img_output + '/"*.jpeg; do mv -- "$file" "$(mktemp --dry-run "' + img_output + '/XXXXXXXXXXX.jpeg")"; done'

    os.system(bashRename)

    print("\nAll image transformations complete.\nTransformed images can be found in: " + userinputs[1] + "\n")


def exit_script():

    return "\nuser has gracefully exited imageTransformer.py!\n"


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
reply = confirm_prompt("Please confirm your input and output directories and then type")

if reply != False:

    confirmed_Transform(userinputs[0], userinputs[1])

else:

    print(exit_script())
