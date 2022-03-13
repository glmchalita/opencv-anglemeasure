import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('circulos.png')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Mask Circuferência Esquerda
left_lower = np.array([50, 50, 50])  
left_upper = np.array([80, 230, 210])
left_mask = cv2.inRange(img_rgb, left_lower, left_upper)

# Mask Circuferência Direita
right_lower = np.array([172, 11, 11])  
right_upper = np.array([179, 180, 210])
right_mask = cv2.inRange(img_rgb, right_lower, right_upper)

# Bitwise_or - Juntando Masks
mask = cv2.bitwise_or(left_mask, right_mask)
target = cv2.bitwise_and(img_rgb,img_rgb, mask=mask)

# Contorno
contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) 
contorno = mask_rgb.copy()
cv2.drawContours(contorno, contornos, -1, [0, 0, 255], 10);

# Centro de Massa
for i in range(len(contornos)):
    cnt = contornos[i]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    size = 20
    color = (128,128,0)
    
    cv2.line(contorno,(cx - size,cy),(cx + size,cy),color,5)
    cv2.line(contorno,(cx,cy - size),(cx, cy + size),color,5)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = cy , cx
    
    if i == 0:
        origem = (730, 350)
    else:
        origem = (230, 50)

    cv2.putText(contorno, str(text), origem, font,1,(200,50,0),2,cv2.LINE_AA)

# Calculando Area dos Circulos
img_r = cv2.imread('circulos.png', 0)
img_r = cv2.medianBlur(img_r,5)
cimg = cv2.cvtColor(img_r,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(img_r,cv2.HOUGH_GRADIENT,1,40,param1=60,param2=50,minRadius=110,maxRadius=200)
circles = np.uint16(np.around(circles))
count = 0
for i in circles[0,:]:
    area = 3.14159 * i[2] * i[2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    origem = ((730,400), (230,100))
    cv2.putText(contorno, str(area), origem[count], font,1,(200,50,0),2,cv2.LINE_AA)
    count = count + 1

# Print
plt.figure(figsize=(10,10))
plt.imshow(contorno, cmap="Greys_r", vmin=0, vmax=255)
plt.show()
