def text_crawling(driver,user_id):
    """
    :param driver: the address of web page
    :return: the text of uploaded post
    """
    import re

    try:
        if driver.find_element_by_xpath("//div[@class='C4VMK']/h2/a"):
            parent_text = driver.find_element_by_xpath("//div[@class='C4VMK']/span").text

            ids = driver.find_elements_by_xpath("//div[@class='C4VMK']/span/a[@class='notranslate']")
            ids_lst = []
            for id in ids:
                # print('id.text',id.text)
                # ids_lst.append(id.text)
                parent_text = parent_text.replace(id.text,'')

            hashtags = driver.find_elements_by_xpath("//div[@class='C4VMK']/span/a")
            hashtag_lst = []
            for hashtag in hashtags:
                # print('hashtag.text',hashtag.text)
                parent_text = parent_text.replace(hashtag.text,'')
                # print(hashtag_lst.append(hashtag.text))

            parent_text = parent_text.replace('•','')
            parent_text = parent_text.replace('\n',' ')

            return parent_text

    except:
        pass


"""
    try:
        if driver.find_element_by_xpath("//div[@class='C4VMK']/h2/a"):
            tagged_id_lst = []
            ids = driver.find_elements_by_xpath("//div[@class='C4VMK']/span/a[@class='notranslate']")
            for id in ids:
                tagged_id_lst.append(id.text[1:])
            return tagged_id_lst
        else:
            pass
    except:
        pass
"""