#===============================MOTIVATION================================
#   This code was created for the semester project of Agent-Based Systems
#   course (SAG_2020L) of master studies programme at the Warsaw University
#   of Technology - Faculty of Electronics and Information Technology. 
#
#   Supervision and mentoring: PhD D.Ryżko
#
#===============================SUMMARY===================================
#
#   The agent system performs task of a distributed image classification.
#   System consists of agents that are communicating asynchronously. The decision
#   of the classifier is obtained by voting. A randomly selected commanding agent 
#   from ordinary agents is responsible for outsourcing tasks and collecting
#   classification results. System ensures operation even if contact with some
#   agents is lost.
#
#===============================LICENSE===================================
#
#   This code is a free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as 
#   published by the Free Software Foundation, either version 3 of the 
#   License, or any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details. It can be found
#   at <http://www.gnu.org/licenses/>.
#
#==========================================================================
#   2020 Warsaw University of Technology - M.Karcz, D.Orlinski, T.Szczepanski
#==========================================================================    
#
#   interface.py - allows user to get access to the data of agent system:
#   results, logs and queue. Allows also to enter images for classification  
#
#==========================================================================


import os
import shutil 

class Interface:

    # constructor creates paths to directories used by multi-agent classifier
    def __init__(self):
        self.home_proj_dir = os.path.dirname(__file__)
        self.logs_dir = "data_to_recognize/logs.txt" # path to logs made by agents
        self.images_to_recognize = "data_to_recognize/recognize/" # in this directory are stored images to be recognized by classifier - they are copies of images provided by user
        self.images_recognized = "data_to_recognize/recognized/" # classifier stores in this directory images that have already been recognized
        self.classification_dir = "data_to_recognize/classification_results.txt"
        
        self.createFileHandles()  
 
    # method creates handle to logs files - user can read from here
    def createFileHandles(self):
        
        absolute_logs_dir = os.path.join(self.home_proj_dir, self.logs_dir) 
        absolute_classification_dir = os.path.join(self.home_proj_dir, self.classification_dir)        

        try:
            self.logs_file_handle = open(absolute_logs_dir,"r") # read only
            self.classif_file_handle = open(absolute_classification_dir,"r") # read only
        except IOError:
            self.logs_file_handle = None
            self.classif_file_handle = None
            print("File not found or path is incorrect")
    
    # method gets path to the image provided by user as an argument and copies this image to the folder that is being watched by agents 
    def getImageFromUser(self,_user_img_path):   
        
        self.user_img_path = _user_img_path
        absolute_dest_dir = os.path.join(self.home_proj_dir, self.images_to_recognize)
        absolute_dest_dir = os.path.join(absolute_dest_dir, os.path.basename(self.user_img_path))

        try:
            shutil.copy(self.user_img_path, absolute_dest_dir)
            print ("File copy success - file has been put in a queue") 
        except IOError:
            print("File not found or path is incorrect")

    # method lists filenames in the given directory
    def listFiles(self, path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    def readLogs(self):
        if (self.logs_file_handle != None):
            print(self.logs_file_handle.name)
            print (self.logs_file_handle.read())

    def readClassification(self):
        if (self.classif_file_handle != None):
            print(self.classif_file_handle.name)
            print (self.classif_file_handle.read())    


def main(): 

    interf = Interface()  
    print ("***\nYou have just run the interface that allows you to both read from the multiagent classifier and provide images to be classifed\n***\n")
    choice = input(">What would you like to do? (q is quit, h is help)\n")

    while choice != 'q':
        if choice == 'p':
            path = input(">Provide absolute path to the image you want to classify:\n")
            if (path != None):                
                interf.getImageFromUser(path)
        elif choice == 'r':
            print("-Get results:")
            interf.readClassification()
        elif choice == 'l':
            print("-Read logs:")
            interf.readLogs()
        elif choice == 'f':
            print("-Check list of files to be recognized:")
            for file in interf.listFiles(interf.images_to_recognize + "."):
                print (file)  
        elif choice == 'h':
            print("*HELP*:\n\tp - path to the image to be recognized \n\tr - get result of classification\n\tl - read logs from system\n\tf - list files to be recognized\n")
        else:
            print(">That is not a valid input!")
        choice = input(">What would you like to do? (q is quit, h is help)\n")

if __name__ == "__main__":    
    main()