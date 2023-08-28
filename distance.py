

import cv2
import winsound



KNOWN_DISTANCE = 76.2  

KNOWN_WIDTH = 14.3  

GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)


face_detector = cv2.CascadeClassifier("G:\downloads\Alerting system\Alerting system\haarcascade_frontalface_default.xml")




def focal_length(measured_distance, real_width, width_in_rf_image):
   
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value



def distance_finder(focal_length, real_face_width, face_width_in_frame):
    
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance



def face_data(image):
   

    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w

    return face_width



ref_image = cv2.imread("G:\downloads\Alerting system\Alerting system\Ref_image.jpg")

ref_image_face_width = face_data(ref_image)
focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, ref_image_face_width)
print("focal length  ",focal_length_found)


while True:
    _, frame = cap.read()

    
    face_width_in_frame = face_data(frame)
    
    if face_width_in_frame != 0:
        Distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)
        if Distance <90:
          cv2.putText(
           frame, f"PLEASE BE AWAY", (200, 300), fonts, 1, (RED), 2   
           )
          frequency = 2500  
          duration = 800 
          winsound.Beep(frequency, duration)
    
        
        cv2.putText(
            frame, f"Distance = {round(Distance,2)} CM", (50, 50), fonts, 1, (WHITE), 2
        )
    

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
