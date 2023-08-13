import os
from PIL import Image, ImageTk

MIDNAME = "_f"
START_NUMBER = 0

def getBox(arr, frame_v_index=0, frame_h_index=0):
    w, h = int(arr[3]), int(arr[4])
    x, y = int(arr[1]) + w * frame_v_index, int(arr[2]) + h * frame_h_index
    return x, y, x + w, y + h

def saveCrop(img, title, box):
    path = os.path.join('./frames/' + title + '.png')
    try:
        cropped_img = img.crop(box)
        cropped_img.save(path)
        print('ok: ' + title)
    except Exception as e:
        print('fail: ' + title + ' -- ' + str(e))


def run(img, dat):
    img = Image.open(img).convert("RGBA")
    
    path = os.path.join(os.getcwd(), "frames")
    if not os.path.isdir(path):
        os.mkdir(path)

    a = open(dat, 'r')
    for line in a.readlines():
        arr = line.split()
        if len(arr) <= 3 or "#" in arr[0]:  # empty line
            pass
        elif len(arr) <= 7:
            num_of_frames = int(arr[5])
            num_ofh_frames = int(arr[6])
            for frameHIndex in range(0, num_ofh_frames):
                for frameIndex in range(0, num_of_frames):
                    saveCrop(img, arr[0] + MIDNAME + str(frameIndex) + str(frameHIndex+START_NUMBER),
                             getBox(arr, frameIndex, frameHIndex))
    a.close()
    print("Done")

if __name__ == "__main__": 
    run("iso_grass.png", "tile_set.dat")
