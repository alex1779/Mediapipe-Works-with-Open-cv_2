# Mediapipe Works
From: https://google.github.io/mediapipe/

## Installation on Windows using Anaconda
```
conda create -n Mediapipe-Works-with-Open-cv_2 -y && conda activate Mediapipe-Works-with-Open-cv_2 && conda install python=3.9.7 -y
git clone https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2.git
cd Mediapipe-Works-with-Open-cv_2
pip install -r requirements.txt
```

## How to run Aligned Face Horizontal

```
python alignedFaceHorizontal_image.py -i input/test1.jpg
```
 *** looks like below

![Example1](https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2/blob/master/imgs/alignedFaceHorizontal_image_example1.jpg)
![Example2](https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2/blob/master/imgs/alignedFaceHorizontal_image_example2.jpg)
![Example3](https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2/blob/master/imgs/alignedFaceHorizontal_image_example3.jpg)

```
you can see the result in 'output' folder.
```


## How to run Face Aligned Without Background

```
python face_aligned_without_background.py -i input/test1.jpg
```
 *** looks like below

![Example1](https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2/blob/master/imgs/face_aligned_without_background_example1.jpg)
![Example2](https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2/blob/master/imgs/face_aligned_without_background_example2.jpg)
![Example3](https://github.com/alex1779/Mediapipe-Works-with-Open-cv_2/blob/master/imgs/face_aligned_without_background_example3.jpg)

```
you can see the result in 'output' folder.
```





## License

Many parts taken from the cpp implementation from github.com/google/mediapipe

Copyright 2020 The MediaPipe Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.






