#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import StringIO
from utils import read_cfg

class Pin(object):
    def __init__(self,name):
        self.name=name
        self.textpos=(0,0)
        self.p0=(0,0)
        self.p1=(0,0)
        self.anchor='start'
        
    def generate_text(self):
        return '<text transform="matrix(1 0 0 1 {} {})" text-anchor="{}" fill="#231F20" font-family="\'DroidSans\'" font-size="3.5">{}</text>\n'.format(self.textpos[0],self.textpos[1],self.anchor,self.name)
        
    def generate_line(self):
        return '<line fill="none" stroke="#231F20" stroke-miterlimit="10" x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(self.p0[0],self.p0[1],self.p1[0],self.p1[1])

def get_rect_size(pinscfg):
    n=(len(pinscfg)+1)/2
    return (50,(n+1)*8)
        
def get_total_size(pinscfg):
    w,h=get_rect_size(pinscfg)
    return (w+14,h+14)

def generate_rect(pinscfg):
    w,h=get_rect_size(pinscfg)
    return '<rect x="7" y="7" fill="none" stroke="#231F20" stroke-width="0.7" stroke-miterlimit="10" width="{}" height="{}"/>\n'.format(w,h)

def generate_pins(pinscfg):
    pins=[Pin(p[0]) for p in pinscfg]
    n=(len(pins)+1)/2
    #rw=50
    #rh=(n+1)*8
    index=0
    y=15
    for p in pins:
        if index<n:
            p.p0=(0.1,y)
            p.p1=(7,y)
            p.textpos=(9,y+2)
        else:
            p.p0=(57,y)
            p.p1=(63.9,y)
            p.textpos=(55,y+2)
            p.anchor='end'
        index+=1
        if index<n:
            y+=8
        elif index>n:
            y-=8
    return pins            
        
def generate_header(w,h):
    s=StringIO.StringIO()
    s.write('<?xml version="1.0" encoding="utf-8"?>\n')
    s.write('<!-- Generator: parter 1.0.0  SVG Version: 6.00 Build 0)  -->\n')
    s.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
    s.write('<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"\n')
    s.write('    width="{}px" height="{}px" viewBox="0 0 {} {}" enable-background="new 0 0 {} {}" xml:space="preserve">\n'.format(w,h,w,h,w,h))
    return s.getvalue()

def generate_footer():
    return '</svg>\n'
    
def generate(cfgname):
    try:
        cfg=read_cfg(cfgname)
        name=cfg['name']
        title=cfg['title']
        pinscfg=cfg['pins']
        pins=generate_pins(pinscfg)
        w,h=get_total_size(pinscfg)
        with open(name+"_schema.svg",'w') as f:
            f.write(generate_header(w,h))
            for p in pins:
                f.write(p.generate_text())
            f.write(generate_rect(pinscfg))
            for p in pins:
                f.write(p.generate_line())
            f.write('<text transform="matrix(0 1 -1 0 32 {})" text-anchor="middle" font-family="\'DroidSans\'" font-size="4.25">{}</text>\n'.format(h/2,title))
            f.write(generate_footer())
    except IOError,e:
        print e
    except KeyError,e:
        print "Missing configuration variable: {}".format(e)

def main():
    if len(sys.argv)<2:
        print "Usage: genschema <config>"
    else:
        generate(sys.argv[1])


if __name__=='__main__':
    main()
