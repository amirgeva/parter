#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def read_cfg(filename):
    with open(filename,'r') as f:
        return json.load(f)
    return {}

def main():
    pass


if __name__=='__main__':
    main()
