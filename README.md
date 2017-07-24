# MSCOCO
The official MSCOCO API is hard to understand for me.
This script create a image for semantic/instance segmentation and object detection.
<br />
### how to use
step1.<br>
glone the official API

```
git clone https://github.com/rkuga/MSCOCO.git
cd MSCOCO
git clone https://github.com/pdollar/coco.git
```
<br />
step2.<br />
make __init__.py
```
vim coco/__init__.py
vim coco/PythonAPI/__init__.py
```
<br />
step3.<br />
download the dataset<br>
your data_dir is<br>
yourpath|---annotations<br>
　　　　　　　|---train2014<br>
　　　　　　　|---val2014<br>
<br />
step4.<br />
if your need instance segmentations
```
python coco.py --data_dir yourpath --data_type train --mode instances
```
<br />
  
if your need semantic segmentations
```
python coco.py --data_dir yourpath --data_type train --mode semantics
```
also create categorical image  
<br /> 
  
if your need bounding boxs
```
python coco.py --data_dir yourpath --data_type train --mode bboxs
```
Bbox's color means its object class  
<br />
  
takes so much time.

