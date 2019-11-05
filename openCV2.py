import numpy as np
import cv2

def filtroRGB(src,r,g,b):
	if r == 0:
		src[:,:,2] = 0    #elimina o vermelho
	if g == 0:
		src[:,:,1] = 0    #elimina o verde
	if b == 0:
		src[:,:,0] = 0    #elimina o azul    

cap = cv2.VideoCapture('laser2.mp4')
cX=[]
cY=[]
cont=0
while(cap.isOpened()):
    ret, frame = cap.read()
    ret,thresh1 = cv2.threshold(frame,252,255,cv2.THRESH_BINARY)
    #filtroRGB -> retira verde e azul da imagem
    filtroRGB(thresh1,1,0,0)
    kernel = np.ones((5,5),np.uint8)
    #erosion = cv2.erode(thresh1,kernel,iterations = 7)
    #gray -> escala de cinza
    gray = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    
    # calculate moments of binary image
    Momento = cv2.moments(gray)
    #calculate x,y coordinate of center
    if (Momento["m00"])!=0:
        cX.append(int(Momento["m10"] / Momento["m00"]))
        cY.append(int(Momento["m01"] / Momento["m00"]))
        if cont>0:
            print(cX)
            print(cont)
            diferencaX = cX[cont]-cX[cont-1]
            diferencaY = cY[cont]-cY[cont-1]
            if diferencaX<0:
                diferencaX=diferencaX*-1
            if diferencaY<0:
                diferencaY=diferencaY*-1
            if diferencaX>50 or diferencaY>50:
                cv2.putText(frame, "Laser nao detectado.",(100, 100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255, 255, 255),2)
        # put text and highlight the center
            else:
                cv2.putText(frame, "centroid", (cX[cont] - 25, cY[cont] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(frame, str(cX[cont])+"/"+str(cY[cont]),(100, 100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255, 255, 255),2)
        cont+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('frame',frame)
    
    #print (cX, cY)
cap.release()
cv2.destroyAllWindows()