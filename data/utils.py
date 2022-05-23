# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:26:35 2022

@author: Ale
"""
import os
from natsort import natsorted

def getBaseNames(pathFolder):
    files = [os.path.splitext(os.path.basename(file))[0] for file in natsorted(os.listdir(pathFolder))] 
    return files


def getBaseName(pathFile):
    basename = os.path.splitext(os.path.basename(pathFile))[0]
    return basename