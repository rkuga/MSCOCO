# MSCOCO
The official MSCOCO API is hard to understand for me.
This script create a image for semantic/instance segmentation and object detection.

### how to use
step1.
glone the official API

```
git clone https://github.com/rkuga/MSCOCO.git
cd MSCOCO
git clone https://github.com/pdollar/coco.git
```

step2.
make __init__.py
```vim coco/__init__.py
   vim coco/PythonAPI/__init__.py
```

step3.
download the dataset
your data_dir is
yourpath|---annotations
        |---train2014
        |---val2014
   
step4.
if your need instance segmentations
```
python coco.py --data_dir yourpath --data_type train --mode instances
```
if your need bounding boxs
```
python coco.py --data_dir yourpath --data_type train --mode bboxs
```
if your need semantic segmentations
```
python coco.py --data_dir yourpath --data_type train --mode semantics
```



