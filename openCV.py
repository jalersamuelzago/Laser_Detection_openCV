import numpy as np
import cv2

def filtroRGB(src,r,g,b):
	if r == 0:
		src[:,:,2] = 0    #elimina o vermelho
	if g == 0:
		src[:,:,1] = 0    #elimina o verde
	if b == 0:
		src[:,:,0] = 0    #elimina o azul    

cap = cv2.VideoCapture('laser5.3gp')

cont=0
while(cap.isOpened()):
    ret, frame = cap.read()
    #===================ajustar tamanho da imagem===================
    
    scale_percent = 60 # percent of original size
    # resize image
    frame = cv2.resize(frame, (int(frame.shape[1] * scale_percent / 100), int(frame.shape[0] * scale_percent / 100)), interpolation = cv2.INTER_AREA)
    #===================================================================

    #ret,thresh1 = cv2.threshold(frame,252,255,cv2.THRESH_BINARY)

    b,g,r = cv2.split(frame)

    minRed = np.array(254)
    maxRed = np.array(255)

    maskRed = cv2.inRange(r, minRed, maxRed)
    resize = cv2.bitwise_and(r, r, mask = maskRed)


    #filtroRGB -> retira verde e azul da imagem
    #filtroRGB(thresh1,1,0,0)
    #kernel = np.ones((5,5),np.uint8)
    #erosion = cv2.erode(thresh1,kernel,iterations = 7)
    #gray -> escala de cinza
    #gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
    
    # calculate moments of binary image
    Momento = cv2.moments(resize)
    #calculate x,y coordinate of center
    if (Momento["m00"])!=0:
        cX = int(Momento["m10"] / Momento["m00"])
        cY = int(Momento["m01"] / Momento["m00"])
        cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, str(cX)+"/"+str(cY),(100, 100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255, 255, 255),2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    cv2.imshow('frame',frame)
    
    #print (cX, cY)
cap.release()
cv2.destroyAllWindows()