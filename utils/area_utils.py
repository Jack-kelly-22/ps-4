from numpy import percentile
from skimage import exposure
from skimage.color import rgb2gray
from numpy import uint8
from porespy.metrics import porosity
from utils import coord_utils
from skimage.draw import circle
from utils.filters_utils import scalar_transform
from pandas import DataFrame


def adjust_exposure(image,lower = 1, high = 99):
    p2,p98 = percentile(image,(lower,high))
    return exposure.rescale_intensity(image, in_range = (p2,p98))


def get_all_areas(regions):
    """"""
    areas = []
    for region in regions:
        area = region["area"]
        areas.append(area)
    #print("about to retrun areas: ", areas[:10])
    return areas

def get_real_area(region):
    area_set = {(1, 0)}
    #print("region area:", str(region.area))
    for pt in region.coords:
        x = pt[1]
        y = pt[0]
        #z = pt[2]
        area_set.add((x, y))
    print("returned area = ", len(area_set))
    return len(area_set) - 1

def get_porosity(img_seg):
    pore = porosity(img_seg)
    return pore

def get_largest_areas(regions,image_data):
    # dataframe = ps.metrics.props_to_DataFrame(regions)
    largest_pores = []
    #largest_pores_coords =[]
    print("gonna sort ",len(regions))
    regions.sort(key=lambda regions: regions["area"])
    largest_reg = []

    regions = regions[-3:]
    regions.reverse()
    for region in regions:
        #y, x, y = region["centroid"]
        y, x,z = region["centroid"]
        print("centroid",x,y,z)
        # print("len cords", len(region["coords"]))
        coords = region["coords"]
        coords = coord_utils.remove_z_set(coords)
        #validate_area(region)
        center,r = get_largest_circle_in_region(coords)
        center = (center[0]* image_data.scale_factor, center[1] * image_data.scale_factor )
        largest_pores.append(
            [image_data.name,
             int(get_real_area(region) * (image_data.scale_factor * image_data.scale_factor)),
             (x // 1),
             (y // 1),
             center,
             r
             ])



    # self.try_circle(largest_pores[0][4],(238,394))
    return largest_pores,regions

def get_thresh_image(image, threshold):
    #print(image)
    #image = rgb2gray(image)
    #thresh_arr = scalar_transform(threshold,image)
    #print("thresh arr",thresh_arr)
    """i =0
    while i<50:
        image[i,:] = multiply(image[i,:], 1.3)
        i= i+ 1
    i =560
    while i < 600:
        image[i, :] = multiply(image[i,:], 0.7)
        i = i + 1"""
    #image = image * 1.9
    #img_seg = (image > threshold).astype(uint8)
    #img_seg = (image > 1).astype(uint8)
    img_seg = (image > threshold).astype(uint8)
    window_size = 25
    #thres = threshold_sauvola(image,window_size = window_size,k =0.03, r=47)
    #print("calculated thresh:", thres)
    #img_seg = (image > thres).astype(uint8)
    return img_seg

def try_circle(coords, middle,size):
    go = True
    i = size
    area_pts = set()
    ls_x,ls_y = [],[]

    while go:
        ls_x,ls_y = circle(middle[0],middle[1],i)
        j = 0
        pt = (0,0)
        while j < len(ls_x) and go:
            if go:
                pt = (ls_x[j],ls_y[j])
                if(coord_utils.check_pt(pt, middle, area_pts, coords)):
                    area_pts.add(pt)
                else:
                    go = False
            j= j + 1
        i = i + 1
    return i-1,(middle[0],middle[1])


def get_largest_circle_in_region(coords):
    """ calculates the largest circle that will fit in the
    retion defined by reg_tup
    Parameters:
        reg_tup(tuple): details about pore
    Returns:
        tup: (center,radius,points"""
    max = 1
    max_pts = []
    pts = []
    center = [0,0]
    reg_coords = coords
    #print("starting et largest ", reg_coords)
    n = 0
    for pt in reg_coords:
        n,pts = try_circle(reg_coords, pt, max)
        if (n > max):
            max = n
            max_pts = pts
            center = pt
    print("MAX:", max)
    return center,max,

def get_largest_holes(largest_areas):
    largest_holes = []
    largest_holes_areas =[]
    for large_area in largest_areas:
        mid,r,pts, = get_largest_circle_in_region(large_area)
        largest_holes.append([mid,r])
        largest_holes_areas.append([mid,r,pts])
    return largest_holes,largest_holes_areas

def validate_area(region):
    print("area: ", region["area"])
    print(" filled area: ", region["filled_area"])
    print("ratio :", float(region["area"])/float(region["filled_area"]))
    

def get_histogram(all_areas):
    # create the bins
    df = DataFrame(all_areas, columns=["Area"])
    hist = df.hist(column="Area")
    return hist



