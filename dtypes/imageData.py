#import pandas as pd
from skimage.measure import label, regionprops
import cv2
from cv2 import resize
import uuid
from utils import image_utils, area_utils
from dtypes.db_helper import Db_helper
from skimage import io
import os
class ImageData:
    def __init__(self,jname,frame,path,const, db_ref,):
        #create unique identifier for imagedata object in db
        self.im_id = str(uuid.uuid4()).replace('-','') + "_" + frame
        #this should be the root path for output of data/images

        #this should strickty be the name of the image(no delimeters)
        self.name = os.path.basename(os.path.normpath(path))
        self.image_out_path = "/job-data/" + jname + "/" + frame + '/' + self.name[:-4] + "_out"
        #opens the image and stores the image data `as a np array
        self.img_path = path
        #unique identifier for the image
        self.frame_id = frame
        #value that indicates the sensitytiy of the thresholding
        self.threshold = const["thresh"]
        #factor to convert the images size to microns
        self.scale_factor = const["scale"]
        #size of pore to alert on or show in red
        self.danger_size = const['warn_size']
        #pore size to ignore IMPORTANT
        self.ignore_size = const['min_ignore']
        #scale image
        self.image_handle = None
        self.filtered_image = None
        self.out_image = None
        self.porosity = 0
        self.largest_areas = []
        self.largest_regions = []
        self.largest_holes = None
        self.all_areas = []
        self.coords = []
        self.histogram = None
        #this should be opened(no need to open or close)
        self.db_ref = db_ref
        self.compute_image(path,const)


    #def __repr__ (self):
    #    return "porosity: " + str(self.porosity) + " \n scale factor: " + str(self.scale_factor)  +" \n image path: " + self.image_path



    def compute_image(self,path,const):
        print("start compute...")
        max = 1
        max_pts = []
        pts = []
        image_data = io.imread(path)
        image=resize(image_data, dsize =(800,600), interpolation = cv2.INTER_CUBIC)
        #image = area_utils.adjust_exposure(image)
        img_seg = area_utils.get_thresh_image(image, const["thresh"])
        #calculate porosity
        self.porosity = area_utils.get_porosity(img_seg)
        label_image = label(img_seg)
        regions = regionprops(label_image)
        self.out_image = image_utils.color_out_image(regions, image)
        self.all_areas = area_utils.get_all_areas(regions)
        self.largest_areas,self.largest_regions, = area_utils.get_largest_areas(regions, self)
        self.out_image = image_utils.color_out_largest(self.largest_regions, self.out_image)
        #self.largest_holes,largest_holes_area = area_utils.get_largest_holes(l)
        #self.histogram = area_utils.get_histogram(self.all_areas)
        #self.out_image = image_utils.color_out_set(max_pts, self.out_image)
        self.out_image = image_utils.color_holes(self.largest_areas, self.out_image)
        image_utils.save_out_image(self.out_image, self.image_out_path)
        db = Db_helper()
        db.post_img_to_db(self)
