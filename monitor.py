import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="port camera")
ap.add_argument("-r", "--res", required=False,
    help="video output resolution")
args = vars(ap.parse_args())

if(int(args["res"]) == 480):
    (H, W) = (480, 852)
elif (int(args["res"]) == 720):
    (H, W) = (720, 1280)
elif (int(args["res"]) == 1080):
    (H, W) = (1080, 1920)
else:
    (H, W) = (480, 852)

cam = cv2.VideoCapture(int(args["input"]))

s = time.time()
for i in range(100):
    ret, frame = cam.read()
e = time.time()
fps = 100/(e-s)
print("[INFO] Estimated Camera FPS: {:.4f}".format(fps))

cam.release()

counter = 0

while(True):
    
    start = time.time()

    cam = cv2.VideoCapture(int(args["input"]))
    # cam = cv2.VideoCapture(0)
    writer = None
    outputName = "Capture"+str(args["res"])+"p-"+str(time.localtime(start).tm_year)+'_'+str(time.localtime(start).tm_mon)+'_'+str(time.localtime(start).tm_mday)+'_'+str(time.localtime(start).tm_hour)+'_'+str(time.localtime(start).tm_min)+".mp4"

    if(cam.isOpened() == False):
        print("[ERROR] Camera connection error")
    else:
        while(time.time() <= (start+950)):
            ret, frame = cam.read()
            
            if(not ret):
                print("[ERROR] Camera runtime error")

            frame = cv2.resize(frame, (W, H))

            if writer is None:
                fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                writer = cv2.VideoWriter(outputName, fourcc, int(fps), (frame.shape[1], frame.shape[0]), True)
                print("[INFO] Recording: "+outputName)
                
            writer.write(frame)
        
        print("[INFO] Recording done, cleaning up...")
        writer.release()
        cam.release()
    
    counter+=1

    if(counter > 5):
        time.sleep(3600)
        counter = 0
    else:
        time.sleep(600)
