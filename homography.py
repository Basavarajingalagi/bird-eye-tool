import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create a function based on a CV2 Event (Left button click)
def clickponts(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #cv2.circle(img,(x,y),100,(0,255,0),-1)
        print(x,y)
        clicks.append([x,y])

#imagepaths
images = [r'F:\googlemap\MSIL\map.jpg',r'F:\googlemap\MSIL\3.jpg']

#src = []
#dst = []

for i in images:
    clicks = []

    # Create a black image
    img =cv2.imread(i, cv2.IMREAD_UNCHANGED)

    # This names the window so we can reference it 
    cv2.namedWindow(winname='my_drawing')
    # Connects the mouse button to our callback function
    cv2.setMouseCallback('my_drawing',clickponts)

    while True: 
        cv2.imshow('my_drawing',img)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    if images.index(i)==0:
        dst=clicks
        print("src",clicks)
    if images.index(i):
        src=clicks
        print("dst",clicks)


print(src)
print(dst)

x= [i[0] for i in dst ]
y = [i[1] for i in dst ]
    
xmax =max(x)
xmin = min(x)
ymin =min(y)
ymax = max(y)

print(xmax)
src1 = np.float32(src)
dst1= np.float32(dst)
#dst = np.float32([[134, 69], [237, 70], [237, 259], [134, 260]])
M = cv2.getPerspectiveTransform(src1, dst1) # The transformation matrix
#Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

img = cv2.imread(r'F:\googlemap\MSIL\3.jpg') # Read the test img
img1 = cv2.imread(r'F:\googlemap\MSIL\map.jpg')
#img = img[450:(450+IMAGE_H), 0:IMAGE_W] # Apply np slicing for ROI crop
warped_img1 = cv2.warpPerspective(img, M, (960, 540)) # Image warping

cv2.imwrite("a.jpg",warped_img1)

crop_img = warped_img1[ymin:ymax, xmin:xmax]

blank_img = np.zeros([540,960,3],dtype=np.uint8)
blank_img[ymin:ymax, xmin:xmax] = crop_img


img2gray = cv2.cvtColor(blank_img,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

img1_bg = cv2.bitwise_and(img1,img1,mask = mask_inv)

img2_fg = cv2.bitwise_and(blank_img,blank_img,mask = mask)


dst = cv2.add(img1_bg,img2_fg)
img1[0:540, 0:960] = dst

cv2.imwrite('crop_destj.jpg',img1)

