# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(1)

_, frame = vid.read()

height,width,_ = frame.shape
k = 3

Upper = (164,255,255)
Lower = (24,128,115)

try:
    while(True):
        
        # Capture the video frame by frame
        ret, frame = vid.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Scaling frame
        Scaled_frame = cv2.resize(frame,(width*k,height*k))

        # Display the resulting frame
        cv2.imshow('frame', Scaled_frame)
        cv2.imshow('hsv', hsv)
            
        # the 'q' button is set a0s the quitting button
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()