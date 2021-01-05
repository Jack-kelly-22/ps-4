from dtypes.imageData import ImageData
import time
from os import mkdir
import sqlite3
from utils.sql_utils import adapt_array,convert_array
from numpy import ndarray,array
import uuid
import os
class Frame:

    def get_images_in_path(self,path):
        imgs = os.listdir(path)
        imgs_paths = []
        for img in imgs:
            if(img[0]!="."):
                imgs_paths.append(path + "/" +img)
        return imgs_paths


    def __init__(self,path,out,inspect_mode,constants,db_ref,jname,tags):
        """
        name: what to call the frame
        image_ls: list of images paths
        inspect_mode: light/dark
        """
        self.name = os.path.basename(os.path.normpath(path))
        self.job_name = jname
        self.image_paths = self.get_images_in_path(path)
        self.tags = tags
        self.type = inspect_mode
        self.out_path = out
        self.id = str(uuid.uuid4()).replace('-','') + "_" + self.name
        self.constants = constants
        self.image_data_ls = []
        self.image_ref_ls = []
        self.avg_pore = 0
        self.db_ref = db_ref
        mkdir("./job-data/" +self.job_name + '/' +self.name)
        self.process_frame()
        self.add_frame_db()

    def add_frame_db(self):
        sqlite3.register_adapter(ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        conn = sqlite3.connect(
            "/Users/jackkelly/PycharmProjects/win_break/dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        out_path = "./job-data/" +self.job_name + '/' +self.name
        sql_str = ''' insert into frames_index(frame_id,frame_name,frame_path,frame_type,tags,image_data_ls,avg_pore,threshold,scale_v)
                        VALUES(?,?,?,?,?,?,?,?,?)'''
        conn.execute(sql_str,(self.id,
                              self.name,
                              out_path,
                              int(self.type),
                              str(self.tags),
                              array(self.image_ref_ls),
                              int(self.avg_pore),
                              int(self.constants["thresh"]),
                              str(self.constants["scale"])
                              ))
        conn.commit()
        conn.close()
        print("image data pushed to database")
    def process_frame(self):
        """ creates instances ImageData objects for all 
        images and adds them so self.image_data_ls
        """
        i =0
        for img in self.image_paths:
            self.process_image(img)
            i = i + 1
            

    def process_image(self,img):
        """ creates new ImageData objects and appends"""
        print("starting image processing of file with path:",img)
        new_image = ImageData(
            jname=self.job_name,
            frame = self.name,
            path = img,
            const = self.constants, 
            db_ref = self.db_ref,
            )
        self.image_data_ls.append(new_image)
        self.image_ref_ls.append(new_image.im_id)




    
