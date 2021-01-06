def hash_crawling(driver):
    """

    :param driver: the address of web page
    :return: a list of hashTag
    """

    try:
        hashtags_text = []
        hashtags =  driver.find_elements_by_xpath("//meta[@property='instapp:hashtags']")
        print('the number of hashtags:',len(hashtags))
        for hash  in hashtags:
            hashtags_text.append(hash.get_attribute("content"))
    except:
        print("There are no hashtags on the post")
        hashtags_text = None
    return hashtags_text
