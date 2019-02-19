#!/usr/bin/env python
import math
import cv2
from darkflow.net.build import TFNet
import numpy as np
import rospy
import time
from tf_classifier import predict

options = {
    'model': '/home/pavel/darkflow/cfg/yolo.cfg',
    'load': '/home/pavel/darkflow/bin/yolo.weights',
    'labels': '/home/pavel/darkflow/cfg/coco.names',
    'threshold': 0.2,
    'gpu': 0.6
}


class Sight(object):
    bottle_types_db = ["Coca Cola", "Coca Cola Light", "Water"]
    bottle_types = ["coke", "coke diet", "water"]
    
    def __init__(self):
        self.objects = []
        self.tfnet = TFNet(options)
        self.mname = "[SIGHT] "

    def recognize_objects(self):
        print(self.mname + "Recognizing objects.")
        colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        for _ in range(10):
            stime = time.time()
            ret, frame = capture.read()
            if ret:
                results = self.tfnet.return_predict(frame)
                self.objects = []#[(result['label'], result['confidence'])for result in results]

                for color, result in zip(colors, results):
                    tl = (result['topleft']['x'],       result['topleft']['y'])
                    br = (result['bottomright']['x'],   result['bottomright']['y'])
                    label = result['label']
                    confidence = result['confidence']
                    
                    if(label == 'bottle'):
                        img_as_string = cv2.imencode('.jpg', frame)[1].tostring()
                        prediction = predict(img_as_string)
                        label = prediction[0][0]
                        confidence = prediction[0][1]

                    self.objects.append((label, confidence))
                    text = '{}: {:.0f}%'.format(label, confidence * 100)
                    frame = cv2.rectangle(frame, tl, br, color, 5)
                    frame = cv2.putText(
                        frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

                cv2.imshow('frame', frame)
                # print('FPS {:.1f}'.format(1 / (time.time() - stime)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows()

    def count(self, label):
        return sum([1 if obj[0] == label else 0 for obj in self.objects])
    
    def count_people(self):
        people = self.count('person')
        print(self.mname + "People detected: " + str(people))
        return people
    
    def count_stock(self):
        stock = [(btdb, self.count(bt)) for (bt, btdb) in zip(self.bottle_types, self.bottle_types_db)]
        print(self.mname + "Stock detected: " + str(stock))
        return stock
    
    def count_bottles(self):
        bottles = sum([c[1] for c in self.count_stock()])
        print(self.mname + "Bottles detected: " + str(bottles))
        
        return bottles
