def like_log(driver):
    """

    :param driver:
    :param like_num:
    :param date_crawl:
    :return: the number of likes, crawling time and the list of ID who like the post
    """

    import time
    from datetime import datetime
    from selenium.webdriver.common.keys import Keys

    like_log = []

    ## A. Appending crawl_time
    now = datetime.now()
    now_ = now.strftime('%Y-%m-%d %H:%M:%S')
    now_datetime = datetime.strptime(now_, '%Y-%m-%d %H:%M:%S')

    like_log.append(str(now_datetime))

    # B. Appending the number of heart(like)
    try:
        num_heart = driver.find_element_by_class_name('Nm9Fw').text
        like_num = str(num_heart[4:-1])
        like_num = like_num.replace(',','')
        like_log.append(int(like_num))
    except:
        like_log.append(0)

    ## C. Appending a list of 'user_num' of users who liked the post
        # 0. click the button to move into the liked page
    try:
        driver.find_element_by_xpath("//button[@class='_0mzm- sqdOP yWX7d    _8A5w5    ']").click()
        time.sleep(1.0)

            # 1. getting the user_id and user_page_URL
        user_id_adds = driver.find_elements_by_xpath("//div[@class='_7UhW9   xLCgt      MMzan  KV-D4            fDxYl     ']/a")

        # user_id_lst =[]
        # for user in user_id_adds:
        #     user_id = user.get_attribute('title')
        #     user_id_lst.append(user_id)
        #
        # like_log.append(user_id_lst)

        #######################################################
        # 무한 스크롤링의 끝을 알기 위한 변수
        before_scrollHeight = 0

        # 중복 제거 전 팔로우 아이디들
        # 매 스크롤링당 5개 정도씩 아이디가 겹침
        temp_follow_ids = []
        while True:
            # 팔로우 아이디가 있는 탭
            new_tab = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div')
            # 현재 스크롤의 높이
            current_scrollHeight = driver.find_elements_by_css_selector(
                'body > div.RnEpo.Yx5HN > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div')[0].rect['height']
            # 시간이 너무 짧을 경우 current_scrollHeight이 탐지되지 않음
            # 그럴 경우 아래 if문에 걸려서 break
            time.sleep(1)

            # 이전 스크롤의 높이와 현재의 스크롤의 높이가 같다면 더이상 스크롤 할 의미가 없음(끝났기때문에)
            if before_scrollHeight == current_scrollHeight:
                break
            # 아닐경우 제일 위로 스크롤을 올림
            # 아래로만 스크롤 할 경우 로딩이 안되고 멈처버리는 경우가 존재
            else:
                # TODO 굳이 맨 위로 올리지 않고 before_scrollHeight을 사용해도 됨, 다만 execute_script()안에 변수를 문자로 적용시키는 방법이 필요
                driver.execute_script("arguments[0].scrollTop = 0", new_tab)

            # 스크롤 다운
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", new_tab)

            driver.implicitly_wait(1)
            before_scrollHeight = current_scrollHeight

            temp = []
            for row in new_tab.text.split('팔로우'):
                follow_id = row.strip('\n').split('\n')[0]
                if follow_id != '':
                    temp.extend([follow_id])
                else:
                    continue
            temp_follow_ids.extend(temp)

        # 중복 제거 후 팔로우 아이디들
        # 매 스크롤링당 5개 정도씩 아이디가 겹침
        user_ids = list(set(temp_follow_ids))
        print('user_ids',user_ids)

        like_log.append(user_ids)

    except:
        pass

    return  like_log


