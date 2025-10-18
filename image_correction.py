import matplotlib.pyplot as plt
from skimage import io, transform
import numpy as np

def get_conversion(n_dists:int,dist_measure:float):
    img = io.imread('Wedge grid.bmp')
    plt.imshow(img)
    pts = plt.ginput(n_dists*2) # do it more times to get a better baseline conversion
    plt.show()

    photo_px = 0
    for i in range(0,5,2):
        photo_px += np.sqrt( (pts[i][0] - pts[i+1][0])**2 + (pts[i][1] - pts[i+1][1])**2 )

    return dist_measure/(photo_px/n_dists) # units are mm/px

def fix_distortion(file):
    img = io.imread(file)
    plt.imshow(img)
    pts = plt.ginput(3) 

    width = np.abs(pts[0][0] - pts[1][0])
    height = np.abs(pts[1][1] - pts[2][1])

    width_px_noflow = np.load('w_px_base.npy')
    height_px_noflow = np.load('h_px_base.npy')

    pct_w_change = 1 + (width-width_px_noflow)/width_px_noflow
    pct_h_change = 1 + (height-height_px_noflow)/height_px_noflow

    rescaled_img = transform.rescale(img, (1/pct_h_change,1/pct_w_change,1), anti_aliasing=True)
    fig, ax = plt.subplots(1,3, figsize=(10,5))

    ax[0].imshow(img)
    ax[0].set_title('Unscaled')

    ax[1].imshow(rescaled_img)
    ax[1].set_title('Rescaled')
    
    ax[2].imshow(io.imread('Wedge grid.bmp'))
    ax[2].set_title('Windoff')

    plt.show()
    accept_image = bool(int(input("Accept rescaled image? Enter 0 for no, 1 for yes. ")))
    if accept_image == 0:
        return
    else:
        fname = str("rescaled_"+file)
        io.imsave(fname, (rescaled_img*255).astype('uint8'))
	np.save( str("height_distortion_"+file), pct_h_change )
	np.save( str("width_distortion_"+file) , pct_w_change )

if __name__ == "__main__":
    mm_p_px = np.load('mm_per_px.npy')

    ##### CHANGE THIS EVERYTIME YOU RUN TO BE THE NAME 
    ##### OF THE CURRENT IMAGE YOU ARE FIXING DISTORTION OF
    filename = "Mach 2 wedge schlieren_horizontal_0.bmp"
    ###################################################

    fix_distortion(filename)