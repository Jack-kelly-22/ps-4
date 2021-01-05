import sqlite3
from numpy import ndarray, array,asarray
from utils import sql_utils
from pandas import DataFrame
import numpy as np
class Db_helper:
    def __init__(self):
        sqlite3.register_adapter(ndarray, sql_utils.adapt_array)
        sqlite3.register_converter("array", sql_utils.convert_array)

        #self.cur = self.conn.cursor()

    def fetch_image(self,img_id):
        sqlite3.register_adapter(ndarray, sql_utils.adapt_array)
        sqlite3.register_converter("array", sql_utils.convert_array)
        conn = sqlite3.connect(
            "/Users/jackkelly/PycharmProjects/win_break/dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        conn = sqlite3.connect(i)
        img_id = str(img_id)
        #img_id = str('27e01e03ae7b4d979519a3dbed79ab2d_frame_ 0')
        print("starting fetch img with type:",type(img_id),"img id:", img_id)
        im_dat = sql_utils.empty_img_dic()
        sql_str = sql_utils.get_img_fetch_str()
        cur = conn.execute(sql_str,(img_id,))

        for row in cur:
            im_dat["img_id"] = str(row[0])
            im_dat["img_name"] = str(row[1])
            im_dat["img_path"] = sql_utils.fix_path(row[2])
            im_dat["pores"] = row[3]
            im_dat["img_largest_areas"] = array(row[4])
            # im_dat["all_areas"] = row[5]
            im_dat["largest_holes"] = row[6]
            print("so:",type(row[6]))

            #print("ls type", type(row[4]))
            # fix this later ^^^^!!!
        conn.commit()
        conn.close()
        print("fin:,",im_dat)
        return im_dat

    def fetch_frame(self,frame_id):
        conn = sqlite3.connect(
            "/Users/jackkelly/PycharmProjects/win_break/dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        f_dat = sql_utils.empty_frame_dic()
        sql_str = sql_utils.get_frame_fetch_str()
        cur = conn.execute(sql_str, (frame_id,))
        for row in cur:
            f_dat["frame_id"] = str(row[0])
            f_dat["frame_name"] = str(row[1])
            f_dat["frame_path"] = str(row[2])
            f_dat["frame_type"] = str(row[3])
            f_dat["tags"] = row[4]
            for img in row[5]:
                f_dat["image_data_ls"].append(self.fetch_image(img))
            f_dat["avg_pore"] = row[6]
            f_dat["thresh"] = int(row[7])
            f_dat["scale"] = str(row[8])
        conn.close()
        return f_dat

    def fetch_job(self,job_id):
        sqlite3.register_adapter(ndarray, sql_utils.adapt_array)
        sqlite3.register_converter("array", sql_utils.convert_array)
        conn = sqlite3.connect(
            "/Users/jackkelly/PycharmProjects/win_break/dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        j_dat = sql_utils.empty_job_dic()
        sql_str = sql_utils.get_job_fetch_str()
        cur = conn.execute(sql_str, (job_id,))

        for row in cur:
            j_dat["job_id"] = row[0]
            j_dat["job_name"] = str(row[1])
            j_dat["job_path"] = str(row[2])
            j_dat["job_type"] = str(row[3])
            j_dat["tags"] = j_dat["tags"] + list(row[4])
            print("types:", type(row[5]))
            print("tyes:", type(row[5][0]))
            for frame in row[5]:
                print("trying to fetch frame with :", frame)
                j_dat["frame_data_ls"].append(self.fetch_frame(frame))
        conn.close()
        return j_dat

    def fetch_jobs(self, n = 100):
        sqlite3.register_adapter(ndarray, sql_utils.adapt_array)
        sqlite3.register_converter("array", sql_utils.convert_array)
        conn = sqlite3.connect(
            "/Users/jackkelly/PycharmProjects/win_break/dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        job_ls = []
        sql_str = sql_utils.get_jobs_fetch_str()
        cur = conn.execute(sql_str)
        for row in cur:
            j_dat = sql_utils.empty_job_dic()
            j_dat["job_id"] = row[0]
            j_dat["job_name"] = str(row[1])
            j_dat["job_path"] = row[2]
            j_dat["job_type"] = row[3]
            j_dat["tags"] = row[4]
            for frame in row[5]:
                j_dat["frame_data_ls"].append(str(frame))
            if len(row)>8:
                j_dat["job_date"]= row[6]
                j_dat["num_frames"] = row[7]
                j_dat["num_images"] = row[8]
            else:
                j_dat["job_date"] = "24h ago"
                j_dat["num_frames"] = '1'
                j_dat["num_images"] = '1'


            job_ls.append(j_dat)
        conn.close()
        return job_ls


    def post_img_to_db(self,img):
        sqlite3.register_adapter(ndarray, sql_utils.adapt_array)
        sqlite3.register_converter("array", sql_utils.convert_array)
        conn = sqlite3.connect(
            "/Users/jackkelly/PycharmProjects/win_break/dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        sql_str = sql_utils.get_img_post_str()
        conn.execute(sql_str, (img.im_id,
                                    img.name,
                                    '.'+ img.image_out_path +'.png',
                                    img.porosity,
                                    array(img.largest_areas),
                                    array(img.all_areas),
                                    array(img.largest_holes)
                                    #asarray(img.largest_holes)
                                    #img.histogram.to_sql()
                                    ))
        conn.commit()
        print("image data post...")
        conn.close()


#db = Db_helper()

