def insTag_crawling(hashTag,data_num):
    """

    :param hashTag: a list of hsahtags
    :param data_num: the number of cralwing data
    :return: a json file with image, hashtags,text and data
    """
    import sys
    sys.path.append("/home/user/insta_crawler")

    from Prj_Wearly.utils.image_crawling import image_crawling
    from Prj_Wearly.utils.text_crawling import text_crawling
    from Prj_Wearly.utils.hash_crawling import hash_crawling
    from Prj_Wearly.utils.date_post import date_post
    from Prj_Wearly.utils.like_num import like_num
    from Prj_Wearly.utils.comments_crawling import comments_crawling
    from Prj_Wearly.utils.making_dir import mkdir_hashTag
    from Prj_Wearly.utils.user_id_num import user_id_num
    from Prj_Wearly.utils.like_log import like_log
    from Prj_Wearly.utils.comment_num import comment_num
    from Prj_Wearly.utils.tagged_id import tagged_id

    from selenium import webdriver
    import json
    import time
    from datetime import datetime
    from collections import OrderedDict
    from selenium.webdriver.common.keys import Keys
    from urllib import request
    import os
    import pymysql

    # Connecting to server DB
#    conn = pymysql.connect(host='121.138.155.10', port = 33060 ,user='remote', password='!@#qweasdzxc', db='prj_wearly', charset='utf8')

    conn = pymysql.connect(host='localhost', port = 3306, user='root', password='!@#qweasdzxc', db='prj_wearly', charset='utf8', connect_timeout=24)
    cursor = conn.cursor()

    # [ HASHTAG USING CHECK ] #
    tags = []
    for tag in hashTag:
        checkTag = tag[0].find("#")
        if checkTag != -1:
            tag = tag.replace("#","")
            tags.append(tag)
        else:
            tags.append(tag)

    print('tag', tags)
  

    # path = '/home/user/insta_craw'
    path = '/home/user/insta_crawler/Prj_Wearly/chromedriver'
    # driver = webdriver.Chrome(path)

    ## setting path for making hashTag folder
    os.path.abspath(os.curdir)
    os.chdir("..")
    parent_path =  '/home/user/images'
    #parent_path = '/home/user/insta_crawler/Prj_Wearly/image'

    for tag in tags:
                
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')  
          
        driver =  webdriver.Chrome(path, chrome_options=chrome_options)
        
        print('Used tag:',tag)
       
        mkdir_hashTag(tag,parent_path=parent_path)
	
        driver.get("https://www.instagram.com/explore/tags/"+str(tag))
#	time.sleep(1.0)
	
        links= []
        while len(set(links))<data_num:
            no_of_pagedowns = 2
            elem = driver.find_element_by_tag_name("body")
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(1.0)
                no_of_pagedowns -= 1

            elems = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
            for ele in elems:
                link = ele.get_attribute("href")
                try:
                    if link in links:
                        continue
                    else:
                        links.append(link)
                except:
                    continue

        print('the number of objects:',len(set(links)))

        print('Start crawling')
        if comment_num(driver, link):
            ## a list of number_of_comment key-link, value - num_of_comment
            number_of_comments=[]
            for idx, link in enumerate(links):
                number_of_comments.append(comment_num(driver, link))

            ## Only crawling instagram data from May to August
            start_str = "2019-05-01 00:00:00"
            # may = datetime.strptime(start_str, "%Y-%m-%d %H:%M").date()
            may = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            #end_str = "2019-08-31 23:59:59"
            # august = datetime.strptime(end_str, "%Y-%m-%d %H:%M").date()
            #august = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

            all_data = []

            for idx, link in enumerate(links):
		#pre_post_id = link[28:-1]		

                try:
                    datetime_post = date_post(driver, link)
                    print('date_post is',datetime_post)

		    
		   #if may < deatetime_post < august and 
                    if may < datetime_post:
                        print()
                        print("crawling ")
                        print('%s_idx:' %(tag),idx,'\n',link)

                        post_data = OrderedDict()


                        ## 1_Saving the used hashtag
                        post_data["hashtag_crawl"] = tag
                        # # inser into table(filed 1, field 2, ...) values(value 1, value 2, ...)
                        # # cursor.execute('''insert into post_test(hashtag_crawl) values(%s) ''',tag)


                        ## 2_datetime of starting carwling
                        now = datetime.now()
                        now_ = now.strftime('%Y-%m-%d %H:%M:%S')
                        # now_datetime = datetime.strptime(now_, '%Y-%m-%d %H:%M').date()
                        now_datetime = datetime.strptime(now_, '%Y-%m-%d %H:%M:%S')
                        post_data["date_crawl"] = now_datetime
                        # cursor.execute('''insert into post_test(date_crewl) values(%s) ''', now_datetime)
                        print('date_crawl:', now_datetime)

                        ## 2.5 comments_num
                        for key, comment_number in number_of_comments[idx].items():
                            if key == link[25:]:
                                print('comments_num', int(comment_number))
                                # comment_num = value
                                # cursor.execute('''insert into post_test(comment_num) values(%i) ''', comment_num)
                                post_data['comments_num'] = int(comment_number)

                        ## 3_URL of post
                        driver.get(link)
                        post_id = link[28:-1]
                        post_data["post_id"] = post_id
                        # if link[27] == '/':
                        #     print('link:', link[28:-1])
                        # cursor.execute('''insert into post_test(post_id) values(%s)''', link[28:-1])

                        ## 4_Owner_Id
                        user_id_, user_num = user_id_num(driver)
                        print("user_num:", user_num)
                        # cursor.execute('''insert into post_test(user_num) values(%i)''', user_num)

                        post_data['user_num'] = user_num

                        ## 5_image crawling
                        try:
                            images = image_crawling(driver, link)
                            print('num_of_images:', len(images))
                            print('images',images)
                            post_data["image_address"] = images
                            # file_data["image_url"] = images

                            for index, image_url in enumerate(images):
                                image_num = index
                                image_file_name = tag + '_' + post_id + '_' + str(index)
                                request.urlretrieve(str(image_url), "/home/user/images/%s" % (tag) + '/' + tag + '_' + post_id + '_' + str(index) + ".jpg")
				#request.urlretrieve(str(image_url), "/home/user/images/%s" % (tag) + '/' + tag + '_' + post_id + '_' + str(index) + ".jpg")

                                # Image_Table
                                cursor.execute('''insert into image(image_num, post_id, image_file_name, image_url) values (%s, %s, %s, %s)''',
                                               (image_num, post_id, image_file_name, image_url))
                                conn.commit()
                                print("Commit image tables")

                                key = tag + '_' + post_id
                            post_data['key'] = key

                            print('이미지 저장')
                        except:
                            images = None

                        ## 6_text crawling
                        text = text_crawling(driver, user_id_)
                        post_data["text"]=text
                        print('text',"\n",text)

                        ## 6.5_tagged_id
                        tagging_id = tagged_id(driver)
                        post_data["tagged_id"] = tagging_id
                        print('tagging_id', "\n", tagging_id)

                        ## 7_hashtag crawling
                        hashText = hash_crawling(driver)
                        post_data["hashtags"] = hashText
                        print('hashtags', hashText)

                        # ## 8_date crawling
                        post_data["date_post"] = datetime_post
                        # cursor.execute('''insert into post_test(date_post) values(%s) ''', datetime_post)

                        print('datetime_post:', datetime_post)

                        ## 9_ like_num
                        num_like = like_num(driver)
                        post_data["like_num"] = num_like
                        # cursor.execute('''insert into post_test(like_num) values(%i) ''', num_heart)

                        print('num_heart:', num_like)

                        # ## 10_ comments and comment_log
                        comment_log = comments_crawling(driver)
                        post_data["comment_log"] = comment_log
                        print('comment_log:',comment_log)

                        ## 11_like_log
                        like_logs = like_log(driver)
                        post_data['like_log'] = like_logs
                        print('like_log',like_logs)

                        ## 12_ commnet_log_num
                        comment_log_num = [int(comment_number), now.strftime('%Y-%m-%d %H:%M:%S')]
                        # now_datetime = datetime.strptime(now_, '%Y-%m-%d %H:%M:%S')
                        print('comment_log_num',comment_log_num)

                        # SQL
                        # Post_Table
                        print('Inserting data into DB')

                        conn.ping(reconnect=True)

                        cursor.execute('''
                        insert into post
                        
                        (post_id, user_num, hashtag_crawl, date_post, date_crawl, image, text, hashtags, tagged_id, like_num, comment_num, like_log, comment_log, comment_log_num)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                       (post_id, user_num, tag, datetime_post, now_datetime, json.dumps(images),  json.dumps(text), json.dumps(hashText), json.dumps(tagging_id), num_like, int(comment_number), json.dumps(like_logs), json.dumps(comment_log), json.dumps(comment_log_num))
                                       )

                        conn.commit()
                        print('Commit data into DB')
                        all_data.append(post_data)

                    else:
                        print("The post is out of month")

                except:
                    continue

            driver.close()

        else:
            continue

        ## save all data as json file
        print('the number of cralwing data:', len(all_data))
        print(all_data)

        #with open('../resources/crawling_data/instagram_#%s.json' %(tag),'w',encoding='UTF-7-sig') as make_file:
         #   json.dump(all_data, make_file,ensure_ascii=False)
