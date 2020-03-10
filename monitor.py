import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="port camera")
ap.add_argument("-r", "--res", required=False,
    help="video output resolution")
args = vars(ap.parse_args())

if(args["res"] == 480):
    (H, W) = (480, 852)
elif (args["res"] == 720):
    (H, W) = (720, 1280)
elif (args["res"] == 1080):
    (H, W) = (1080, 1920)
else:
    (H, W) = (480, 852)

while(True):
    start = time.time()
    # cam = cv2.VideoCapture(args["input"])
    cam = cv2.VideoCapture(0)
    writer = None
    outputName = "Capture"+str(args["res"])+"p-"+str(int(start))+".mp4"

    if(cam.isOpened() == False):
        print("[ERROR] Camera connection error")
    else:
        while(time.time() <= (start+300)):
            ret, frame = cam.read()
            
            if(not ret):
                print("[ERROR] Camera runtime error")

            frame = cv2.resize(frame, (W, H))

            if writer is None:
                fourcc = 0x00000021
                writer = cv2.VideoWriter(outputName, fourcc, 30,
                    (frame.shape[1], frame.shape[0]), True)
                print("[INFO] Recording: "+outputName)
                
            writer.write(frame)
        
        print("[INFO] Recording done, cleaning up...")
        writer.release()
        cam.release()

