def like_num(driver):
    """
    :param driver: the address of web page
    :return: the number of heart
    """
    try:
        num_heart = driver.find_element_by_class_name('Nm9Fw').text
        num_heart_str = num_heart[4:-1]
        int_like_num = int(num_heart_str.replace(",",""))
        # print('int_like_num',int_like_num,type(int_like_num))
        return int_like_num
    except:
        print("There are no any likes")
        return 0

