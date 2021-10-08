import cv2
import time
import datetime
import requests
import json
import os
import threading



result = None

def get_result():
    global result
    
    url = "http://localhost:8888/image"

    while True:
    
        data = open(r"{loaction to your pic}", 'rb').read()
        response = requests.post(url,
                            data=data)
                            #headers=headers)

    #print(response.text.encode('utf8'))
        res_body = response.text

        json_body = json.loads(res_body)
        #print(json_body)

        #print(e2float(json_body["predictions"][0]["probability"]))
        #print(e2float(json_body["predictions"][1]["probability"]))

        if round(json_body["predictions"][0]["probability"],1) > 0.5:
            result = json_body["predictions"][0]["tagName"]

        else:
            result = json_body["predictions"][1]["tagName"]

        print(result)


def open_camera(window_name, video_id):

    start_time = time.time()
    counter = 0
    x = 1
    timeF = 10
    global result
    status = None
    

    cascPath = r"D:/Playground/AI_Sapmles/Mask_Detection/Mask_Detection/model/haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    
    cv2.namedWindow(window_name)

    capture = cv2.VideoCapture(video_id)
    fps = capture.get(cv2.CAP_PROP_FPS)
    #capture.set(cv2.CAP_PROP_POS_FRAMES, 20)

    while capture.isOpened():
        ok, frame=capture.read()
        if not ok:
            print("Check Your Camera Connection !!")
            break
        #frame = cv2.flip(frame,0)

        
        # 转换为灰度图片
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 调用分类器进行检测
        faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(50, 50),
        )

        # 标识人脸框
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (0, 255, 0), 2)
            cv2.rectangle(frame, (x-20, y-40), (x+w+20, y-20), (255, 0, 0), -1)
            cv2.putText(frame,"Status: {0}".format(status), (x-19, y-20), 1 , 1.2, (255, 255, 255), 1)
            pic = frame[(y-20):(y+h+20),(x-20):(x+w+20)]
        
        # 间隔截图
        counter += 1
        #print(counter)

        if(counter%timeF == 0):
            cv2.imwrite(r"{where to put your pic}", pic)
            #print("pic saved")
  
            # 请求结果
            #get_result()
            status = result
            #print(result)

        # 显示帧率和时间
        
        cv2.putText(frame,"FPS: {0}".format(int(counter / (time.time() - start_time))), (10, 20), 1 , 1.2, (255, 0, 255), 1)
        #cv2.putText(frame,"FPS: {0}".format(fps), (10, 20), 1 , 1.2, (255, 0, 255), 1)
        #cv2.putText(frame,"Time: {0}".format(datetime.datetime.now()), (10, 40), 1 , 1.2, (255, 0, 255), 1)
        
        # 打开视频窗口
        cv2.imshow(window_name, frame)
        
        
        
        try:
            c = cv2.waitKey(50)
        except KeyboardInterrupt:
            print("Exitting Program !!")
            break


    capture.release()
    cv2.destroyWindow(window_name)
    print("Camera Closed !!")


start_capture_thread = threading.Thread(target = open_camera, args=("Capture1",0,))
start_capture_thread.daemon = True
start_capture_thread.start()

result_thred = threading.Thread(target = get_result, args=())
result_thred.daemon = True
result_thred.start()


while True:
    selection = input("Press Q to quit\n")
    if selection == "Q" or selection == "q":
        print("Quitting...")
        break


