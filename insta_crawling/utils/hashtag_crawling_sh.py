def insta_crawling(hashTag, username, password, data_num):
    """
    :param hashTag: a list of hashtags
    :param username: instagram ID
    :param password: instagram PW
    :param data_num: the number of cralwing data
    
    :return:a json file with image, hashtags, text and data
    """
    from selenium import webdriver
    import json
    import time
    from collections import OrderedDict
    from selenium.webdriver.common.keys import Keys
    import urllib.request

    # [ HASHTAG USING CHECK ] #

    tags = []
    for i, tag in enumerate(hashTag):
        checkTag = tag[i].find('#')
        if checkTag==-1:
            tag = '#'+tag
            tags.append(tag)
    print(tags)

    path = '../chromedriver.exe'
    driver = webdriver.Chrome(path)# Chromedriver PATH
    driver.get("https://www.instagram.com/accounts/login/")

    #username과 password element를 찾아서 변수명으로 설정
    try:
        element_id = driver.find_element_by_name("username")
        element_pw = driver.find_element_by_name("password")
    except:
        element_id = driver.find_element_by_class_name("_2hvTZ pexuQ zyHYP")[0]
        element_pw = driver.find_element_by_class_name("_2hvTZ pexuQ zyHYP")[1]

    # 설정된 변수명에 위에서 설정한 login 정보 입력
    element_id.send_keys(username)
    element_pw.send_keys(password)
    element_pw.submit()

    password = 0 #RESET Password
    driver.implicitly_wait(5)

    #알림 설정 창을 지우기 위한 '나중에 하기'버튼 클릭
    time.sleep(2)
    driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()


    # [ LOGIN COMPLETE and SEARCH ] #
    # 검색란에 hashTag를 입력하기 위한 경로 찾은 후 send_kyes로 입력
    for tag in tags:
        print('start crawling based on '+tag)
        driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(tag)
        driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]""").click()

        try:
            searchTotalCount = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/header/div[2]/div[2]/span/span""").text
            if int(searchTotalCount) < data_num:
                print('게시물보다 더 많은 수집 데이터 수를 입력하였습니다.')
            else:
                print('검색결과  Total : '+ searchTotalCount +' 건 의 게시물이 검색되었습니다.')

        except:
            pass


        # 해쉬태그 검색 결과에서 각 게시물의 태그 a를 이용해 주소(href)를 가져옴
        elems = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
        links= []

        while len(set(links)) < data_num:
            print('1_the number of links: ', len(set(links)))
            no_of_pagedowns = 2
            elem = driver.find_element_by_tag_name("body")
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
                no_of_pagedowns -= 1

            elems = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
            print('the number of elems',len(elems))
            for ele in elems:
                link = ele.get_attribute("href")
                try:
                    if link in links:
                        pass
                    else:
                        links.append(link)
                        print(link)
                except:
                    continue

        print('2_the number of objects:',len(set(links)))
        all_data = []
        for idx, link in enumerate(links):
            print('idx:',idx)
            file_data = OrderedDict()
            driver.get(link)

            ## 1_image crawling
            # try~execpet for skipping the video post
            try:
                image = driver.find_element_by_xpath("//div[@class='KL4Bh']/img").get_attribute('src')
                file_data["image"] = image
                urllib.request.urlretrieve(image, "../image/" + tag + str(idx) + ".jpg")
                k = tag + str(idx)
                file_data['key'] = k
                print('이미지 저장')
            except:
                print("이미지 저장 실패")
                continue

            ## 2_text crawling
            text = driver.find_element_by_xpath("//div[@class='C4VMK']/span").text
            file_data["text"]=text

            ## 3_hashtag crawling
            hashtags =  driver.find_elements_by_xpath("//div[@class='C4VMK']/span/a")
            hashText=[]
            for hashtag in hashtags:
                hashText.append(hashtag.text)
            file_data["hashtags"] = hashText

            ## 4_date crawling
            try:
                date=driver.find_element_by_xpath("//div[@class='_7UhW9  PIoXz       MMzan   _0PwGv       uL8Hv         ']/time").get_attribute('title')
                file_data["date"] = date
            except:
                continue

            print(file_data)
            all_data.append(file_data)



        ## save all data as json file
        print('the number of cralwing data:', len(all_data))

        with open('instagram_%s.json' %(tag),'w',encoding='UTF-8-sig') as make_file:
            json.dump(all_data, make_file,ensure_ascii=False)
