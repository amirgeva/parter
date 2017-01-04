#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cv2

class ImageParser(object):
    def __init__(self,img):
        self.image=img
        self.lab=cv2.cvtColor(self.image,cv2.COLOR_BGR2LAB)
        cv2.setMouseCallback('vis',self.on_mouse)
        cv2.imshow("vis",img)
        self.corners=[]
        
    def redraw(self):
        vis=self.image.copy()
        n=len(self.corners)
        for i in xrange(0,n):
            cur=self.corners[i]
            cv2.circle(vis,cur,8,(0,0,255),3)
            if n>0:
                nxt=self.corners[(i+1)%n]
                cv2.line(vis,cur,nxt,(255,255,0),3)
        cv2.imshow("vis",vis)

    def process(self):
        while cv2.waitKey(10)!=27:
            pass

    def on_mouse(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print "mouse: {},{}".format(x,y)
            self.corners.append((x,y))
            self.redraw()

def main():
    name='pam8403.jpg'
    if len(sys.argv)>1:
        name=sys.argv[1]
    cv2.namedWindow('vis',cv2.WINDOW_NORMAL)
    img=cv2.imread(name)
    p=ImageParser(img)
    p.process()

if __name__=='__main__':
    main()
