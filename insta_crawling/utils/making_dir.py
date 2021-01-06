def mkdir_hashTag(hashTag, parent_path):
    import os
    if os.path.isdir(parent_path + '/'+ hashTag):
        pass
    else:
        os.mkdir(parent_path +'/'+ hashTag)
