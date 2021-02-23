from imageai.Detection import ObjectDetection
import os
import sys
import glob
# import telegram (use either telegram or Pushover )
from datetime import datetime
import configparser
from pushover import Client

config_file = "alerts.ini"

config = configparser.ConfigParser()
config.read(config_file)
now = datetime.now()
date_time = now.strftime("%m%d%Y%H%M%S")

# Telegram
#my_chatID = '1499804078'
#token = "1506875212:AAE5YkRKA3s2og5TTu3-haTK4z9YlaMelCw"
# pushover
my_push_token = 'ay9kn4biebdaz8mzgw3ic3dmgn2qd9'
my_pushID = 'uzmbs8vh2vjib49284uids6wejbn6m'

alerts_path = "E:\\BlueIris\\Alerts\\"
execution_path = "C:\\BlueIris\\ai\\"
output_path = "E:\\BlueIris\\Alerts\checked\\"
cam_num = sys.argv[1]

if not os.path.isdir(output_path):
    os.makedirs(output_path)

if config['camera_alerts']['inside'] == "OFF" and "Cam" in cam_num:
    sys.exit("Exiting, we aren't monitoring inside cameras")
if config['camera_alerts']['outside'] == "OFF" and "Out" in cam_num:
    sys.exit("Exiting, we aren't monitoring outside cameras")

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
       # Pushover
       client = Client(my_pushID, api_token=my_push_token)
       # Telegram
       #bot = telegram.Bot(token=token)
       with open(os.path.join(output_path , date_time+"_"+os.path.basename(LatestFile)), 'rb') as image:
           client.send_message("We detected a person with a "+str(round(eachObject["percentage_probability"],2))+"% probability", attachment=image)
           #bot.send_message(chat_id=my_chatID, text="We detected a person with a "+str(round(eachObject["percentage_probability"],2))+"% probability")
           #bot.sendPhoto(chat_id=my_chatID, photo=image)
           image.close()
       break # We dont want multiple messages with the same image
    else:
       print("We did not detect a person")
    print("--------------------------------")

## Clean Up
#photo.close()
#if os.path.exists(os.path.join(output_path , date_time+"_"+os.path.basename(LatestFile))):
#    os.remove(os.path.join(output_path , date_time+"_"+os.path.basename(LatestFile)))
