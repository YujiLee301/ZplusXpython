#import stage
import numpy as np
import ROOT
from ROOT import TCanvas, TH1F, TF1, TLegend, gPad, THStack, TColor
#import tdrstyle
import os.path
import os
from array import array
import yaml
import sys
import math

from estimateZX import *


fileList = ["/eos/user/y/yujil/HZZRun3Share/Data2022CD_noDuplicate.root",
            "/eos/user/y/yujil/HZZRun3Share/ZXCR/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8.root"
            ]

RootNickNames = ["Data","ZZ"]

# For testing
#fileList = ["../DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_2018filter2l_new_ZX.root",]
#RootNickNames = ["DY50"]

print("Second stage of processing (Creation of ZX SR contributions for Data and ZZ.\n")

for i in range(len(fileList)):
    inFile =  ROOT.TFile.Open(fileList[i], "READ")
    if i == 0:
        tree = inFile.Get("Events")
    else:
        tree = inFile.Get("Events")


    print ("- File: \"" + fileList[i] + "\" has been opened.\n-- It has "+str(tree.GetEntries())+" events.\n")
    estimateZX("Hist_Data_ptl3_WZremoved.root",tree, RootNickNames[i])
    inFile.Close()