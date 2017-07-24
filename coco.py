import coco.PythonAPI.pycocotools.coco as coco
import numpy as np
import cv2
import pylab
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import argparse
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import os

def SaveFigureAsImage(fileName, fig=None, **kwargs):
    ''' Save a Matplotlib figure as an image without borders or frames. (from https://gist.github.com/marquisthunder/ce4b2ede4c3786d0a5d7)
       Args:
            fileName (str): String that ends in .png etc.
            fig (Matplotlib figure instance): figure you want to save as the image
        Keyword Args:
            orig_size (tuple): width, height of the original image used to maintain 
            aspect ratio.
    '''
    fig_size = fig.get_size_inches()
    w,h = fig_size[0], fig_size[1]
    fig.patch.set_alpha(0)
    if kwargs.has_key('orig_size'): # Aspect ratio scaling if required
        w,h = kwargs['orig_size']
        w2,h2 = fig_size[0],fig_size[1]
        fig.set_size_inches([(w2/w)*w,(w2/w)*h])
        fig.set_dpi((w2/w)*fig.get_dpi())
    a=fig.gca()
    a.set_frame_on(False)
    a.set_xticks([]); a.set_yticks([])
    plt.axis('off')
    plt.xlim(0,h); plt.ylim(w,0)
    fig.savefig(fileName, transparent=True, bbox_inches='tight', \
                        pad_inches=0)

class MYCOCO(coco.COCO):
    def semantics(self, anns, dictionary, shape ,out_path, out_path2):
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """
        if len(anns) == 0:
            return 0
        new_img=np.zeros(shape, dtype=np.uint8)
        new_img2=np.zeros(shape[0:2], dtype=np.uint8)
        for ann in anns:
            c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]
            if 'segmentation' in ann:
                if type(ann['segmentation']) == list:
                    for seg in ann['segmentation']:
                        poly = np.array(seg).reshape((int(len(seg)/2), 2)).astype(np.int32)
                        index=int(np.where(np.array(dictionary["raw"])==ann["category_id"])[0])
                        rgb = dictionary["palette"][ann['category_id']-dictionary["sa"][index]]
                        cv2.fillPoly(new_img, pts =[poly], color=rgb)
                        cv2.fillPoly(new_img2, pts =[poly], color=ann['category_id']-dictionary["sa"][index])
                                              
        new_img=cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        
        cv2.imwrite(out_path+'COCO_'+args.data_type+'2014_%012d.png'%(ann['image_id']),new_img)
        cv2.imwrite(out_path2+'COCO_'+args.data_type+'2014_%012d.png'%(ann['image_id']),new_img2)

    def instances(self, anns, orig_size, out_path):
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """
        if len(anns) == 0:
            return 0
        for ann in anns:
            c = (np.random.random((1, 3))*0.6+0.4).tolist()[0]
            if 'segmentation' in ann:
                if type(ann['segmentation']) == list:
                    # polygon
                    for seg in ann['segmentation']:
                        poly = np.array(seg).reshape((int(len(seg)/2), 2)).astype(np.int32)
                        polygons.append(Polygon(poly))
                        color.append(c)
        p = PatchCollection(polygons, facecolor=color, linewidths=0, alpha=0.4)
        ax.add_collection(p)

        # only mask
        # bx=ax.get_figure()
        # SaveFigureAsImage(out_path+'COCO_'+args.data_type+'_mask_2014_%012d.png'%(ann['image_id']), bx, orig_size=orig_size[0:2] )
        
        # with boundary
        p = PatchCollection(polygons, facecolor='none', edgecolors=color, linewidths=2)
        ax.add_collection(p)
        SaveFigureAsImage(out_path+'COCO_'+args.data_type+'2014_%012d.png'%(ann['image_id']), plt.gcf(), orig_size=orig_size[0:2] )

    def bboxs(self, anns, dictionary, img, out_path):
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """
        if len(anns) == 0:
            return 0
        for ann in anns:
            if 'bbox' in ann:
                if ann['iscrowd']==0:
                    x, y, width, height = ann['bbox']
                    index=int(np.where(np.array(dictionary["raw"])==ann["category_id"])[0])
                    cv2.rectangle(img, (int(x),int(y)), (int(x+width),int(y+height)), tuple(dictionary["palette"][ann['category_id']-dictionary["sa"][index]]), 3)
        cv2.imwrite(out_path+'COCO_'+args.data_type+'2014_%012d.png'%(ann['image_id']),img)

    def captions(self, anns, out_path):
        """
        Display the specified annotations.
        :param anns (array of object): annotations to display
        :return: None
        """
        if len(anns) == 0:
            return 0
        for ann in anns:
            if 'bbox' in ann:
                if ann['iscrowd']==0:
                    x, y, width, height = ann['bbox']
                    index=int(np.where(np.array(dictionary["raw"])==ann["category_id"])[0])
                    cv2.rectangle(img, (int(x),int(y)), (int(x+width),int(y+height)), tuple(dictionary["palette"][ann['category_id']-dictionary["sa"][index]]), 3)
        cv2.imwrite(out_path+'COCO_'+args.data_type+'2014_%012d.png'%(ann['image_id']),img)


parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='bboxs', help='mode')
parser.add_argument('--data_type', type=str, default='train', help='train/val')
parser.add_argument('--data_dir', type=str, default='train', help='your dataset path')

args = parser.parse_args()


base_path=args.data_dir
if args.data_type=='train':
    json_path=base_path + '/annotations/instances_train2014.json'
    image_path=base_path + '/train2014'
elif args.data_type=='val':
    json_path=base_path + '/annotations/instances_val2014.json'
    image_path=base_path + '/val2014'

coco = MYCOCO(json_path)
imgIds = coco.getImgIds()
imgs = coco.loadImgs(imgIds)
categorie_ids=[]

if args.mode=='semantics':
    out_path=image_path+'_semantics/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_path2=image_path+'_semantics_categoryID/'
    if not os.path.exists(out_path2):
        os.makedirs(out_path2)
    with open('./coco.json', 'r') as fp:
        dictionary = json.load(fp)
    for img in imgs:
        image_id=img['id']
        I=cv2.imread(image_path+'/COCO_'+args.data_type+'2014_%012d.jpg'%(image_id))
        annIds = coco.getAnnIds(imgIds=image_id)
        anns = coco.loadAnns(annIds)
        coco.semantics(anns,dictionary,I.shape,out_path,out_path2)
elif args.mode=='instances':
    out_path=image_path+'_instances/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for img in imgs:
        image_id=img['id']
        I=cv2.imread(image_path+'/COCO_'+args.data_type+'2014_%012d.jpg'%(image_id))
        I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
        plt.clf()
        plt.figure(); plt.axis('off')
        plt.imshow(I)
        annIds = coco.getAnnIds(imgIds=image_id)
        anns = coco.loadAnns(annIds)
        ax=coco.instances(anns,I.shape,out_path)
        plt.close()
elif args.mode=='bboxs':
    out_path=image_path+'_bboxs/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open('./coco.json', 'r') as fp:
        dictionary = json.load(fp)
    for img in imgs:
        image_id=img['id']
        I=cv2.imread(image_path+'/COCO_'+args.data_type+'2014_%012d.jpg'%(image_id))
        annIds = coco.getAnnIds(imgIds=image_id)
        anns = coco.loadAnns(annIds)
        coco.bboxs(anns,dictionary,I,out_path)
elif args.mode=='captions':
    if args.data_type=='train':
        json_path=base_path + '/annotations/captions_train2014.json'
    elif args.data_type=='val':
        json_path=base_path + '/annotations/captions_val2014.json'
    out_path=image_path+'_captions/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    f = open(json_path,'r')
    json_data=json.load(f)
    f.close()
    caption_list=[]

    for caption_data in json_data['annotations']:
        image_id=caption_data['image_id']
        caption=caption_data['caption']

        caption = caption.replace('\n','').strip().lower()

        if caption[-1]=='.':
            caption=caption[0:-1]
        caption_tokens = caption
        caption_tokens += ' <EOS>'
        caption_list.append('COCO_'+args.data_type+'2014_%012d.jpg'%(image_id) +'/'+ caption_tokens)

    caption_list.sort()
    f = open(out_path+'captions.txt', 'w')
    for line in caption_list:
        f.write(str(line) + "\n")
    f.close()

