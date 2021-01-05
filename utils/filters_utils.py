from numpy import array,eye,zeros_like,multiply,dot
from skimage.color import rgb2gray
from numpy import full
from skimage import img_as_uint
def scalar_transform(thresh_val,image):

    thresh_val = thresh_val/255
    #print(img[0])
    eye_arr = eye(600,800, dtype=(float,3))
    ident = eye(800,800)
    thresh_arr = full((600,800),thresh_val)
    #ident = eye(600, 800)
    #thresh_arr = full((600, 800), thresh_val)
    scalar = 0.6
    i = 0
    j = 0
    while(i<150):
        ident[i,j]= scalar
        i = i + 1
        j = j+1
    i = 650
    j = 650
    while(i<800):
        ident[i,j] = scalar
        i = i + 1
        j = j+1
    thresh_arr = dot(thresh_arr,ident)
    print("shape:", thresh_arr.shape)
    return thresh_arr