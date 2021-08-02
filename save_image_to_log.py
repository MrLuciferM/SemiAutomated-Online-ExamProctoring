import cv2
from PIL import Image
import csv


PATH = "./Cheating_logs/images/"
SIZE = (128,128)

def save_image_log(image, timestamp, cheatingtype):
    t = timestamp.strftime("%d_%m_%Y_%H__%M_%S")
    filename = f"{t}-{cheatingtype}.jpg"
    location = PATH+filename
    resized = cv2.resize(image, SIZE)
    img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    im_pil.save(location)

    log_time = timestamp.strftime("%d/%m/%Y %H:%M:%S")
    log = [log_time, cheatingtype, location]
    with open("./Cheating_logs/logfiles/logs.csv","a") as logfile:
        writer_obj = csv.writer(logfile)
        writer_obj.writerow(log)

# from datetime import datetime

# # datetime object containing current date and time
# now = datetime.now()
 
# print("now =", now)

# # dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string)	
