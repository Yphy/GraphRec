def image_crawling(driver, link):
    """

    :param driver: the address of web page
    :return: images' address which is uploaded on a specific webpage
    """
    import time
    try:
        driver.get(link)
        images = []
        img_elems = driver.find_elements_by_xpath("//div[@class='KL4Bh']/img")
        for img in img_elems:
            images.append(img.get_attribute('src'))

        ## if there were some images, click the button and collect the image
        while True:
            try:
                driver.find_element_by_xpath("//button[@class='  _6CZji']").click()
                time.sleep(0.8)

                img_elems = driver.find_elements_by_xpath("//div[@class='KL4Bh']/img")
                for img in img_elems:
                    src = img.get_attribute('src')
                    if src in images:
                        continue
                    else:
                        images.append(src)
            except:
                break
        return images

    except:
        print("This post is not an image but a video")
        pass