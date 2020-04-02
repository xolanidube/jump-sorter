# MIT License
# 
# Copyright (c) 2020 Xolani Dube and Surprise Ngoveni
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.




#Given a directory or a set of directories or a full hard drive the program should automatically sort files based on their names, types, sizes and
#other meta data related to the files and also first the program should crawl the given directory or a set of directories or a hard drive and then find 
#the file types and other meta data revelant data and then based on user preference is should sort the files and put according to how the user wants
#them to be.
# 

#Also integrate A.I that will automatically sort the files based on their content inside them and actually read and write files of users like allowing
#the user to edit their files.
#Include face detection and verification for images 




import os
import threading
import time
from shutil import *
import dicttoxml
from datetime import datetime
from xml.etree import ElementTree as ET
from nudenet import NudeClassifier
from nudenet import NudeDetector
import cv2
from PySide2 import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sched, time
import face as fc
import numpy as np


__version__ = '0.0.1'
__author__ = 'Emmanuel Xolani Dube'
__contact__ = "xolanidube575@gmail.com"

#THERE MUST BE A DIRECTORY ENTERED FIRST
#THE PROGRAM SHOULD CRAWL OVER ALL THE DIRECTORIES AND FILES IF ANY IN THE LISTED DIRECTORY ABOVE
#THEN IT SHOULD SHOW THE USER ALL THE FILES IT HAS FOUND AND HOW IT WILL SORT THE FILES OUT
#THE USER IS ALLOWED TO MAKE EDITS AND CHANGES
#THEN THE PROGRAM SORTS THE FILES 
#


class sorter():
    
    def __init__(self, mode, specific_formats=None, specific_folder=None):
        
        self.mode = mode;
        self.lst_of = {}
        self.doc_ext = []
        self.img_ext = []
        self.vid_ext = []
        self.sound_ext = []
        self.zip_ext = []
        self.code_ext = []
        self.media_ext = []
        self.data_ext = []
        self.app_ext = []
        self.font_ext = []
        self.sys_ext = []
        self.flags = []
        self.specifics = []
        self.all_files = {}
        self.errors = []
        self.file_structure = {}
        self.load_ext()
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d-%m-%Y %Hh%M")
        self.nude_classifier = NudeClassifier()
        self.nude_detector = NudeDetector()
        self.s = sched.scheduler(time.time, time.sleep)
        
        self.number_of_files = 0
        self.time_taken = 0
        self.prev_dir = None
        self.curr_dir = None
        self.faces = None
        self.points = None
        

        self.walked_dir = "checked.dir"
        self.all_walked = []
        self.load_walked()

        self.available_dirs = []
        self.non_available_dirs = []
        self.attach = ":/"
        self.let_dir = ["A","B","C","D","E","F","G","H","I","J","K",
                        "L","M","N","O","P","Q","R","S","T","U","V",
                        "W","X","Y","Z"]

        self.runt = threading.Thread(target=self.find_all_dirs)
        self.runt.start()
        
        self.master_ext = [self.doc_ext, self.img_ext, self.vid_ext, self.sound_ext, self.zip_ext, self.code_ext, self.media_ext, self.data_ext, self.app_ext, self.font_ext, self.sys_ext, self.flags]

        self.type_s = ["Documents", "Images", "Videos", "Sounds", "Compressed_Files", "Programming_Files", "Discs_Media", "Databases", "Applications", "Fonts", "System_Files", "Infected"]


        self.face_detection = fc.Detection()
        self.face_recognition = fc.Recognition()
        self.face_verification = fc.Verification()
        
        
        
        if specific_formats is not None and specific_folder is not None:
            self.specifics = self.specifics + specific_formats
            self.master_ext.append(self.specifics)
            
            self.type_s.append(specific_folder)

    def get_mode(self):
        return self.__mode


    def get_lst_of(self):
        return self.__lst_of


    def get_doc_ext(self):
        return self.__doc_ext


    def get_img_ext(self):
        return self.__img_ext


    def get_vid_ext(self):
        return self.__vid_ext


    def get_sound_ext(self):
        return self.__sound_ext


    def get_zip_ext(self):
        return self.__zip_ext


    def get_code_ext(self):
        return self.__code_ext


    def get_media_ext(self):
        return self.__media_ext


    def get_data_ext(self):
        return self.__data_ext


    def get_app_ext(self):
        return self.__app_ext


    def get_font_ext(self):
        return self.__font_ext


    def get_sys_ext(self):
        return self.__sys_ext


    def get_flags(self):
        return self.__flags


    def get_specifics(self):
        return self.__specifics


    def get_all_files(self):
        return self.__all_files


    def get_errors(self):
        return self.__errors


    def get_file_structure(self):
        return self.__file_structure


    def get_now(self):
        return self.__now


    def get_dt_string(self):
        return self.__dt_string


    def get_nude_classifier(self):
        return self.__nude_classifier


    def get_number_of_files(self):
        return self.__number_of_files


    def get_time_taken(self):
        return self.__time_taken


    def get_prev_dir(self):
        return self.__prev_dir


    def get_curr_dir(self):
        return self.__curr_dir


    def get_master_ext(self):
        return self.__master_ext


    def get_type_s(self):
        return self.__type_s


    def set_mode(self, value):
        self.__mode = value


    def set_lst_of(self, value):
        self.__lst_of = value


    def set_doc_ext(self, value):
        self.__doc_ext = value


    def set_img_ext(self, value):
        self.__img_ext = value


    def set_vid_ext(self, value):
        self.__vid_ext = value


    def set_sound_ext(self, value):
        self.__sound_ext = value


    def set_zip_ext(self, value):
        self.__zip_ext = value


    def set_code_ext(self, value):
        self.__code_ext = value


    def set_media_ext(self, value):
        self.__media_ext = value


    def set_data_ext(self, value):
        self.__data_ext = value


    def set_app_ext(self, value):
        self.__app_ext = value


    def set_font_ext(self, value):
        self.__font_ext = value


    def set_sys_ext(self, value):
        self.__sys_ext = value


    def set_flags(self, value):
        self.__flags = value


    def set_specifics(self, value):
        self.__specifics = value


    def set_all_files(self, value):
        self.__all_files = value


    def set_errors(self, value):
        self.__errors = value


    def set_file_structure(self, value):
        self.__file_structure = value


    def set_now(self, value):
        self.__now = value


    def set_dt_string(self, value):
        self.__dt_string = value


    def set_nude_classifier(self, value):
        self.__nude_classifier = value


    def set_number_of_files(self, value):
        self.__number_of_files = value


    def set_time_taken(self, value):
        self.__time_taken = value


    def set_prev_dir(self, value):
        self.__prev_dir = value


    def set_curr_dir(self, value):
        self.__curr_dir = value


    def set_master_ext(self, value):
        self.__master_ext = value


    def set_type_s(self, value):
        self.__type_s = value


    def del_mode(self):
        del self.__mode


    def del_lst_of(self):
        del self.__lst_of


    def del_doc_ext(self):
        del self.__doc_ext


    def del_img_ext(self):
        del self.__img_ext


    def del_vid_ext(self):
        del self.__vid_ext


    def del_sound_ext(self):
        del self.__sound_ext


    def del_zip_ext(self):
        del self.__zip_ext


    def del_code_ext(self):
        del self.__code_ext


    def del_media_ext(self):
        del self.__media_ext


    def del_data_ext(self):
        del self.__data_ext


    def del_app_ext(self):
        del self.__app_ext


    def del_font_ext(self):
        del self.__font_ext


    def del_sys_ext(self):
        del self.__sys_ext


    def del_flags(self):
        del self.__flags


    def del_specifics(self):
        del self.__specifics


    def del_all_files(self):
        del self.__all_files


    def del_errors(self):
        del self.__errors


    def del_file_structure(self):
        del self.__file_structure


    def del_now(self):
        del self.__now


    def del_dt_string(self):
        del self.__dt_string


    def del_nude_classifier(self):
        del self.__nude_classifier


    def del_number_of_files(self):
        del self.__number_of_files


    def del_time_taken(self):
        del self.__time_taken


    def del_prev_dir(self):
        del self.__prev_dir


    def del_curr_dir(self):
        del self.__curr_dir


    def del_master_ext(self):
        del self.__master_ext


    def del_type_s(self):
        del self.__type_s

    def run_t(self):
        self.s.enter(60, 1, self.find_all_dirs, (self.s,));
        self.s.run()
    
    def find_all_dirs(self):
        
        for i in range(len(self.let_dir)):
            dr = self.let_dir[i]+self.attach
            if os.path.isdir(dr):
                self.available_dirs.append(dr)
            else:
                self.non_available_dirs.append(dr)


        #self.s.enter(60, 1, self.find_all_dirs, (self.s,))


    def load_ext(self):
        extensions_path = "C:/Users/GabhaDi/eclipse-workspace2/project sortMyFiles/src/extensions/"
        name = ["application","code","data","document","flags","font","image",
                "media","sound","system","video","zip"]
        #full_path = os.path.abspath(extensions_path)

        i = 0

        print("The full to your extensions is ", extensions_path)

        if os.path.isdir(extensions_path) is True:
            print("loading all extensions...")
            list_files = os.listdir(extensions_path)
            
            for file in list_files:


                if "document" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.doc_ext.append(line.rstrip("\n"))

                    print("Successfully loaded document exts, size : ", len(self.doc_ext), self.doc_ext)


                if "image" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.img_ext.append(line.rstrip("\n"))

                    print("Successfully loaded image exts, size : ", len(self.img_ext), self.img_ext)


                if "video" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.vid_ext.append(line.rstrip("\n"))

                    print("Successfully loaded video exts, size : ", len(self.vid_ext), self.vid_ext)

                
               
                if "application" in file:
                    
                    with open(extensions_path+file) as f:
                        for line in f:
                            self.app_ext.append(line.rstrip("\n"))

                    print("Successfully loaded app exts, size : ", len(self.app_ext), self.app_ext)
               
                if "code" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.code_ext.append(line.rstrip("\n"))

                    print("Successfully loaded source code exts, size : ", len(self.code_ext), self.code_ext)

                
                    
                if "data" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.data_ext.append(line.rstrip("\n"))

                    print("Successfully loaded database exts, size : ", len(self.data_ext), self.data_ext)

                

                
                

               
                    
                            
                if "flags" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.flags.append(line.rstrip("\n"))

                    print("Successfully loaded dangerous and malicious exts, size : ", len(self.flags), self.flags)


                


                if "font" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.font_ext.append(line.rstrip("\n"))

                    print("Successfully loaded font exts, size : ", len(self.font_ext), self.font_ext)

                

                

              

                if "media" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.media_ext.append(line.rstrip("\n"))

                    print("Successfully loaded media exts, size : ", len(self.media_ext), self.media_ext)

                

                if "sound" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.sound_ext.append(line.rstrip("\n"))

                    print("Successfully loaded sound and audio exts, size : ", len(self.sound_ext), self.sound_ext)

               

                if "system" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.sys_ext.append(line.rstrip("\n"))

                    print("Successfully loaded system exts, size : ", len(self.sys_ext), self.sys_ext)

                

                

                

                if "zip" in file:

                    with open(extensions_path+file) as f:
                        for line in f:
                            self.zip_ext.append(line.rstrip("\n"))

                    print("Successfully loaded archive and compressions exts, size : ", len(self.zip_ext), self.zip_ext)

                
            print("Successfully loaded all extensions...")
                
    def load_walked(self):
        
        if os.path.isfile(self.walked_dir):
                
            with open(self.walked_dir) as f:
                for line in f:
                    self.all_walked.append(line.rstrip("\n"))
        else:
            print("File doesnt't exist.")

	
    def load_session(self, dir):
            
        if len(self.all_files) != 0:
                self.all_files.clear()
        all_files = []	
        pc = []
        if os.path.isdir(dir) == True:
            dir_list = os.listdir(dir)
            session = "session.sess"
            session_cp = "session_cp.sess"
            if(session in dir_list) is True and (session_cp in dir_list) is True:
                with open(session) as f:
                    for line in f:
                        all_files.append([int(n) for n in line.strip().split(',')])
                    for pair in all_files:
                        try:
                            self.all_files[pair[0]] = pair[1]
                        except IndexError:
                            print("A line in the file doesn't have enough entries")
                                        
                    with open(session_cp) as fn:
                        for line in fn:
                            pc.append([int(n) for n in line.strip().split(',')])
                        
                        for pair in pc:
                            try:
                                self.prev_dir = pair[0]
                                self.curr_dir = pair[1]
                            except IndexError:
                                print("A line in the file doesn't have enough entries")
                    print(f"Successfully loaded sessions for from files {session} and {session_cp} from directory {dir}")
                    return 1
            else:
                    print(f"Something went wrong...i couldnt find the files {session} and {session_cp} in dir")
                    return -1
        else:
            print(f"Something went wrong...invalid directory provided ERROR : {dir} doesn't exist")
            return -1
	
    def add_dir(self, new_dir):

        
        
        if(os.path.exists(self.walked_dir) == False):
            f = open(self.walked_dir, "w+")
        else:
            f = open(self.walked_dir, "a+")

        _checked = open(self.walked_dir, 'r').readlines()
        _checked = [i.strip() for i in _checked]
        
        if (new_dir in _checked) is True:
            print("Skipping ", new_dir, " it has been added.")
            
        elif new_dir not in _checked:
            
            f.write(new_dir+"\n")
        else:
            f.write(new_dir+"\n")

        f.close()
    

    def files(self, directory):
        total_files = 0
        total_directories = 0
        if os.path.isdir(directory) == True:
            dir_list = os.listdir(directory)
            print("Listing dir")
            print(dir_list)
            print("Total size : ", len(dir_list))
            
            for file in dir_list:
                print(file)
                if os.path.isfile(os.path.abspath(file) == True):
                    i = 0
                        
                    for extensions in self.master_ext:
                            
                        for ext in extensions:
                                
                            if ext in file:
                                    
                                self.lst_of[file] = self.type_s[i]
								
                if os.path.isdir(os.path.abspath(file)) == True:
                        #new_dir_list = os.listdir(file)
                        print()
                        print()
                        print(os.path.dirname(file))
                        self.files(os.path.abspath(file)) 
				
                
                        
                            
                            
                        i+=1
    def copy_(self, new_directory):
        if not os.path.exists(new_directory):
            os.mkdir(new_directory)
                        
            for key, value in self.lst_of.items():
                #new_directory = new_directory + value + "/"
                try:
                    print(key, new_directory +"/"+ value + "/")
                    if not os.path.exists(new_directory +"/"+ value + "/"):
                        os.mkdir(new_directory +"/"+ value + "/")
                        copy(key, new_directory +"/"+ value + "/")
                    else:
                        copy(key, new_directory +"/"+ value + "/")
                except Exception as e:
                    print(e)
                    continue
                    
            
                            
        else:
            
            for key, value in self.lst_of.items():
                try:
                #new_directory = new_directory + value + "/"
                    print(key, new_directory +"/"+ value + "/")
                    if not os.path.exists(new_directory +"/"+ value + "/"):
                        os.mkdir(new_directory +"/"+ value + "/")
                        copy(key,new_directory +"/"+ value + "/")
                    else:
                        copy(key, new_directory +"/"+ value + "/")                      
                except Exception as e:
                    print(e)
                    continue
    def move_(self, new_directory):
        if not os.path.exists(new_directory):
            os.mkdir(new_directory)
                        
            for key, value in self.lst_of.items():
                #new_directory = new_directory + value + "/"
                try:
                    print(key, new_directory +"/"+ value + "/")
                    if not os.path.exists(new_directory +"/"+ value + "/"):
                        os.mkdir(new_directory +"/"+ value + "/")
                        move(key, new_directory +"/"+ value + "/")
                    else:
                        move(key, new_directory +"/"+ value + "/")
                except Exception as e:
                    print(e)
                    continue
                    
            
                            
        else:
            
            for key, value in self.lst_of.items():
                try:
                #new_directory = new_directory + value + "/"
                    print(key, new_directory +"/"+ value + "/")
                    if not os.path.exists(new_directory +"/"+ value + "/"):
                        os.mkdir(new_directory +"/"+ value + "/")
                        move(key, new_directory +"/"+ value + "/")
                    else:
                        move(key, new_directory +"/"+ value + "/")                      
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
            print("The provided previous directory is not a directory or doesn't exist, please check ", prev_dir)
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
            
    def display(self, dic):
	
        for key, value in dic.items():
            try:
                print(key, value)
            except Exception as e:
                print(e)
                continue
            
        
    
    #Todo rollback code here
    #Main function is to reverse any sorting done by the program 
    # 1. Get all the files and their paths
    # 2. Move them from their curr directory to their previous directories
    # 3. Verify and check if the operation was successful
    # 4. Save the progress for later use


    def check_for_faces(self, directory):

        (self.im_width, self.im_height) = (160, 160)
        face_pic = 0
        file_sess = "face.check"
        print("Checking for faces...", directory)

        directory = directory + "/images"

        face_ = directory + "/" + "faces"

        file_s = directory + "/" + file_sess

        if os.path.exists(file_s) is False:
            f = open(file_s, 'w+')
        else:
            f = open(file_s, 'a+')

        previous_session = open(file_s, 'r').readlines()
        previous_session = [i.strip() for i in previous_session]
        print(file_s, len(previous_session), previous_session )
        
        


        if os.path.isdir(face_) is False:
            os.mkdir(face_)


        
        
        if os.path.isdir(directory) is True:
            images = os.listdir(directory)

            for each_pic in images:
                 self.pin = (sorted([int(n[: n.find(".")]) for n in os.listdir(face_) if n[0] != "."] + [0])[-1] + 1)
                 if (each_pic in previous_session) is True:
                    print("Skipping file", each_pic, "already scanned")
                    continue
                    
                 elif each_pic not in previous_session:
                    f.write(each_pic+"\n")

                    try:
                        image = cv2.imread(os.path.abspath(directory+"/"+each_pic), 1)

                        normal = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        normal = cv2.cvtColor(normal, cv2.COLOR_RGB2BGR)
                       
                            

                        if self.face_recognition.detection(image) is None:
                            faces = None

                        if self.face_recognition.detection(image) is not None:
                            faces, points = self.face_recognition.detection(image)

                        if faces is not None:
                            for face in faces:
                                face_bb = face.bounding_box.astype(int)

                                yourface = normal[max(0, face_bb[1]) : min(face_bb[3], normal.shape[0] - 1),
                                                 max(0, face_bb[0]) : min(face_bb[2], normal.shape[1] - 1),]

                                for i in range(points.shape[1]):
                                    pts = points[:, i].astype(np.int32)
                                    for j in range(pts.size // 2):
                                        pt = (pts[j], pts[5 + j])
                                        cv2.circle(image, center=pt, radius=1, color=(255, 0, 0), thickness=2,)



                                face_resize = cv2.resize(yourface, (self.im_width, self.im_height))

                                cv2.rectangle(image, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),(22, 20, 60), 1,)
                                
                                
                                cv2.imwrite("%s/%s.png" % (face_, self.pin), face_resize)

                                print(f"Face detected in image {each_pic} now creating face in {face_+'/'+str(self.pin)}.png")

                                face_pic += 1
                        
                                
                                cv2.destroyAllWindows()
                    except:
                        continue
                 else:
                    f.write(each_pic+"\n")
                

        print(f"Process done. Created {face_pic} face files to {face_+'/'}")                    
        

    
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

                                elif lvl is 'unsafe' and score >=.6 and score < 0.9:

                                    print(f"Indecency detected ", f"Am not sure about Image ({each_pic}) should i move it to {profanity}...")

                                    image = cv2.imread(path, 1)
                                    width = 320
                                    height = 320
                                    
                                    dim = (width, height)
                                    try:
                                        resized_img = cv2.resize(image, dim, cv2.INTER_AREA)
                                        cv2.imshow("SUGGESTION", resized_img)
                                    except:
                                        print(e)
                                        continue
                                    print(f" Move {path} Press(y) to move or n to continue?")
                                    k = cv2.waitKey(0)
                                    

                                    if(k == ord('y')):
                                        move(path, os.path.abspath(profanity))
                                        profane_pic += 1
                                        cv2.destroyAllWindows()
                                        print(f"Suggestion moved {path} to {profanity}")
                                    else:
                                        cv2.destroyAllWindows()
                                        continue
                                        
                                    
                                    
                        #print(preds)
                        
                        #f.append(each_pic+"\n")
                    else:
                        
                        f.write(each_pic+"\n")
        print(f"Process done. Moved {profane_pic} profane files to {profanity}")

    def save_session(self, fls, prev, curr):

        #if(type(self.files) is not dict):
        
        #    print(f"Must be dictionary not {type(files)}")
        #    return
        

        if(len(fls) == 0):
        
            print("print data not provided its empty")
            return
        

        if(os.path.isdir(prev) == False):
        
            print("Please provide a valid directory ERROR : ", prev)
        

        if(os.path.isdir(curr) == False):
        
            print("Please provide a valid directory ERROR : ", curr)
        

        filename = "session.sess"
        full_filename = str(os.path.abspath(os.path.join(curr, filename)))
        #full_dr = new_directory + "/" + filename
        print(full_filename, self.dt_string,  "string : ", fls)
        fn = "session_cp.sess"
        full_fn = str(os.path.abspath(os.path.join(curr, fn)))


        if os.path.exists(full_filename) is False:
            f = open(full_filename, 'w+', encoding="utf-8")
            fp = open(full_fn, 'w+', encoding="utf-8")
            fp.write(prev+","+curr+"\n")
        else:
            f = open(full_filename, 'a+', encoding="utf-8")
            fp = open(full_fn, 'w+', encoding="utf-8")
            fp.write(prev+","+curr+"\n")

        _checked_ = open(full_filename, 'r').readlines()
        _checked_ = [i.strip() for i in _checked_]
        
        for file, dr in self.all_files.items():
            x = file+","+ dr
            if(x in _checked_):
                print("Skipping ", x, "it has been added")
                continue
            elif x not in _checked_:
            
                f.write(x+"\n")
            else:
                f.write(x+"\n")

        f.close()
        fp.close()

        print("Successfully Saved session at " , self.dt_string)
    

    
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

                            try:
                                EXT_ = file.split(".")[1]
                                EXT_ = "."+EXT_
                                if EXT_ == ext:
                                    #print("ROOT ", root, "DIRECTORIES : ", dirs, "FILES ", files)
                                    self.lst_of[os.path.join(root, file)] = self.type_s[i]
                                    print("TYPE : ", self.type_s[i], "FILE EXT FOUND : ", ext, "FILE NAME : ",os.path.join(root, file), "ITER : ", i , EXT_)
                                    
                                    #self.all_files.append(file)
                                    self.all_files[file] = os.path.join(root, file)
                            except:
                                print("ERROR WITH FILE : ", file)
                                continue
                                
                                
                    
                        
                    i+=1
                
                
                
            
        
        
            
            
            
            new_directory = input("Please enter name of new directory...")

            print("Available dirs please choose which dir to " , self.mode , " to?")
            self.runt.join()
            for i in range(len(self.available_dirs)):
                print(i, self.available_dirs[i])

            choice =  input("Please choose directory?")
            
            while True:
                
                if int(choice) < 0 or int(choice) > len(self.available_dirs):
                    print("Invalid choice!!!, Please choose again.")
                    choice =  input("Please choose directory?")
                    continue
                else:
                    break
                
                    
            new_directory = self.available_dirs[int(choice)] + new_directory+"_"+os.path.basename(directory)

                        
            self.curr_dir = new_directory
            print(new_directory)
            print(self.lst_of)
            self.display(self.lst_of)
            if self.mode == 'move':
                self.move_(new_directory)
            else:
                self.copy_(new_directory)

            self.save_session(self.all_files, self.prev_dir, self.curr_dir)

            self.add_dir(new_directory)
            print("All files : ", self.all_files, " Previous Directory : " , self.prev_dir, " Current Directory : ", self.curr_dir);
            
            choice = input(f"Operation {self.mode} is done, Are you sure you want to continue or Rollback the process Y - Yes(Rollback) / N - No(Continue)?")
            choice = choice.lower()
            if "y" in choice or choice is "y" or choice is "yes" or "yes" in choice :
                #prev_dir = input("Please enter the previous directory where the files where located before operation")
                #curr_dir = input("Please enter the current directory where the files where are located now")
                self.rollback(self.all_files, self.prev_dir, self.curr_dir)
                
                print("Rollback operation successfully files where placed back to their original places.")

            threading.Thread(target=self.check_for_porn(new_directory)).start()

        else:

            print("Directory doesn't exist : ", directory, "Please enter a valid directory!")

            path = input("Please enter the directory or folder or file path you want to sort?")
            srt.sort_dir(rf"{path}")
    
    mode = property(get_mode, set_mode, del_mode, "mode's docstring")
    lst_of = property(get_lst_of, set_lst_of, del_lst_of, "lst_of's docstring")
    doc_ext = property(get_doc_ext, set_doc_ext, del_doc_ext, "doc_ext's docstring")
    img_ext = property(get_img_ext, set_img_ext, del_img_ext, "img_ext's docstring")
    vid_ext = property(get_vid_ext, set_vid_ext, del_vid_ext, "vid_ext's docstring")
    sound_ext = property(get_sound_ext, set_sound_ext, del_sound_ext, "sound_ext's docstring")
    zip_ext = property(get_zip_ext, set_zip_ext, del_zip_ext, "zip_ext's docstring")
    code_ext = property(get_code_ext, set_code_ext, del_code_ext, "code_ext's docstring")
    media_ext = property(get_media_ext, set_media_ext, del_media_ext, "media_ext's docstring")
    data_ext = property(get_data_ext, set_data_ext, del_data_ext, "data_ext's docstring")
    app_ext = property(get_app_ext, set_app_ext, del_app_ext, "app_ext's docstring")
    font_ext = property(get_font_ext, set_font_ext, del_font_ext, "font_ext's docstring")
    sys_ext = property(get_sys_ext, set_sys_ext, del_sys_ext, "sys_ext's docstring")
    flags = property(get_flags, set_flags, del_flags, "flags's docstring")
    specifics = property(get_specifics, set_specifics, del_specifics, "specifics's docstring")
    all_files = property(get_all_files, set_all_files, del_all_files, "all_files's docstring")
    errors = property(get_errors, set_errors, del_errors, "errors's docstring")
    file_structure = property(get_file_structure, set_file_structure, del_file_structure, "file_structure's docstring")
    now = property(get_now, set_now, del_now, "now's docstring")
    dt_string = property(get_dt_string, set_dt_string, del_dt_string, "dt_string's docstring")
    nude_classifier = property(get_nude_classifier, set_nude_classifier, del_nude_classifier, "nude_classifier's docstring")
    number_of_files = property(get_number_of_files, set_number_of_files, del_number_of_files, "number_of_files's docstring")
    time_taken = property(get_time_taken, set_time_taken, del_time_taken, "time_taken's docstring")
    prev_dir = property(get_prev_dir, set_prev_dir, del_prev_dir, "prev_dir's docstring")
    curr_dir = property(get_curr_dir, set_curr_dir, del_curr_dir, "curr_dir's docstring")
    master_ext = property(get_master_ext, set_master_ext, del_master_ext, "master_ext's docstring")
    type_s = property(get_type_s, set_type_s, del_type_s, "type_s's docstring")
              
        
    
mode = input("Please enter the mode (copy or move)?")
time.sleep(5)
srt = sorter(mode.lower())

while True:

    
    print("1. Check for faces\n",
          "2. Check for Indecency\n",
          "3. Sort a folder/directory\n",
          "#. Press 0 to Exit!\n")
    choice = input("Enter please your option:")
    if int(choice) is 1:
        for i in range(len(srt.all_walked)):
            print(i, srt.all_walked[i])
        opt = input("\nPlease choose a directory\n")
        if int(opt) < 0 or int(opt) > len(srt.all_walked):
            print("invalid option!!!, please enter a valid option!")
            continue
            
        else:

            srt.check_for_faces(srt.all_walked[int(opt)])

        continue

    elif int(choice) is 2:
        for i in range(len(srt.all_walked)):
            print(i, srt.all_walked[i])
        opt = input("\nPlease choose a directory\n")
        if int(opt) < 0 or int(opt) > len(srt.all_walked):
            print("invalid option!!!, please enter a valid option!")
            continue
            
        else:

            srt.check_for_porn(srt.all_walked[int(opt)])

        continue
    elif int(choice) is 3:
        

        path = input("Please enter the directory or folder or file path you want to sort?")
        srt.sort_dir(rf"{path}")
    elif int(choice) is 0:
        break
    else:
        print("Invalid choice please choose a valid option!")
        continue

            
            
            



