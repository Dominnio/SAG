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