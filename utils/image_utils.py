from skimage.draw import set_color
from skimage.io import imsave
from skimage.draw import circle,circle_perimeter
def color_out_image(regions,image):

    for reg in regions:
        temp_set = {(1,0)}
        for pt in reg.coords:
            x = pt[1]
            y = pt[0]
            #z = pt[2]
            temp_set.add((x,y))
            set_color(image, (y,x), color =(161, 239, 16))
    return image

def color_out_image_large_area(region,image):
        #ut = image
        for pt in region.coords:
            x=pt[1]
            y=pt[0]
            #z=pt[2]
            set_color(image, (y, x), color=(255, 1, 1))
        return image

def color_out_largest(region_ls, image):
    for region in region_ls:
        image = color_out_image_large_area(region, image)
    return image


def color_out_set(coord_set, image):
    #out_image = image
    #print("co[0]", coord_set[0])
    set_color(image, (coord_set[1],coord_set[0]), color=(0, 77, 253))
    return image


def color_circle(c,r,image):
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r)
    set_color(image, (y_ls,x_ls), color=(0, 77, 253))
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r-1)
    set_color(image, (y_ls, x_ls), color=(0, 77, 253))
    x_ls,y_ls = circle_perimeter(int(c[0]),int(c[1]),r-2)
    set_color(image, (y_ls, x_ls), color=(0, 77, 253))


def color_holes(hole_ls, image):
    #print(len(hole_ls))
    for hole in hole_ls:
        color_circle(hole[4],hole[5],image)
    return image

def save_out_image(image,out_path):
    save_name = '.' + out_path + ".png"
    imsave(save_name,image)
    print("saved image at",save_name)
    # io.imsave("." + self.image_out_path + "/" + self.name[:-4] + "_out.png", self.out_image)
