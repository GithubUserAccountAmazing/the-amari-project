note: this repository will most likely be renamed to Stable-Diffusion-Tests-and-Data (or something similar) with The Amari Project becoming a sub directory of the newly named repository. There are several more Stable-Diffusion related tests that I think would be interesting to perform and learn from. Once new tests and data are created they will be merged into this repository.

---

<br><br><p align="center"><img src="https://github.com/originates/the-amari-project/blob/main/github%20images/amarifaces.gif?raw=true" alt="The Amari Project"></p>

### <h3 align="center">The Amari Project</h3>

#### <p align="center">creating and recognizing an artificial human face using machine learning</p>
<br> <br>

----

<br>

## **Table of Contents**

1. [Introduction (where I try to convince the reader that generating thousands of faces isn't weird)](#introduction)
2. [Using Stable-Diffusion to Mine for a Specific Face](#using-stable-diffusion-to-mine-for-a-specific-face)
3. [Putting an AI generated Face to a Name](#putting-an-ai-generated-face-to-a-name)
4. [Textual Inversion Testing and Training](#textual-inversion-testing-and-training)
5. [Prompting Stable Diffusion for *](#prompting-stable-diffusion-for-)
6. [Analyzing the Results](#analyzing-the-results)
7. [Final Thoughts about the Amari Project](#final-thoughts-about-the-amari-project)

<br>

## Introduction

<br>After learning about [textual inversion](https://github.com/rinongal/textual_inversion) 2 of my first thoughts were:

- could this be used to teach Stable-Diffusion (SD) a specific person/face?
- and if I wanted to test this idea, how could I go about it? 


I thought about using my face as training data but ultimately decided against it for 2 reasons.

- I wasn't quite ready to have SD learn what I looked like.
- if I wanted to share this publicly, I didn't particularly want to share a trained model of my face online.


I considered using someone else’s face but again, decided against this idea as well.

- I did not want to use someone's face without permission
- I generally wanted to avoid explaining to someone why I wanted to use their face for a machine learning project.


If the potential to use my face or someone else’s face was out of the question, how could I possibly have a face to use as training data for SD? 

What if I used SD itself to generate faces? <br><br>


## Using Stable-Diffusion to Mine for a Specific Face

<p align="center"><img src="https://github.com/originates/the-amari-project/blob/main/github%20images/kramerfaces.gif?raw=true" alt="It does kind of seem like something Kramer might do.">
<br><br>

Generating faces in SD can be incredibly hit or miss in terms of the quality of the image produced. 

To mitigate image quality issues-a bash script later titled the AMARI SD FaceMiner (ASDF) was created. 

ASDF is composed of 5 general steps

1. Generate face images from a prompt using SD.
2. AI upscale the images and facial features using [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) and [GFPGAN](https://github.com/TencentARC/GFPGAN).
3. Compare the upscaled images to a set of images, labeled 'sim-group' using [Face Recognition](https://github.com/ageitgey/face_recognition)
4. Sort the images based on how similar they are to the sim-group. If the image is considered very similar the image will itself be included into the sim-group.
5. Use Face Recognition to determine the average similarity of all the images within the sim-group and remove images if they become less similar to the group as new images are included.

The Face Recognition program works by comparing 2 images and outputting a number between 0 to 1 with 0 being perfectly similar and 1 being not at all similar. The default tolerance level for deciding if 2 faces are the same is <=0.60. Judging from visual inspection, 0.60 was not strict enough and 0.40 seemed to be a more reasonable acceptable tolerance level. This number would be referred to as the image's Sim-Score, short for similarity score.<br><br>  


## Putting an AI Generated Face to a Name.

<br>After mining for faces for many hours—312 images with a <=0.40 sim-score to each other had been created. There was also approximately 3900 images that were 'almost' considered the same person

While not particularly important-I felt the face being generated needed a name. The name Amari was chosen since it had several meanings such as eternal and immortal. Thus, the name of the project, the bash script, and the face had been born.

Finally, [`imageTransformer.py`](imageTransformer.py) was written to copy, rescale, and rename the images produced during the face mining step.<br><br>

## Textual Inversion Testing and Training

<br>The textual inversion paper recommends 3-5 images being used to train with, however, the paper only focuses using textual inversion on objects and art styles and never once dives into the concept of creating artificial humans. I wanted to test textual inversion using the recommended number of images as well as larger groups of images—I ended up creating 3 different training groups.

 <img align="right" src="https://github.com/originates/the-amari-project/blob/main/github%20images/total_epochs_at_global_step_50n.png?raw=true" width="45%">
 
 | training group | Total Images |
 |:---:|:---:|
 |&nbsp;&nbsp;a_312&nbsp;&nbsp;| &nbsp;&nbsp;312 (all) images &nbsp;&nbsp;|
 |&nbsp;&nbsp;b_11&nbsp;&nbsp;| &nbsp;&nbsp;11 images&nbsp;&nbsp; |
 |&nbsp;&nbsp;c_4&nbsp;&nbsp;| &nbsp;&nbsp;4 images&nbsp;&nbsp; |   

I wanted to see what differences would arise in the images produced in all 3 groups for the same amount of training using the same prompt and seed values. I also wanted to view the data that is created during training to get an understanding of how the number of images in the group effects the actual training.

 
I trained each group until approximately 15,500 steps. This was the total amount of steps it took for group a_312 to reach a single completed epoch.

 <br><br>
 
The default textual-inversion settings were used for training with the specific command being.
 
 

     python3 ./main.py --base ./configs/stable-diffusion/v1-finetune.yaml \
                  -t \                                             
                  --actual_resume ./models/ldm/stable-diffusion-v1/model.ckpt \                                             
                  -n amari \                                       
                  --gpus 0,1 \                                            
                  --data_root /home/user/ai/trainingimages/ \                                           
                  --init_word 'woman'

 
 [more information about the training data will be available here soon] :)
  
<br><br>
## Prompting Stable-Diffusion for *

<br>The following commands and prompts were used to test the trained Amari models using [lstein's implementation of Stable-Diffusion](https://github.com/lstein/stable-diffusion).

&nbsp;&nbsp;
|Commands|Prompts|
| --- | --- |
|<table><tr><th>Command ID</th><th>Stable-Diffusion Command</th></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[sd1]</td><td>'prompt' -s250 -W512 -H512 -C7.5 -Ak_lms -S335728730</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[sd2]</td><td>'prompt' -s250 -W512 -H512 -C7.5 -Ak_lms -S691007764</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[sd3]</td><td>'prompt' -s250 -W512 -H512 -C7.5 -Ak_lms -S1295044561</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[sd4]</td><td>'prompt' -s250 -W512 -H512 -C7.5 -Ak_lms -S2565311105</td></tr><tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[sd5]</td><td>'prompt' -s250 -W512 -H512 -C7.5 -Ak_lms -S1995053400</td></tr></table>|<table><tr><td>&nbsp;&nbsp;&nbsp;'a photo of amari'</td></tr><tr><td>&nbsp;&nbsp;&nbsp;'a photograph of amari walking outside'</td></tr><tr><td>&nbsp;&nbsp;&nbsp;'a side profile image of amari'</td></tr><tr><td>&nbsp;&nbsp;&nbsp;'an extremely detailed photograph of amari'</td></tr></table>|


<br>A control (ctrl) group was included to go along with the 3 trained groups. 
<br>The ctrl group images are generated without the use of any trained model of Amari.
<br>
<br>20 images were produced for each group, resulting in 80 test images in total.
<br>To get an idea of the quality of imaged produced during these tests a set of images from each prompt using the same Command ID can be found below.<br>
The training group and sim-score are both shown beneath each image.<br>

### <p align="center">'a photo of amari' &nbsp;&nbsp; [sd3]</p>

|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photo_of_amari_e13w.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photo_of_amari_GGxZ.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photo_of_amari_WlO0.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photo_of_amari_DFnC.png?raw=true" width="100%">|
|:---:|:---:|:---:|:---:|
|<b><p align="center">a-312 : 0.4181</p>|<b><p align="center">b-11 : 0.4235</p>|<b><p align="center">c-4 : 0.4480</p>|<b><p align="center">ctrl : 0.8654</p>|


### <p align="center">'a photograph of amari walking outside' &nbsp;&nbsp; [sd4]</p>

|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photograph_of_amari_walking_outside_Eefb.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photograph_of_amari_walking_outside_3VHE.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photograph_of_amari_walking_outside_AYKO.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_photograph_of_amari_walking_outside_Zq6F.png?raw=true" width="100%">|
|:---:|:---:|:---:|:---:|
|<b><p align="center">a-312 : 0.3952*</p>|<b><p align="center">b-11 : 0.4354</p>|<b><p align="center">c-4 : 0.5118</p>|<b><p align="center">ctrl : 0.7429</p>|


### <p align="center">'a side profile image of amari' &nbsp;&nbsp; [sd2]</p>

|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_side_profile_image_of_amari_ojC9.png" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_side_profile_image_of_amari_0Af3.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_side_profile_image_of_amari_ZIB0.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/a_side_profile_image_of_amari_a9HD.png?raw=true" width="100%">|
|:---:|:---:|:---:|:---:|
|<b><p align="center">a-312 : 0.4767</p>|<b><p align="center">b-11 : 0.4574</p>|<b><p align="center">c-4 : 0.5734</p>|<b><p align="center">ctrl : no face found</p>|


### <p align="center">'an extremely detailed photograph of amari' &nbsp;&nbsp; [sd1] </p>

|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/an_extremely_detailed_photograph_of_amari_uY1K.png" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/an_extremely_detailed_photograph_of_amari_gqjs.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/an_extremely_detailed_photograph_of_amari_vg7k.png?raw=true" width="100%">|<img src="https://github.com/originates/the-amari-project/blob/main/github%20images/an_extremely_detailed_photograph_of_amari_tYWO.png?raw=true" width="100%">|
|:---:|:---:|:---:|:---:|
|<b><p align="center">a-312 : 0.4452</p>|<b><p align="center">b-11 : 0.4802</p>|<b><p align="center">c-4 : 0.4735</p>|<b><p align="center">ctrl : 0.7520</p>|

*This is the only image out of 80 that had a sim-score <=0.40. However, the realism of this image is arguably not great. The image also does not reflect the prompt idea of 'walking outside.'
 
<br>For the full set of 80 images see the included amari_test_images.zip<br><br>

## Analyzing the Results

<br>

<img align="right" src="https://github.com/originates/the-amari-project/blob/main/github%20images/Total_Faces_Not_Found_per_Prompt.png?raw=true" width="48%">
It was quickly noticed that the 'side profile image of amari' prompt led to some problems in terms of located faces. It seems there is a limitation to Facial Recognition when a face was rotated. Furthermore, it was noted that the c_4 group also had trouble generating a face that could be found with 3 faces not found in total. the ctrl group produced 6 images where a face could not be found. Images where a face could not be found were not included in the following sim-test data.

<br><br><br><br>
 
<img align="left" src="https://github.com/originates/the-amari-project/blob/main/github%20images/average_sim_score_per_prompt.png?raw=true" width="48%"> 

<br><br><br><br>

Outside of images where a face was not found-the individual prompts had little effect on the sim-scores for each training group.
 
<br><br><br><br>
 
<img align="right" src="https://github.com/originates/the-amari-project/blob/main/github%20images/Group_Sim_Scores_for_all_Prompts.png?raw=true" width="48%">

<br><br><br><br>

Number of images in a training group will determine the sim-scores for a generated image. A single completed a-312 epoch produced much better sim-scores versus c-4's 77 total epochs.
 
<br><br><br><br><br><br>
 
 ## Final Thoughts about the Amari Project
 
 <br>
 
- It is indeed possible to generate faces via Stable-Diffusion that are very similar to each other.
- Textual Inversion may be used to create trained models of a specific face
- A trained face model that uses more than the reccommended amount of 3-5 images will produce faces more similar to the original faces on average.
 
 <br>

The default imagenet_templates were used during training and I am currently uncertain how modifying these prompts would alter the trained model.
 
It is unknown currently how an increase in training time would influence the results for the 3 training groups. I may in the future add more time to each group and post the results.

It's also currently unknown what the sim-scores of an actual collection of a real human face is-perhaps 0.40 is still too high. Also, it's very easy to consider that the idea of a 'sim-score' may not be the best way of determining if any single face should belong in a group of faces.

It was noticed that while using ASDF to generate faces—many of the images seemed to have been upscaled incorrectly when it came to certain hairstyles. This may be the result of Real-ESRGAN and/or GFPGAN displaying training bias. More research would need to be done to determine if that is indeed factual. Simple observation showed that straight hair was upscaled more appropriately than tightly coiled hairstyles. This resulted in the trained models having a high likelyhood of generated malformed hairstyles.

Outside of the prompts listed during the testing phase, this project did not look into using other prompts to produce faces. These images were also not upscaled after being generated. It is probable that higher quality faces could be produced with modified prompts and upscaling. I also did not look into using img2img to produce faces either. It is probable that img2img could be a powerful tool as well.

[more thoughts, data, charts, and files will be provided over the next several days]



