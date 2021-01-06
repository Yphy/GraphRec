def hashTag_data():

    import csv
    import sys
    sys.path.append("/home/user/insta_crawler")

    f = open('/home/user/insta_crawler/Prj_Wearly/resources/hashTag_list.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    hashtag_list = []
    for line in rdr:
        hashtag_list.extend(line)

    return hashtag_list
