import os, sys
import h5py
import numpy as np
import pandas as pd

def stitch(dir_, filename='', output_file_base=""):

    files = os.listdir(dir_)
    pixel_map_files = [x for x in files if ("pixel" in x)]
    object_map_files = [x for x in files if ("Object" in x)]
    
    if len(pixel_map_files) > 0:
        do_pixel = True
    else: do_pixel = False

    print(object_map_files)
    if len(object_map_files) > 0:
        do_object = True
    else: do_object = False
    print(do_pixel)
    xstart = []
    xend = []
    ystart = []
    yend = []
    
    if do_pixel:
        interval_file_list = pixel_map_files
    else:
        interval_file_list = object_map_files

    for f in interval_file_list:
        _, xs, xe, ys, ye, *_ = f[:-3].split("_")
        xstart.append(int(xs))
        xend.append(int(xe))
        ystart.append(int(ys))
        yend.append(int(ye))

    xstart = np.array(sorted(list(set(xstart))))
    xend = np.array(sorted(list(set(xend))))
    ystart = np.array(sorted(list(set(ystart))))
    yend = np.array(sorted(list(set(yend))))

    # load in first file to get number of channels
    
    if not do_pixel:

        first_file = h5py.File(os.path.join(dir_, object_map_files[0]),'r')
        data = first_file['exported_data']

    else:

        first_file = h5py.File(os.path.join(dir_, pixel_map_files[0]),'r')
        data = first_file['exported_data']

    if len(data.shape) == 3:
        x,y,c=data.shape
        offset = 0
    elif len(data.shape) == 5:
        _,_,x,y,c = data.shape
        offset = 2
    big_pixel_file = np.zeros((int(np.max(xend)), int(np.max(yend)), c), dtype=np.uint8)
    big_object_file = big_pixel_file[:,:,0].copy()

    xt = (xend[0]-xstart[1])/2
    yt = (yend[0]-ystart[1])/2

    xdiv = np.hstack(([0], xend-xt))
    xdiv[-1] = max(xend)
    ydiv = np.hstack(([0], yend-yt))
    ydiv[-1] = max(yend)
    xbound=[0,0]
    ybound=[0,0]
    last_object_id = 0
    
    print("Stitching...")

    for i in np.arange(len(xstart)):
        for j in np.arange(len(ystart)):
            rs = int(xstart[i])
            re = int(xend[i])
            cs = int(ystart[j])
            ce = int(yend[j])

            pixelpath = os.path.join(dir_, "_".join(["tmp", str(rs), str(re), str(cs), str(ce), "pixel_probabilities"]) + ".h5")
            objectpath = os.path.join(dir_, "_".join(["tmp", str(rs), str(re), str(cs), str(ce), "Object_Prediction"]) + ".h5")

            if do_pixel:
                pixel_file = h5py.File(pixelpath, 'r')
                pixel_data = pixel_file['exported_data']
                xe = pixel_data.shape[0+offset]
                ye = pixel_data.shape[1+offset]
            if do_object:
                object_file = h5py.File(objectpath,'r')
                object_data = object_file['exported_data']
                xe = object_data.shape[0+offset]
                ye = object_data.shape[1+offset]

            if i == 0:
                xs = 0
                xbound[0]=-1
            else:
                xs = int(xt)
                xbound[0] = xs

            if i == len(xstart)-1:
                xe = int(xe)
                xbound[1] = xe
            else:
                xe = int(xe - xt)
                xbound[1] = xe

            if j == 0:
                ys = 0
                ybound[0]=-1
            else:
                ys = int(yt)
                ybound[0] = ys

            if j == len(ystart)-1:
                ye = int(ye)
                ybound[1] = ye
            else:
                ye = int(ye - yt)
                ybound[1] = ye
            
            if do_pixel:
                if len(pixel_data.shape) == 3:
                    big_pixel_file[int(xdiv[i]):int(xdiv[i+1]), int(ydiv[j]):int(ydiv[j+1]), :] = pixel_data[xs:xe, ys:ye, :]
                if len(pixel_data.shape) == 5:
                    big_pixel_file[int(xdiv[i]):int(xdiv[i+1]), int(ydiv[j]):int(ydiv[j+1]), :] = pixel_data[0,0,xs:xe, ys:ye, :]

            if do_object:
                if len(object_data.shape) == 3:
                    big_object_file[int(xdiv[i]):int(xdiv[i+1]), int(ydiv[j]):int(ydiv[j+1])] = object_data[xs:xe, ys:ye, 0]
                if len(object_data.shape) == 5:
                    big_object_file[int(xdiv[i]):int(xdiv[i+1]), int(ydiv[j]):int(ydiv[j+1])] = object_data[0,0,xs:xe, ys:ye, 0]
                
                df = pd.read_csv(os.path.join(dir_, "_".join(["object_feature_output-tmp",str(rs),str(re),str(cs),str(ce),"table.csv"])))

                filtered = df[( df['Center of the object_1'] > xbound[0] ) &
                    ( df['Center of the object_1'] <= xbound[1] ) &
                    ( df['Center of the object_0'] > ybound[0] ) &
                    ( df['Center of the object_0'] <= ybound[1] )]

                if i == 0:
                    filtered['Center of the object_1'] += xdiv[i]
                    filtered['Bounding Box Minimum_1'] += xdiv[i]
                    filtered['Bounding Box Maximum_1'] += xdiv[i]
                else:
                    filtered['Center of the object_1'] += xdiv[i]-xt
                    filtered['Bounding Box Minimum_1'] += xdiv[i]-xt
                    filtered['Bounding Box Maximum_1'] += xdiv[i]-xt
                if j == 0:
                    filtered['Center of the object_0'] += ydiv[j]
                    filtered['Bounding Box Minimum_0'] += ydiv[j]
                    filtered['Bounding Box Maximum_0'] += ydiv[j]
                else:
                    filtered['Center of the object_0'] += ydiv[j]-yt
                    filtered['Bounding Box Minimum_0'] += ydiv[j]-yt
                    filtered['Bounding Box Maximum_0'] += ydiv[j]-yt
                if (i == 0) and (j == 0):
                    big_data_frame = filtered
                else:
                    try:
                        filtered['object_id'] += last_object_id
                        big_data_frame = big_data_frame.append(filtered, ignore_index=True)
                    except KeyError:
                        pass
                
                try:
                    object_id_list = filtered['object_id']
                    if len(object_id_list) > 0:
                        last_object_id = max(filtered['object_id'])
                except KeyError:
                    pass
               
    
    if do_pixel:
        with h5py.File(os.path.join(dir_, "_".join(["full",filename,output_file_base,"pixel_probabilities.h5"])), "w") as out:
            dset = out.create_dataset("data", data=big_pixel_file)
    if do_object:
        with h5py.File(os.path.join(dir_, "_".join(["full",filename,output_file_base,"object_predictions.h5"])), "w") as out:
            dset = out.create_dataset("data", data=big_object_file)

        big_data_frame.to_csv(os.path.join(dir_, "_".join(["full",filename,output_file_base,"object_feature_output.csv"])))

