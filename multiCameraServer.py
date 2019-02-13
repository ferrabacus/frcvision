#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Copyright (c) 2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
#----------------------------------------------------------------------------

import json
import time
import sys
import cv2
import numpy as np

from cscore import CameraServer, VideoSource
from networktables import NetworkTables

#   JSON format:
#   {
#       "team": <team number>,
#       "ntmode": <"client" or "server", "client" if unspecified>
#       "cameras": [
#           {
#               "name": <camera name>
#               "path": <path, e.g. "/dev/video0">
#               "pixel format": <"MJPEG", "YUYV", etc>   // optional
#               "width": <video mode width>              // optional
#               "height": <video mode height>            // optional
#               "fps": <video mode fps>                  // optional
#               "brightness": <percentage brightness>    // optional
#               "white balance": <"auto", "hold", value> // optional
#               "exposure": <"auto", "hold", value>      // optional
#               "properties": [                          // optional
#                   {
#                       "name": <property name>
#                       "value": <property value>
#                   }
#               ]
#           }
#       ]
#   }

configFile = "/boot/frc.json"

class CameraConfig: pass

team = None
server = False
cameraConfigs = []

"""Report parse error."""
def parseError(str):
    print("config error in '" + configFile + "': " + str, file=sys.stderr)

"""Read single camera configuration."""
def readCameraConfig(config):
    cam = CameraConfig()

    # name
    try:
        cam.name = config["name"]
    except KeyError:
        parseError("could not read camera name")
        return False

    # path
    try:
        cam.path = config["path"]
    except KeyError:
        parseError("camera '{}': could not read path".format(cam.name))
        return False

    cam.config = config

    cameraConfigs.append(cam)
    return True

"""Read configuration file."""
def readConfig():
    global team
    global server

    # parse file
    try:
        with open(configFile, "rt") as f:
            j = json.load(f)
    except OSError as err:
        print("could not open '{}': {}".format(configFile, err), file=sys.stderr)
        return False

    # top level must be an object
    if not isinstance(j, dict):
        parseError("must be JSON object")
        return False

    # team number
    try:
        team = j["team"]
    except KeyError:
        parseError("could not read team number")
        return False

    # ntmode (optional)
    if "ntmode" in j:
        str = j["ntmode"]
        if str.lower() == "client":
            server = False
        elif str.lower() == "server":
            server = True
        else:
            parseError("could not understand ntmode value '{}'".format(str))

    # cameras
    try:
        cameras = j["cameras"]
    except KeyError:
        parseError("could not read cameras")
        return False
    for camera in cameras:
        if not readCameraConfig(camera):
            return False

    return True

"""Start running the camera."""
#def startCamera(config):
#    print("Starting camera '{}' on {}".format(config.name, config.path))
#    camera = CameraServer.getInstance() \
#        .startAutomaticCapture(name=config.name, path=config.path)
#
#    camera.setConfigJson(json.dumps(config.config))
#
#   return camera

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        configFile = sys.argv[1]

    # read configuration
    if not readConfig():
        sys.exit(1)

    # start NetworkTables
    #ntinst = NetworkTablesInstance.getDefault()
    #if server:
        #print("Setting up NetworkTables server")
        #ntinst.startServer()
    #else:
        #print("Setting up NetworkTables client for team {}".format(team))
        #ntinst.startClientTeam(team)
    NetworkTables.initialize(server='roborio-5049-frc.local')
    
    #print("Vision", NetworkTablesInstance.isConnected())
    


    vp = NetworkTables.getTable("Vision")

    # start cameras
    cs = CameraServer.getInstance()

   # cs.enableLogging()
    
    camera = cs.startAutomaticCapture()
    
    camera.setResolution(640, 480)
    
    cvSink = cs.getVideo()

    outputStream = cs.putVideo("Rectangle", 640, 480)

    img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

    isDebug = True

    # loop forever
    while True:

        time, frame = cvSink.grabFrame(img)

        #cv2.rectangle(img, (100, 100), (400, 400), (255, 0, 255), 5)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #frame = cv2.GaussianBlur(hsv, (7, 7), 0)
        #lower_green = np.array([75, 200, 200])
        #upper_green = np.array([85, 255, 255])
        lower_green = np.array([30, 200, 25])
        upper_green = np.array([100, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode (mask, kernel, iterations = 1)
        mask = cv2.dilate(mask, kernel, iterations = 1)
        if  isDebug:
             res = cv2.bitwise_and(frame,frame,mask=mask)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
             for cnt in contours:
                 area = cv2.contourArea(cnt)
                 if area > 250:
                     cnt = contours[0]
                     hull = cv2.convexHull(cnt)
                     rect = cv2.minAreaRect(hull)
                     box = cv2.boxPoints(rect)
                     box = np.int0(box)

                     if isDebug:
                         cv2.drawContours(res, [box], -1, (255, 0, 128), 2)
                     M = cv2.moments(box)
                     if M["m00"] != 0:
                         centerX = int(M["m10"] / M["m00"])
                         centerY = int(M["m01"] / M["m00"])
                     else:
                         centerX, centerY = 0, 0
                     area = cv2.contourArea(box)
                     perimeter = cv2.arcLength(box, True)
                     vp.putNumber('centerX', centerX)
                     vp.putNumber('centerY', centerY)
                     vp.putNumber('area', area)

        status = cv2.imwrite("picture.jpg", img)

        print("Image written to file system..... :[ ", status)
        outputStream.putFrame(res)

        print("I'm in a while loop")

   # import logging
        # cv2.imshow('orig',frame)
        # cv2.imshow('fff',res)

        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #       break

        #time.sleep(10)
    #cv2.destroyAllWindows()
