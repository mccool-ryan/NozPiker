
# function to sort projected images into dictionary as arrays
def GetImageSet(mrc,name,store):
    from mrcfile import open
    with open(mrc,'r') as m:
        data = []
        for i in range(m.data.shape[0]):
            data.append(m.data[i,:,:])
    size = len(data[-1][:,0])
    store[name] = data
    return size

# function to create training data
def CreateTrainingData(store, size):
    from numpy import array, where, zeros, min, max, resize, transpose
    from tensorflow.image import resize_with_crop_or_pad
    # Get Dict keys
    class_names = array(sorted(store.keys()))
    # Pre-allocate arrays
    key = class_names[0]
    length = len(store[key])
    shape = (size,size)
    train_images = zeros((length,shape[0],shape[1]))
    train_labels = zeros(length)
    # Load images and labels
    for key in class_names:
        loc = where(class_names == key)[0]
        # Add images
        if store[key][1].shape[1] < size:
            for i in range(len(store[key])):
                array = (store[key][i] - min(store[key][i]))/(max(store[key][i]) - min(store[key][i]))
                array = resize(array,(array.shape[0],array.shape[1],1))
                array = resize_with_crop_or_pad(array,size,size)
                array = np.transpose(array,(2,0,1))
                train_images[(loc*length)+i,:,:] = array
                train_labels[(loc*length)+i] = loc
    return train_images, train_labels, class_names