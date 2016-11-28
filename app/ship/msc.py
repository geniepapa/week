from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def grab(bl_num='MSCUOL252100'):
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get("https://www.msc.com/track-a-shipment?agencyPath=chn")

    elem_input = driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_txtBolSearch_TextField")
    elem_input.send_keys(str.strip(bl_num))

    # elem_cookie_accept = WebDriverWait(driver, 10).\
    #    until(EC.element_to_be_clickable((By.ID, "lnkCookieAccept")))
    # elem_cookie_accept.click()

    #elem_search = driver.find_element_by_id("ctl00_ctl00_plcMain_plcMain_TrackSearch_hlkSearch")
    driver.execute_script("WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions('ctl00$ctl00$plcMain$plcMain$TrackSearch$hlkSearch', '', true, 'BolSearchPage', '', false, true))")

    elem_output = WebDriverWait(driver, 10).\
        until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_rptContainers_ctl01_pnlContainer")))

    # print(elem_output.get_attribute("innerHTML"))
    return elem_output.get_attribute("innerHTML")

    driver.close()

if __name__ == '__main__':
    grab()
