import os
import shutil 
import argparse

#config file names 


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
    choice = input("What would you like to do? (q is quit, h is help)\n")

    while choice != 'q':
        if choice == 'p':
            print("You chose path")
        elif choice == 'r':
            print("You chose result")
        elif choice == 'l':
            print("You chose logslist")
        elif choice == 'f':
            print("You chose files")
        elif choice == 'h':
            print("p - path to the image to be recognized \nr - get result of classification\nl - read logs from system\nf - list files to be recognized")
        else:
            print("That is not a valid input.")
        choice = input("What would you like to do? (q is quit, h is help)\n")

      
    # parser = argparse.ArgumentParser("Interface for multiagent classifer - user can provide images to be classifed and read logs from system")
    # parser.add_argument('-m','--mode', type=str, help='"result" - user can get classification result,\n "data" - user can provide image to be classified')
    
    # my test file path: /home/tomek1911/Pictures/test.jpg
    # python interface.py -p "/home/tomek1911/Pictures/test.jpg"

    # parser.add_argument('-p','--path', type=str, help='provide image to be classified by system')
    # args = parser.parse_args()
    
    # example of using interface - get image from user - check folder of images in to be recognized and read from logs and classification results
   
    # interf = Interface()  
    # if (args.path != None):
    #     interf.getImageFromUser(args.path)

    # for file in interf.listFiles(interf.images_to_recognize + "."):
    #     print (file)    
    
    # interf.readLogs()
    # interf.readClassification()

if __name__ == "__main__":    
    main()