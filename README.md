# MSCOCO
The official MSCOCO API is hard to use for me.  
This script creates images for semantic/instance segmentation, object detection and image caption.  
  
## how to use
  
### step1.  
clone the official API

```
git clone https://github.com/rkuga/MSCOCO.git
cd MSCOCO
git clone https://github.com/pdollar/coco.git
```

### step2.  
make __init__.py    
```
vim coco/__init__.py
vim coco/PythonAPI/__init__.py
```

### step3.  
download the dataset<br>
your data_dir is<br>
yourpath|---annotations<br>
　　　　　　　|---train2014<br>
　　　　　　　|---val2014<br>
  
### step4.  
for instance segmentations
```
python coco.py --data_dir yourpath --data_type train --mode instances
```

 
for semantic segmentations
```
python coco.py --data_dir yourpath --data_type train --mode semantics
```
with categorical images
  
  
for bounding boxs
```
python coco.py --data_dir yourpath --data_type train --mode bboxs
```
Bbox's color means its object class  
  

for captions
```
python coco.py --data_dir yourpath --data_type train --mode captions
```
  
  
  

instances mode takes so much time.

