###
 # @file        OpenVINODetect.py
 # @brief       This python code is used for vehicle/face detection using OpenVINO
 #              ALL RIGHTS RESERVED.
 ###

#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import cv2
import numpy as np
import time
import math
import logging as log
import json
from collections import namedtuple
from openvino.inference_engine import IENetwork, IEPlugin, IENetLayer
import pandas as pd

class VideoCamera(object):
# Function for initilising model file and input
    def __init__(self):
    
        self.input_vid = "./2.mp4"
        
        #Path of the directory where OpenVINO is installed
        self.OPENVINO_HOME = "/opt/intel/computer_vision_sdk_2018.4.420"
        #Path to cpu extension library
        self.cpu_extension = self.OPENVINO_HOME +"/inference_engine/lib/ubuntu_16.04/intel64/libcpu_extension_sse4.so"
        self.prob_threshold = 0.5
        
        #Path to vehicle detection model file
        #model_xml = OPENVINO_HOME +"/deployment_tools/intel_models/pedestrian-detection-adas-0002/FP32/pedestrian-detection-adas-0002.xml"
        self.model_xml = self.OPENVINO_HOME +"/deployment_tools/intel_models/vehicle-detection-adas-0002/FP32/vehicle-detection-adas-0002.xml"    
        #Path to intermediate .bin file of vehicle detection model
        self.model_bin = os.path.splitext(self.model_xml)[0] + ".bin"
        # Plugin initialization for specified device and load extensions library
        self.plugin = IEPlugin(device="CPU", plugin_dirs=None)
        self.plugin.add_cpu_extension(self.cpu_extension)
        # Read IR of vehicle Detection model
        self.net_vehicle_detection = IENetwork.from_ir(model=self.model_xml, weights=self.model_bin)
        
        
        self.input_vehicle_detection_blob = next(iter(self.net_vehicle_detection.inputs))
        
        self.out_vehicle_blob = next(iter(self.net_vehicle_detection.outputs))
        
        self.exec_net_vehicle_detection = self.plugin.load(network=self.net_vehicle_detection, num_requests=2)
    
        # Read and pre-process input frame
        self.n, self.c, self.h, self.w = self.net_vehicle_detection.inputs[self.input_vehicle_detection_blob].shape
        del self.net_vehicle_detection
       
        self.cap = cv2.VideoCapture(self.input_vid)
        
        self.cur_request_id = 0
        self.next_request_id = 0
        self.cap.set(cv2.CAP_PROP_FPS, 0.05)


    def __del__(self):
        self.cap.release()

    def get_frame(self):
            ret, frame = self.cap.read()
            
            initial_w = self.cap.get(3)
            initial_h = self.cap.get(4)

            in_frame_vehicle_detection = cv2.resize(frame, (self.w, self.h))
            in_frame_vehicle_detection = in_frame_vehicle_detection.transpose((2, 0, 1))  # Change data layout from HWC to CHW
            in_frame_vehicle_detection = in_frame_vehicle_detection.reshape((self.n, self.c, self.h, self.w))

            #Start execution
            self.exec_net_vehicle_detection.start_async(request_id=self.next_request_id, inputs={self.input_vehicle_detection_blob: in_frame_vehicle_detection})
            if self.exec_net_vehicle_detection.requests[self.cur_request_id].wait(-1) == 0:

                # Parse vehicle detection results of the current request
                res_vehicle_detection = self.exec_net_vehicle_detection.requests[self.cur_request_id].outputs[self.out_vehicle_blob]
                xTopLeft = []
                yTopLeft = []
                xBotRight = []
                yBotRight = []
                for vehicle in res_vehicle_detection[0][0]:

                    # Detect vehicle when probability is more than specified threshold of 0.5
                    if vehicle[2] > self.prob_threshold:
                        # Bounding box co-ordinate output of vehicle detection
                        xmin = int(vehicle[3] * initial_w)
                        ymin = int(vehicle[4] * initial_h)
                        xmax = int(vehicle[5] * initial_w)
                        ymax = int(vehicle[6] * initial_h)
                        cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),3)
                        #print(xmin,ymin,xmax,ymax)
                        xTopLeft.append(xmin)
                        xBotRight.append(xmax)
                        yTopLeft.append(ymin)
                        yBotRight.append(ymax)
                        class_id = int(vehicle[1])
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

