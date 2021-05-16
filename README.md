LPR-for-Chinese-Plate
---------------------

Licence Plate Recognition for Chinese Plate : Authors: N18927927 Shuwei
Zheng, N12971419 Junsong Xin

### Intriduction:

The Automatic License Plate Recognition is a challenging and important
task in many fields: the traffic management, digital security
surveillance, parking management and some other applications. Due to
many factors’ affect, it is a tough task: the different weather
conditions, the unclear image, poor lighting conditions, different types
of license plates (such as license plates from different countries) [1]
And for Chinese license plate recognition, it is even more challenging:
It will have letters in different language, and is more complex than the
English letters or number digits.

In this project, we build our own license plate recognition system using
the deep learning knowledge. By training our network, it can find out
the license plate of the car in the picture, then segment the license
plate into several single letters and digits. After that by using our
training network, we can classify each digit and find out the exactly
license plate number.

### Environment and Commands:

Python 3.7, install requirement

    pip install -r requirement.txt

### How to run:

Detecte licence plate

    python detector.py --image test.jpg

Train recognition model

    python main.py -mode train -d dataset

Recognize licence plate

    python main.py -mode predict -i test_out_plate.jpg -model mlp.pkl

### Explanation of the output:

-   'hu' stands for '沪'
-   'jing' stands for '京'
-   'min' stands for '闽'
-   'su' stands for '苏'
-   'yue' stands for '粤'
-   'zhe' stands for '浙'

### Reference:

Our model is base on: [ANPR](https://github.com/GuiltyNeuron/ANPR) 
