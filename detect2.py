from imageai.Detection import ObjectDetection
import os
import sys
import glob
import telegram
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m%d%Y%H%M%S")

my_chatID = '1499804078'
token = "1506875212:AAE5YkRKA3s2og5TTu3-haTK4z9YlaMelCw"

alerts_path = "E:\\BlueIris\\Alerts\\"
execution_path = "C:\\BlueIris\\ai\\"
output_path = "E:\\BlueIris\\Alerts\checked\\"
cam_num = sys.argv[1]

LatestFile = max(glob.iglob(alerts_path + cam_num +"*.jpg"),key=os.path.getctime)
print(LatestFile)
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=LatestFile, output_image_path=os.path.join(output_path , date_time+"_"+os.path.basename(LatestFile)), minimum_percentage_probability=50)

for eachObject in detections:
    # print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    if(eachObject["name"] == "person"):
       print("We detected a person with a "+str(round(eachObject["percentage_probability"],2))+"% probability")
       bot = telegram.Bot(token=token)
       photo=open(os.path.join(output_path , date_time+"_"+os.path.basename(LatestFile)), 'rb')
       bot.sendPhoto(chat_id=my_chatID, photo=photo)
       break # We dont want multiple messages with the same image
    else:
       print("We did not detect a person")
    print("--------------------------------")