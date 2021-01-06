def image_mapping(hashTag, image_show):
    """
   :param hashTag: a list of hashtags
   :param image_show: show image if true
   """

    import json
    from PIL import Image

    tags = []
    for tag in hashTag:
        checkTag = tag[0].find("#")
        if checkTag != -1:
            tag = tag.replace("#", "")
            tags.append(tag)
        else:
            tags.append(tag)

    print('tags', tags)

    for tag in tags:
        # with open(r"instagram_" + tag + ".json", "r", encoding='UTF-8-sig') as read_file:
        with open("../resources/crawling_data/instagram_#%s" %(tag) + ".json", "r", encoding='UTF-8-sig') as read_file:
            data = json.load(read_file)

        print('the number of %s data' %(tag),len(data))

        for i in data:
            keys = i['key']
            for index, value in enumerate(keys):
                key = value + '.jpg'
                # print('key: ', key)
                im = Image.open('../image/%s' %(tag) + '/' + key)  # 이미지 불러오기
                if image_show == True:
                    print(key, "이미지에 해당하는 정보", i)
                    # 이미지 보여주기
                    im.show()
                else:
                    # print(key, "이미지에 해당하는 정보", i)
                    print('key가 잘못 설정되었습니다.')


# def image_mapping(hashTag, image_show):
#      """
#     :param hashTag: a list of hashtags
#     :param image_show: show image if true    
#     """
#     import json
#     from PIL import Image
        
#     tags = []
#     for i, tag in enumerate(hashTag):
#         checkTag = tag[i].find('#')
#         if checkTag==-1:
#             tag = '#'+tag
#             tags.append(tag)
#     print(tags)

#     for tag in tags:
#         with open(r"instagram_"+ tag + ".json", "r",encoding='UTF-8-sig') as read_file:
#             data = json.load(read_file)

#         for i in data:
#             key=i['key']
#             key= key + '.jpg'

#             im = Image.open('../image/'+key)  # 이미지 불러오기

#             if image_show == True:
#                 print(key,"이미지에 해당하는 정보",i)
#                 im.show()  # 이미지 보여주기

#             else:
#                 print(key, "이미지에 해당하는 정보", i)
