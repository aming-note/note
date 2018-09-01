import cv2
cap = cv2.VideoCapture('C:\\Users\\Admin\\Videos\\test.mp4')
while(cap.isOpened()):
    ret,frame = cap.read()
    print(cap.read())
    if ret==True:
        cv2.imshow('a',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print('视频不存在')
        break
cap.release()
cv2.destroyAllWindows()