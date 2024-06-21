import cv2
import cvzone
import serial
import time

from cvzone.FaceMeshModule import FaceMeshDetector

ser = serial.Serial('COM4', 9600)
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=50)

while True:
    # choice = int(input("Enter 1 to procedddd"))
    # if choice == 1 :
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=True)
    
        my_array = []
        my_array.append(0)
        if faces:
            for face in faces:
                d = 0
                pointLeft = face[145]
                pointRight = face[374]

            # cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
            # cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)

                w, _ = detector.findDistance(pointLeft, pointRight)
                W = 6.3
                f = 500
                d = (W*f)/w

                cvzone.putTextRect(img, f'Depth {int(d)}cm',
                            (face[10][0]-75, face[10][1]-20), scale=2)
            
                my_array.append(int(d/60 +1))
            
        

        else : 
            my_array.append(5)    
    
        my_array = list(set(my_array))        
        my_string = ','.join(str(i) for i in my_array)
        ser.write(my_string.encode())
        print(my_string.encode())
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        time.sleep(1)

