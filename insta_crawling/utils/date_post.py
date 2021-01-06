def date_post(driver, link):
    """

    :param driver: the address of web page
    :return:the date of uploaded post
    """
    from datetime import datetime, timedelta
    import sys
    sys.path.append("/home/user/insta_crawler")


    driver.get(link)

    # Converting UTC time into KST time
    def utc_to_local(utc):
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        utc_ = datetime.strptime(utc, date_format)
        kst = utc_ + timedelta(hours=9)
        return kst.strftime('%Y-%m-%d %H:%M')

    try:
        date = driver.find_element_by_xpath("//div[@class='k_Q0X NnvRN']/a/time").get_attribute('datetime')
        datetime_ = utc_to_local(date)

        # return datetime.strptime(datetime_, "%Y-%m-%d %H:%M").time()
        return datetime.strptime(datetime_, "%Y-%m-%d %H:%M")
        # return datetime

    except:
        print('there is an error about date cralwing')
