


# 1 dim to 3 dims conversions

# def gray2color(data, color):
#     # color: rgb tuple
    
#      data = 100, color = (128, 128, 0)
     
     
#      => (100/255  *128, 100/255*128, 0)
    
    
#     ...
    
    
def merge_channels(data, colors: list):
    # colors = list of tuples(r, g, b)
    # should be able to combine an arbirary number of color channels into a single rgb image
    ...


# 3 dims => 3 dims conversions

# cv2.cvtColor

def rgb2hsv(r, g, b):
    rp = r/255
    gp = g/255
    bp = b/255
    
    v = max(rp, gp, bp)
    delta = v - min(rp, gp, bp)
    
    # hue calculation
    if delta == 0:  h = 0
    elif v == rp:   h = 60 * ((gp - bp)/delta % 6)
    elif v == gp:   h = 60 * ((bp - rp)/delta + 2)
    elif v == bp:   h = 60 * ((rp - gp)/delta + 4)
        
    # saturation calculation
    if v == 0:  s = 0
    else:       s = delta / v
    
    return h, s, v
    


def hsv2rgb(): ...


# def 


q = rgb2hsv(128, 128, 0)

print(q)