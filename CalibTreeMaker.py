'''
Created on Oct 9, 2013

@author: mbenoit
'''
import time,os,fileinput,sys
from math  import sqrt
from numpy import matrix
from array import array
from ROOT import *
import pyximport; pyximport.install(pyimport=True)

from itertools import product

class CalibTreeMaker:
    '''
    classdocs
    '''
    last_time = time.time()
    AllClusters = []

    def __init__(self,filename,outfile):
        '''
        Constructor
        '''
        self.ReadFile(filename,outfile)
        
    def ReadFile(self,filename,outfile):
        
        
        #data_file = open(filename,"r")
        #lines = data_file.readlines()
        
        X = []
        Y = []
        TOT = []
        nFrames = 0
       
        size1cnt = 0
        self.last_time=time.time()
        
        outfile = TFile(outfile,'recreate')
        pixelTree = TTree("pixels","pixelstree")
        
        xt=array( 'i', [ 0 ] )
        yt=array( 'i', [ 0 ] )
        tott=array( 'i', [ 0 ])
        
        pixelTree.Branch( 'col', xt, 'col/I' )
        pixelTree.Branch( 'row', yt, 'row/I' )      
        pixelTree.Branch( 'tot', tott, 'tot/I' )       
        
        
        self.last_time = time.time()
        finput=fileinput.input([filename])
        for line in finput :
        #for line in lines : 
            
            if "#" in line : 
                nFrames+=1
                
                for i in range(len(X)) :
                    xt[0]=X[i]
                    yt[0]=Y[i]
                    tott[0]=TOT[i]
                    pixelTree.Fill()      
                
                if(nFrames%100==0):
                    print "Processed Frame %i (%.5fs/frame)"%(nFrames,(time.time()-self.last_time )/100.)
                    self.last_time = time.time()
                X = []
                Y = []
                TOT = []
                
            
            else : 
                data = line.split()
                X.append(int(data[0]))
                Y.append(int(data[1]))
                TOT.append(int(data[2]))
                del data
               
        
        pixelTree.Write() 
        outfile.Close()
        finput.close()
        
        print "found %i single pixel clusters"%size1cnt
 
    
   
   
dataFile = "/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/Validation_Calibration_A06-W0110/Am241_A06-W0110_24-06-2014_25V"
rootFile = "/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/Validation_Calibration_A06-W0110/Am241_A06-W0110_24-06-2014_25V_CalibTree.root"
aCalibDataSet = CalibTreeMaker(dataFile,rootFile)


  
