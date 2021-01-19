"""
@ author  : 刘思一 武玉琢 
@ date    : 2021.1.11
@ lesson  : 机电系统实验
"""
from cv2 import cv2
import numpy as np
import json
import time

# sub-functions needed
def test(test_list):  
    if len(test_list)==0:
        return False
    else: return True

def split(llst):  #split boundaries by rows
    lst=[]
    lst.append(llst.pop(0)) # take down the first boundary as a sample
    while len(llst)>0: 
        # only take down the boundaries whose centers are not so close to each other 
        if abs(llst[0]['cy']-lst[-1]['cy'])<=50:
            lst.append(llst.pop(0))
        else: break
    # sort the boundaries by x label
    lst.sort(key=lambda k: (k.get('cx')))
    i=0
    while i<len(lst)-1:
        # only take down the boundaries whose centers are not so close to each other 
        if lst[i+1]['cx']-lst[i]['cx']<=50:
            del lst[i+1]
            i = i - 1
        i = i + 1
    return lst

def getcenter(img):  # get all the boundaries in the picture
    x, y = img.shape[0:2]
    x1 = int(x/2-200)
    y1 = int(y/2-200)
    x2 = int(x/2+200)
    y2 = int(y/2+200)
    img_t=img[x1:x2, y1:y2] # get the proper part of the image
    img_test1 = cv2.resize(img_t,(400,400))
    # image processing

    gray = cv2.cvtColor(img_test1, cv2.COLOR_BGR2GRAY) 
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 10, 50)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)
    (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]
    index = 0
    center = []
    for component in zip(contours, hierarchy):
        contour = component[0]
        peri = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        # compute the center of the contour  
        M = cv2.moments(contour)
        # compute the center location of each boundaries
        if M["m00"]:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX = None
            cY = None
        # select available boundaries
        if 5006 < area < 14000 and cX is not None and 50 < peri < 600 :
            tmp = {'index': index, 'cx': cX, 'cy': cY, 'contour': contour}
            center.append(tmp)
            index += 1

    center.sort(key=lambda k: (k.get('cy')))
    if test(center): # test whether the center variable is usable
        row1=split(center)
    else:
        return center, img_test1 
    if test(center):# test whether the center variable is usable
        row2=split(center)
    else:
        return center, img_test1
    if test(center):# test whether the 'center' variable is usable
        row3=split(center)
    else: 
        return center, img_test1

    center.clear()
    center = row1 + row2 + row3 # rewrite the variable 'center'
    return center,img_test1


def knn(sample ,k, RGB_array, Color_array): # kNN color recognizing function

    # compute the distances and sort them, output indexes to simplify color recognizing
    dist = (((RGB_array-sample)**2).sum(1))**0.5
    sortedDist = dist.argsort()

    # find out the occurrence frequency of the four nearest sample 
    ColorCount = {}
    for i in range(k):
        label = Color_array[sortedDist[i]]
        ColorCount[label] = ColorCount.get(label, 0)+1

    # find out the most frequent color symbol
    maxClr=0
    maxCount = -1
    for key, value in ColorCount.items():
        if value > maxCount:
            maxClr = key
            maxCount = value
    return maxClr



# standard data needed in kNN algorithm
RGB_array = np.loadtxt('train.txt', dtype=int, usecols=(0,1,2), delimiter=',')
Color_array = list(np.loadtxt('train.txt', dtype=int, usecols=3, delimiter=',')) 
number=0
while True:
    time.sleep(0.5) 
    # read frame per half second
    number+=1
    #if os.path.exists('Screenshot_.png'):
    try :
        img = cv2.imread('Screenshot_.png')
        img_save = cv2.resize(img, (800,600)) # resize frame to a proper size
        print(f'valid pic {number}')        #  monitor programme running
        # get the border of nine blocks and other items needed
        center,img_test1 = getcenter(img_save)
        while len(center) == 9:   # only take data when nine boundaryies are all recognized
            print('detecting finished!')
            newimg = cv2.cvtColor(img_test1, cv2.COLOR_BGR2RGB) # convert OpenCV BGR file to RGB file
            # Clritem = {1:'blue', 2:'green', 3:'red', 4:'orange', 5:'white', 6:'yellow'}   this sentence was to display colors directly

            # present recognized color data in the form of python-dictionary
            outputDic = {'colordata':[]}
            for i in center:
                item = knn(newimg[i['cx'], i['cy']], 4, RGB_array, Color_array)
                outputDic['colordata'].append({'number':str(center.index(i)),'color':str(item)})
        
            # write json file
            try:
                out_file = open('clrarray.json', "w") 
                json.dump(outputDic, out_file, indent = 2) 
                out_file.close()
                center.clear()
            except(PermissionError): # if unity is using json file, stop writing
                print('unable to write json file')

    # file reading error processing        
    except(TypeError): 
        print('invalid pic')
    except(cv2.error):
        print('unknown error')