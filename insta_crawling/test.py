from urllib import request

image_url = "https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-19/s150x150/89683032_189456909017882_3650198370208710656_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_ohc=awT5vaJwND4AX-LQ8LD&oh=330ed45ab64523e431968af9048c08d9&oe=5ECF1D8B"
image_file_name = "test"
request.urlretrieve(str(image_url), "/home/user/insta_crawler/wearly-crawler/images/" +image_file_name+ ".jpg")
