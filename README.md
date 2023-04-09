### <h3 align="center">The Amari Project</h3>

The Amari Project is a novel research project that explores the possibilities and challenges of Stable-Diffusion and Textual Inversion as techniques for creating and simulating artificial identities through automation. It also examines the implications of this technology for the future of fake news and culture.

<p align="center"><img src="https://github.com/originates/the-amari-project/blob/main/github%20images/kramerfaces.gif?raw=true" alt="It does kind of seem like something Kramer might do.">
<br><br>

The Amari Project consists of two main components: [`ASDF (AMARI SD FaceMiner)`](AMARI%20SD%20FaceMiner) and [`imageTransformer.py`](imageTransformer.py). ASDF is a bash script that automates the process of generating and filtering face images from a text prompt using Stable-Diffusion. imageTransformer is a Python script that copies, rescales, and renames the images produced by ASDF for further processing.

ASDF works as follows:

- It takes a text prompt as input and uses Stable-Diffusion to generate face images based on the prompt. The model used for this step is sd-v1-4.ckpt, which is trained on a large dataset of face images.
- It uses [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) and [GFPGAN](https://github.com/TencentARC/GFPGAN) to upscale the images and enhance the facial features. These are two state-of-the-art models for super-resolution and face restoration, respectively.
- It uses [Face Recognition](https://github.com/ageitgey/face_recognition) to compare the upscaled images to a set of images called sim-group, which contains the most similar images to the target face.
- Face Recognition is also used to determine the average similarity of all the images within the sim-group and remove images if they become less similar to the group as new images are included.

The Face Recognition program works by comparing 2 images and outputting a number between 0 to 1 with 0 being perfectly similar and 1 being not at all similar. The default tolerance level for deciding if 2 faces are the same is <=0.60. Based on visual inspection, 0.60 was not strict enough and 0.40 seemed to be a more reasonable acceptable tolerance level. This number would be referred to as the image's Sim-Score, short for similarity score.


## Putting an AI Generated Face to a Name.

<br>After mining for faces for many hours—312 images with a <=0.40 sim-score to each other had been created. There was also approximately 3900 images that were 'almost' considered the same person
<br>

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
 
The default textual-inversion settings were used for training using `sd-v1-4.ckpt`

The associated config yaml files used can be found [here](https://github.com/originates/the-amari-project/tree/main/configs/the%20amari%20project/textual%20inversion)

The specific command used:
 

     python3 ./main.py --base ./configs/stable-diffusion/v1-finetune.yaml \
                  -t \                                             
                  --actual_resume ./models/ldm/stable-diffusion-v1/model.ckpt \                                             
                  -n amari \                                       
                  --gpus 0,1 \                                            
                  --data_root /home/user/ai/trainingimages/ \                                           
                  --init_word 'woman'

  
<br><br>
## Prompting Stable-Diffusion for *

<br>The following commands and prompts were used to test the trained Amari models using [lstein's implementation of Stable-Diffusion](https://github.com/lstein/stable-diffusion) (now known as InvokeAI).

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

<br><br>

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

Number of images in a training set seemingly affects the average sim-score of faces produced by the trained model
 
It is shown that a single epoch completed by group a-312 produced more favorable results versus c-4's 77 total epochs.
 
<br><br><br><br><br><br>
 
## Final Thoughts about the Amari Project

In this project, I demonstrated the feasibility and the limitations of Stable-Diffusion and Textual Inversion as techniques for generating and simulating synthetic identities through automation and we found that:

- Stable-Diffusion can produce faces that are very similar to each other given enough time and iterations.
- Textual Inversion can be used to create trained models of a specific face by using a few reference images.
- A trained face model that uses more than the recommended number of 3-5 images will produce faces that are more faithful to the original face than a model that uses fewer images, under the same training settings and steps.
 

I also identified some limitations and future directions for this project. For instance:


- I used the default imagenet_templates for Textual Inversion, but according to https://github.com/rinongal/textual_inversion/issues/59#issuecomment-1239210198, they can have an impact on the training process. It would be interesting to experiment with different prompts and see how they affect the output images.
- I did not have a reliable way of measuring the similarity between the generated faces and the reference face. We used a sim-score metric, but it may not capture all the nuances and variations of human faces. A more robust and comprehensive evaluation method is needed.
- I noticed that some hairstyles were not upscaled properly by ASDF, which uses Real-ESRGAN and GFPGAN. This may indicate a training bias or a limitation of these models.
- I only tested a few prompts for generating faces using Stable-Diffusion. There may be other prompts that can produce better or more interesting results.
<br><br>

## The Future

I contend that this technology has profound implications for the future of fake news and culture. It can already be leveraged to create realistic and persuasive fake images that can be utilized for various purposes, such as propaganda, misinformation, and social engineering. The automation of modeling a synthetic identity will make it effortless for malicious actors to generate an individual in infinite settings which will make these identities even more believable. Therefore, we need to be aware of these risks and develop suitable safeguards to prevent misuse and abuse of this technology.
 

