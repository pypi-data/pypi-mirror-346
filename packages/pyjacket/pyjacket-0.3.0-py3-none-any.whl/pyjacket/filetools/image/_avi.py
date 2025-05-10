import cv2
import numpy as np
import pims

# def read(filepath):
#     cap = cv2.VideoCapture(filepath)
#     ret, frame = cap.read()  
#     t = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     ret, frame = cap.read()
#     y, x, c = frame.shape
#     result = np.empty((t, y, x, c), frame.dtype)
#     for i in range(t):
#         ret, frame = cap.read()
#         if not ret:  break
#         result[i] = frame
#     return result

def read(filepath):
    print('reading img data, this can take a while...')
    return np.array(pims.open(filepath))

# def read_frame(cap, idx):
#     cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
#     ret, frame = cap.read()
#     if not ret:
#         raise ValueError("Error: Could not read frame.")
#     return frame


def write(filepath, data, fps=30):
    """_summary_

    Args:
        filepath (_type_): _description_
        data (np.ndarray | ImageHandle): _description_
        fps (int, optional): _description_. Defaults to 30.
    """
    
    frames, height, width, *channels = data.shape
    
    # Handle color or grayscale
    if not channels:
        isColor = False
    elif len(channels) == 1 and channels[0]==3:
        isColor = True
    else:
        raise ValueError(f"Cannot interpret data of shape {data.shape}")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=isColor)
    for frame in data:
        out.write(frame)

    out.release()
    return

if __name__ == '__main__':
    import numpy as np
    # Create a sample 3D NumPy array (e.g., 100 frames of 256x256 grayscale images)
    frames = 100
    height = 256
    width = 256
    video_data = np.random.randint(0, 256, (frames, height, width), dtype=np.uint8)
    write('output_video.avi', video_data)
