#Given a directory or a set of directories or a full hard drive the program should automatically sort files based on their names, types, sizes and
#other meta data related to the files and also first the program should crawl the given directory or a set of directories or a hard drive and then find 
#the file types and other meta data revelant data and then based on user preference is should sort the files and put according to how the user wants
#them to be.
# 

#Also integrate A.I that will automatically sort the files based on their content inside them and actually read and write files of users like allowing
#the user to edit their files.




import os
import threading


import time
from shutil import *
import dicttoxml
from datetime import datetime
from xml.etree import ElementTree as ET
from nudenet import NudeClassifier
import cv2















#THERE MUST BE A DIRECTORY ENTERED FIRST
#THE PROGRAM SHOULD CRAWL OVER ALL THE DIRECTORIES AND FILES IF ANY IN THE LISTED DIRECTORY ABOVE
#THEN IT SHOULD SHOW THE USER ALL THE FILES IT HAS FOUND AND HOW IT WILL SORT THE FILES OUT
#THE USER IS ALLOWED TO MAKE EDITS AND CHANGES
#THEN THE PROGRAM SORTS THE FILES 
#







class sorter():
    
    def __init__(self, specific_formats=None, specific_folder=None):
        
        self.mode = 'move'
        self.lst_of = {}
        self.doc_ext = ['.doc', '.docx', '.odt', '.pdf', '.xls', '.xlsx', '.ods', '.ppt', '.pptx', '.txt', '.pps', '.odp', '.key', '.xlr', '.ods', '.rtf', '.tex', '.wks', '.wps', '.wpd']
        self.img_ext = ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.png', '.gif', '.webp', '.tiff','.tif', '.psd', '.raw', '.arw', '.cr2', '.nrw', '.k25', '.bmp', '.dib', '.heif', '.heic', '.ind', '.indd', '.indt', '.jp2','.j2k','jpf','jpx','.jpm', '.mj2', '.svg', '.svgz', '.ai', '.eps']
        self.vid_ext = ['.webm','.mpg','.mpeg','.mpe','.mpv', '.mp4','.m4p','.m4v', '.avi', '.wmv', '.mov', '.qt', '.flv', '.swf', 'avchd', '.3gp', '.3g2','.h264', '.m4v', '.mkv', '.mov', '.rm', '.swf', '.vob']
        self.sound_ext = ['.pcm', '.wav', '.aiff', '.mp3', '.aac', '.flac', '.wma', '.3ga', '.aif', '.cda', '.mid', '.midi', '.mpa', '.ogg', '.wpl']
        self.zip_ext = ['.7z', '.zip', '.z', '.tar.gz', '.arj', '.deb', '.pkg', '.rar', '.rpm']
        self.code_ext = ['.py','.java','.cpp', '.html', '.htm','.asp','.aspx', '.css', '.cgi', '.pl','.js', '.jsp', '.php', '.xhtml', '.c', '.class', '.cs', '.h', '.sh', '.swift', '.vb', '.cfm', '.cer']
        self.media_ext = ['.bin', '.dmg', '.iso','.toast', '.vcd']
        self.data_ext = ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml']
        self.app_ext = ['.apk','.bat','.bin','.cgi','.pl','.com','.exe','.gadget','.jar','.wsf']
        self.font_ext = ['.fnt','.fon','.otf','.ttf']
        self.sys_ext = ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.ink', '.msi', '.sys', '.tmp']
        self.flags = [".peta",'.seto']
        self.specifics = []
        self.all_files = {}
        self.errors = []
        self.file_structure = {}
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d-%m-%Y %Hh%M")
        self.nude_classifier = NudeClassifier()
        
        self.number_of_files = 0
        self.time_taken = 0
        self.prev_dir = None
        self.curr_dir = None

        self.master_ext = [self.doc_ext, self.img_ext, self.vid_ext, self.sound_ext, self.zip_ext, self.code_ext, self.media_ext, self.data_ext, self.app_ext, self.font_ext, self.sys_ext]

        self.type_s = ["Documents", "Images", "Videos", "Sounds", "Compressed_Files", "Programming_Files", "Discs_Media", "Databases", "Applications", "Fonts", "System_Files"]

        if specific_formats is not None and specific_folder is not None:
            self.specifics = self.specifics + specific_formats
            self.master_ext.append(self.specifics)
            
            self.type_s.append(specific_folder)
            

    def files(self, directory):
        
        if os.path.isdir(directory) == True:
            dir_list = os.listdir(directory)
            print("Listing dir")
            print(dir_list)
            print("Total size : ", len(dir_list))
            
            for file in dir_list:
                print(file)
                        
                if os.path.isdir(os.path.abspath(file)) == True:
                        #new_dir_list = os.listdir(file)
                        print()
                        print()
                        print(os.path.dirname(file))
                        self.files(os.path.abspath(file)) 
                else:
                    i = 0
                        
                    for extensions in self.master_ext:
                            
                        for ext in extensions:
                                
                            if ext in file:
                                    
                                self.lst_of[file] = self.type_s[i]
                        
                            
                            
                        i+=1
    def copy_(self, new_directory):
        if not os.path.exists(new_directory):
            os.mkdir(new_directory)
                        
            for key, value in self.lst_of.items():
                #new_directory = new_directory + value + "/"
                try:
                    print(key, new_directory + value + "/")
                    if not os.path.exists(new_directory + value + "/"):
                        os.mkdir(new_directory+ value + "/")
                        copy(key, new_directory+ value + "/")
                    else:
                        copy(key, new_directory + value + "/")
                except Exception as e:
                    print(e)
                    continue
                    
            
                            
        else:
            
            for key, value in self.lst_of.items():
                try:
                #new_directory = new_directory + value + "/"
                    print(key, new_directory + value + "/")
                    if not os.path.exists(new_directory + value + "/"):
                        os.mkdir(new_directory + value + "/")
                        copy(key, new_directory + value + "/")
                    else:
                        copy(key, new_directory + value + "/")                      
                except Exception as e:
                    print(e)
                    continue
    def move_(self, new_directory):
        if not os.path.exists(new_directory):
            os.mkdir(new_directory)
                        
            for key, value in self.lst_of.items():
                #new_directory = new_directory + value + "/"
                try:
                    print(key, new_directory + value + "/")
                    if not os.path.exists(new_directory + value + "/"):
                        os.mkdir(new_directory+ value + "/")
                        move(key, new_directory+ value + "/")
                    else:
                        move(key, new_directory + value + "/")
                except Exception as e:
                    print(e)
                    continue
                    
            
                            
        else:
            
            for key, value in self.lst_of.items():
                try:
                #new_directory = new_directory + value + "/"
                    print(key, new_directory + value + "/")
                    if not os.path.exists(new_directory + value + "/"):
                        os.mkdir(new_directory + value + "/")
                        move(key, new_directory + value + "/")
                    else:
                        move(key, new_directory + value + "/")                      
                except Exception as e:
                    print(e)
                    continue
    def display(self, dic):
    
        for key, value in dic.items():
            try:
                print(key, value)
            except Exception as e:
                print(e)
                continue
    
    def rollback(self, files, prev_dir, curr_dir):
        
        if len(files) < 0:
            print("Please provide the files that you want to undo the process.")
            return 
            
        if type(files) is not dict:
            print("files should be list, but ", type(files), " was provided instead.")
            return
            
        if not os.path.isdir(prev_dir):
            print("The provide previous directory is not a directory or doesn't exist, please check ", prev_dir)
            return 
        
        if not os.path.isdir(curr_dir):
            print("The provide current directory is not a directory or doesn't exist, please check ", curr_dir)
            return
        
        print("Rollback Operation started : from - ", curr_dir, " to  - ", prev_dir)
        
        dir_walk = os.walk(curr_dir)
        new_files = {}
        
        for (root, dirs, files_) in dir_walk:
            
            for f in files_:
                for file, full_path in files.items():
                    
                    if f == file:
                        
                        new_files[os.path.join(root, f)] = full_path
        
        print(new_files)
        for each_file, fullpath in new_files.items():
            try:
                print("FROM -- [", each_file, "] TO -- [", fullpath, "] success")
                move(each_file, fullpath)
            
            except Exception as e:
                print(e)
                continue
            
        
            
        
    
    #Todo rollback code here
    #Main function is to reverse any sorting done by the program 
    # 1. Get all the files and their paths
    # 2. Move them from their curr directory to their previous directories
    # 3. Verify and check if the operation was successful
    # 4. Save the progress for later use
    
    def check_for_porn(self, directory):
        

        profane_pic = 0
        file_sess = "profanity.check"
        print("Checking for nudity and pornographic material...", directory)
        directory = directory + "/images"
        
        profanity = directory + "/"+ "Profanity"
        
        file_s = directory + "/" + file_sess
        
        if os.path.exists(file_s) is False:
            
            f = open(file_s, 'w+')
        else:
            f = open(file_s, 'a+')
        previous_session = open(file_s, 'r').readlines()
        previous_session = [i.strip() for i in previous_session]
        print(file_s, len(previous_session), previous_session )
       
        if os.path.isdir(profanity) is False:
            os.mkdir(profanity)
        
        if os.path.isdir(directory) is True:
            
            images = os.listdir(directory)
            
            for each_pic in images:
                
                
                    
                
                    
                    if (each_pic in previous_session) is True:
                        print("Skipping file", each_pic, "already scanned")
                        continue
                    
                    elif each_pic not in previous_session:
                        f.write(each_pic+"\n")
                        preds = self.nude_classifier.classify(os.path.abspath(directory + "/"+ each_pic))
                        
                        #print(preds, type(preds))
                        for (path, dicti) in preds.items():
                            
                            
                            for lvl , score in dicti.items():
                                if lvl is 'unsafe' and score >= 0.9:
                                    print(f"Profanity detected ", f"Image ({each_pic}) MOVING to {profanity}...")
                                    move(path, os.path.abspath(profanity))
                                    profane_pic += 1
                        #print(preds)
                        
                        #f.append(each_pic+"\n")
                    else:
                        
                        f.write(each_pic+"\n")
        print(f"Process done. Moved {profane_pic} profane files to {profanity}")
    def sort_dir(self, directory):
        
        self.prev_dir = directory
 
        #given a dir, check if its a dir or not
        print("Starting sorting operation...", directory)
        if os.path.isdir(directory) == True:
            #print("Listing dir")
            dir_list = os.walk(directory)
            #print(dir_list)
            #print("Total size : ", len(dir_list))
            
            for (root,dirs,files) in dir_list:
                
                self.number_of_files = len(files)
           
                    
                #print(files)    
                
                
                i = 0
                
                print("files LEN ", self.number_of_files, " DIRS LEN ", len(dirs), "root " , root, "dirs ", dirs, "files ", files)
                
                for direct in dirs:
                    full_dir = os.path.join(root, direct)
                    
                    if os.path.isdir(full_dir) is True:
                        full_dir_files = os.listdir(full_dir)
                        
                        self.file_structure[full_dir] =  full_dir_files
                    
                for extensions in self.master_ext:
                        
                    for ext in extensions:
                            
                        for file in files:
                                
                            if ext in file:
                                #print("ROOT ", root, "DIRECTORIES : ", dirs, "FILES ", files)
                                self.lst_of[os.path.join(root, file)] = self.type_s[i]
                                
                                #self.all_files.append(file)
                                self.all_files[file] = os.path.join(root, file)
                                
                                
                    
                        
                    i+=1
                
                
                
            
        
        
            
            print(self.file_structure)
            print(len(self.file_structure))
            xml = dicttoxml.dicttoxml(self.file_structure)
            tree = ET.XML(xml)
            print("XML " , tree)
            
            new_directory = input("Please enter name of new directory...")
                        
            new_directory = "X:/" + new_directory+"_"+os.path.basename(directory)
            
            filename = "session_"+str(self.dt_string)+".xml"
            full_filename = str(os.path.abspath(os.path.join(new_directory, filename)))
            print(full_filename, self.dt_string,  "string : ", ET.tostring(tree))
            
            
            
            f = open(full_filename, "wb")
            f.write(ET.tostring(tree))
            f.close()
                
            
            
                        
            self.curr_dir = new_directory
            print(new_directory)
            print(self.lst_of)
            self.display(self.lst_of)
            if self.mode == 'move':
                self.move_(new_directory)
            else:
                self.copy_(new_directory)
                
            
            choice = input(f"Operation {self.mode} is don, Are you sure you want to continue or Rollback the process Y - Yes(Rollback) / N - No(Continue)?")
            choice = choice.lower()
            if "y" in choice or choice is "y" or choice is "yes" or "yes" in choice :
                #prev_dir = input("Please enter the previous directory where the files where located before operation")
                #curr_dir = input("Please enter the current directory where the files where are located now")
                self.rollback(self.all_files, self.prev_dir, self.curr_dir)
                
                print("Rollback operation successfully files where placed back to their original places.")
            threading.Thread(target=self.check_for_porn(new_directory)).start()
              
        
    
    
srt = sorter()

srt.sort_dir(r"X:/cs2018bsc")





