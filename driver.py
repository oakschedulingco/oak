from loguru import logger
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By

def get_to_the_thing(zip, dob, email, phone, smsyes, flu, covid, rsv, pneumonia, shingles, radius):
    driver = webdriver.Chrome()
    driver.get("https://www.walgreens.com/findcare/schedule-vaccine")

    driver.implicitly_wait(1)
    zipcode_box = driver.find_element(by=By.ID, value="autocomplete-search")
    dob_box = driver.find_element(by=By.ID, value="userDob")
    email_box = driver.find_element(by=By.ID, value="field-email")
    phone_box = driver.find_element(by=By.ID, value="field-phone")
    checkbox_box = driver.find_element(by=By.ID, value="sms-yes")

    zipcode_box.send_keys(zip)
    dob_box.send_keys(dob)
    email_box.send_keys(email)
    phone_box.send_keys(phone)
    if smsyes:
        checkbox_box.click()

    sleep(1.5)

    next1_btn = driver.find_element(by=By.ID, value="nextBtn")
    next1_btn.click()

    sleep(1.5)

    if flu:
        driver.find_element(by=By.ID, value="check-1").click()
    if covid:
        driver.find_element(by=By.ID, value="check-2").click()
    if rsv:
        driver.find_element(by=By.ID, value="check-3").click()
    if pneumonia:
        driver.find_element(by=By.ID, value="check-4").click()
    if shingles:
        driver.find_element(by=By.ID, value="check-5").click()

    sleep(1.5)

    driver.find_element(by=By.CLASS_NAME, value="vaccine-list-btn").click()

    sleep(1.5)

    driver.find_element(by=By.CLASS_NAME, value="cursor-pointer").click()

    sleep(1.5)

    driver.find_element(by=By.ID, value="editBoosterOverlay").click()

    radius_dropdown = driver.find_element(by=By.ID, value="distance-dropdown")
    radius_dropdown.click()
    radius_dropdown.send_keys(radius)
    radius_dropdown.send_keys("\n")

    validate_radius = driver.find_element(by=By.CLASS_NAME, value="zipvalidation")
    validate_radius.click()

    sleep(1.5)

    calendar = driver.find_element(by=By.ID, value="cal_btn_id_3")
    calendar.click()

    sleep(1.5)
    return driver

def check_date_availability(zip, dob, email, phone, smsyes, flu, covid, rsv, pneumonia, shingles, radius, date):
    driver = get_to_the_thing(zip, dob, email, phone, smsyes, flu, covid, rsv, pneumonia, shingles, radius)

    try:
        driver.find_element(by=By.CSS_SELECTOR, value=f'button[data-date=\'{date}\']').click()
        sleep(2)
        elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'wag-store-info-')]")
        max_number = max([int(element.get_attribute('id').split('-')[-1]) for element in elements], default=0)

        da_soup = BeautifulSoup(driver.page_source, 'html.parser')

        locations_list = []
        for locations in range(max_number + 1):
            element_id = f'wag-store-info-{locations}'
            location_element = driver.find_element(By.ID, element_id).text.split("\n")
            distance = location_element[1]
            street_address = location_element[2]
            csz = location_element[3]

            parentElem = da_soup.find('li', id=element_id)
            all_spans = parentElem.find_all('span', {'class': 'newTimeslot__text'})
            available_timeslots = ', '.join([f'{e.text}' for e in all_spans])

            locations_list.append(f"{street_address}, {csz} - {distance} away - slots: {available_timeslots[:5]} - id {locations}")

        return locations_list

    except:
        driver.quit()
        return False

def book_timeslot(zip, dob, email, phone, smsyes, flu, covid, rsv, pneumonia, shingles, radius, date, location_id, time):
    driver = get_to_the_thing(zip, dob, email, phone, smsyes, flu, covid, rsv, pneumonia, shingles, radius)

    try:
        driver.find_element(by=By.CSS_SELECTOR, value=f'button[data-date=\'{date}\']').click()
        sleep(2)
        elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'wag-store-info-')]")
        max_number = max([int(element.get_attribute('id').split('-')[-1]) for element in elements], default=0)

        da_soup = BeautifulSoup(driver.page_source, 'html.parser')

        for locations in range(max_number + 1):
            if locations != location_id:
                continue
            element_id = f'wag-store-info-{locations}'
            location_element = driver.find_element(By.ID, element_id).text.split("\n")
            distance = location_element[1]
            street_address = location_element[2]
            csz = location_element[3]

            elem = driver.find_element(By.CSS_SELECTOR, f'span.newTimeslot__text:contains(\'{time}\')')
            elem.click()

            input()
    except e:
        print(e)
        input()
        driver.quit()
        return False
