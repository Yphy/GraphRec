def user_id_num(driver):
    """

    :param driver: the address of web page
    :return: a listh which is consist of nickname and the ID of post's ownder
    """

    ## 1_user id which can be modified as like a nickname
    user_id = driver.find_element_by_xpath("//div[@class='e1e1d']/h2/a").get_attribute("title")

    ## 2_user num which cannot be converted
    user_num =  driver.find_element_by_xpath("//meta[@property='instapp:owner_user_id']").get_attribute('content')

    return user_id, user_num