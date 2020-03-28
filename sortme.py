# MIT License
# 
# Copyright (c) 2020 Xolani Dube 
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
import cv2

















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
        self.flags = ['.peta','.seto']
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
        

        self.walked_dir = "checked.dir"
        self.all_walked = []

        self.master_ext = [self.doc_ext, self.img_ext, self.vid_ext, self.sound_ext, self.zip_ext, self.code_ext, self.media_ext, self.data_ext, self.app_ext, self.font_ext, self.sys_ext, self.flags]

        self.type_s = ["Documents", "Images", "Videos", "Sounds", "Compressed_Files", "Programming_Files", "Discs_Media", "Databases", "Applications", "Fonts", "System_Files", "Infected"]

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

    def load_walked(self):
        return 0

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
                                    cv2.imshow("SUGGESTION", image)
                                    k = cv2.waitKey(0)
                                    print(f" Move {path} Press(y) to move or n ?")

                                    if(k == ord('y')):
                                        move(path, os.path.abspath(profanity))
                                        profane_pic += 1
                                        cv2.destroyAllWindows()
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
            f = open(full_filename, 'w+')
            fp = open(full_fn, 'w+')
            fp.write(prev+","+curr+"\n")
        else:
            f = open(full_filename, 'a+')
            fp = open(full_fn, 'w+')
            fp.write(prev+","+self.curr+"\n")

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
                                
                            if ext in file:
                                #print("ROOT ", root, "DIRECTORIES : ", dirs, "FILES ", files)
                                self.lst_of[os.path.join(root, file)] = self.type_s[i]
                                
                                #self.all_files.append(file)
                                self.all_files[file] = os.path.join(root, file)
                                
                                
                    
                        
                    i+=1
                
                
                
            
        
        
            
            
            
            new_directory = input("Please enter name of new directory...")
                        
            new_directory = "X:/" + new_directory+"_"+os.path.basename(directory)

                        
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
              
        
mode = "copy"
srt = sorter(mode)

srt.sort_dir(r"YOUR_DIRECTORY_HERE")





