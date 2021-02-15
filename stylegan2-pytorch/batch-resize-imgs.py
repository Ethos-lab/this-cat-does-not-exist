#!/usr/bin/env python
# coding: utf-8



'''
.cat file: 9 points (verified guaranteed)
x coord index: 1,3,5,7,9,11,13,15,17
y coord index: 2,4,6,8,10,12,14,16,18
example: 9 175 160 239 162 199 199 149 121 137 78 166 93 281 101 312 96 296 133 
Number of points (default is 9)
Left Eye
Right Eye
Mouth
Left Ear-1
Left Ear-2
Left Ear-3
Right Ear-1
Right Ear-2
-Right Ear-3
'''

import os


image_folder = r"D:\Bravo\git_repos\stylegan2-pytorch\datasets\cat-faces"

dest_folder= r"D:\Bravo\git_repos\stylegan2-pytorch\datasets\cat-faces-cropped"
#elements of img_list format: [image_path,new_filename,[x1,x2,...x9],[y1,y2,...y9]]
img_list=[]
for folder in os.listdir(image_folder):
    #for each subfolder
    fullfolder=os.path.join(image_folder,folder)
    for imgfn in os.listdir(fullfolder):
        if(imgfn.endswith(".jpg")):
            fullpath=os.path.join(fullfolder,imgfn)
            annopath=fullpath+".cat"
            with open(annopath,"r") as fp1:
                ln=fp1.read()
                pts=ln.split(" ")
                xcoord=[int(pts[i]) for i in range(1,18,2)]
                ycoord=[int(pts[i]) for i in range(2,19,2)]
            newimgfn="{}_{}".format(folder,imgfn)
            img_list.append([fullpath,newimgfn,xcoord,ycoord])
            
print(len(img_list))
for row in img_list[:10]:
    print(row)




from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


out_image_folder = dest_folder

IMG_SIZE=(256,256)
def get_face(img_info):
    #should return mean coord (center) of face
    x=img_info[2]
    y=img_info[3]
    midx=sum(x)/len(x)
    leftx=min(x)-midx*0.15
    rightx=max(x)+midx*0.15
    width=(rightx-leftx)
    bottomy=max(y)+40
    topy=bottomy-width
    return (x,y,leftx,topy,rightx,bottomy)

def crop_center(fn,destfn):
    im = Image.open(fn)
    width, height = im.size

    new_width = min(width,height)

    # Setting the points for cropped image 
    #crop from center
    left = (width-new_width)//2
    top = (height-new_width)//4
    right = left+new_width
    bottom = top+new_width
    im1 = im.crop((left, top, right, bottom))
    im1 = im1.resize(IMG_SIZE)
    im1.save(destfn)

    
def crop_by_range(fn,destfn,left, top, right, bottom):
    im = Image.open(fn)
    width, height = im.size
    if(left<0):#offset
        right+=(-1)*left
        left+=(-1)*left    #==0
    if(right>width):
        left-=(right-width)
        right-=(right-width)    #==width
    if(top<0):
        bottom+=(-1)*top
        top+=(-1)*top    # ==0
    if(bottom>height):
        top-=(bottom-height)
        bottom-=(bottom-height)    #==height
        
        
    im1 = im.crop((left, top, right, bottom))
    im1 = im1.resize(IMG_SIZE,Image.ANTIALIAS)
    im1.save(destfn,quality=90)
    return
idx=0
for img_info in tqdm(img_list[5:]):
    #crop_center(fn=os.path.join(image_folder,img),destfn=os.path.join(out_image_folder,img))
    #idx+=1
    fn=img_info[0]
    destfn=os.path.join(dest_folder,img_info[1])
    item = get_face(img_info)
    if(item is None):
        print("no face in {}".format(fn))
        continue
    (x,y,leftx,topy,rightx,bottomy)=item
    crop_by_range(fn,destfn,leftx,topy,rightx,bottomy)
    img = Image.open(fn)
    
    w,h=img.size
    dpi=200

    plt.figure(figsize=(w/dpi,h/dpi),dpi=dpi)
    fig, ax = plt.subplots(1,1)
    ax.imshow(img)
    ax.scatter(x,y,s=1,c='green')
    lx=np.linspace(0,w,1000)
    ly=np.linspace(topy,topy,1000)
    ax.scatter(lx,ly,s=1,c='red')
    lx=np.linspace(0,w,1000)
    ly=np.linspace(bottomy,bottomy,1000)
    ax.scatter(lx,ly,s=1,c='red')
    lx=np.linspace(0,h,1000)
    ly=np.linspace(leftx,leftx,1000)
    ax.scatter(ly,lx,s=1,c='red')
    lx=np.linspace(0,h,1000)
    ly=np.linspace(rightx,rightx,1000)
    ax.scatter(ly,lx,s=1,c='red')
    plt.show()
    break
print("all done.")



