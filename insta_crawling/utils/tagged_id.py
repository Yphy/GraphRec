def tagged_id(driver):
    """

    :param driver: the address of web page
    :return:
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

    # file_data["text"] = text
    # print('text', "\n", text)