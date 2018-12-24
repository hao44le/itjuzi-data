from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
import platform
import atexit
import time

def check_exists_by_xpath(xpath, driver):
    try:
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

def read_itjuzi_cre():
    sec = open('.secret')
    username = '957024640@qq.com'
    password = 'crf456crf'
    sec.close()
    return (username, password)

def login_itjuzi(driver):
    driver.get("https://www.itjuzi.com/login")

    time.sleep(1)
    (username, password) = read_itjuzi_cre()

    username_input = check_exists_by_xpath('//input[@placeholder="手机/邮箱"]', driver)
    username_input.send_keys(username)

    password_input = check_exists_by_xpath('//input[@placeholder="密码"]', driver)
    password_input.send_keys(password)

    confirm_button = check_exists_by_xpath('//button[@class="btn btn-primary submit-btn w-100 mt-3"]', driver)
    driver.execute_script("arguments[0].click();", confirm_button)

    time.sleep(1)

def check_if_next_page_exist(driver):
    return check_exists_by_xpath('//div[@class="custom-btn list-load-more-btn"]', driver)

def fetch_companies(driver, url):
    login_itjuzi(driver)

    driver.get(url)

    # While this is next, go to the next page
    next_page_button = check_if_next_page_exist(driver)
    counter = 0
    while next_page_button is not None and counter <= 2:
        driver.execute_script("arguments[0].click();", next_page_button)
        time.sleep(1)
        next_page_button = check_if_next_page_exist(driver)
        counter += 1
    company_dict = dict()

    # Find the companies id
    company_links = driver.find_elements_by_xpath('//a[contains(text(), "详情")]')

    # Find the companies
    companies = driver.find_elements_by_css_selector("tr")[1:]
    for (index, row) in enumerate(companies):
        # print(row.text)
        company_texts = row.text.split('\n')
        company_name = company_texts[0]
        company_round = company_texts[-1].split()[1]
        if company_round == "尚未获投": continue
        company_url = company_links[index].get_attribute("href")
        company_id = company_url.split('/')[-1]
        print(company_name)
        print(company_url)
        print(company_round)
        print(company_id)
        company_dict[company_id] = {"company_name":company_name, "company_url":company_url, "company_round":company_round}

    return company_dict

def fetch_details(driver, company_id="33759623"):
    return dict()

def get_shared_chrome_session():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    f = open('./config')
    data = json.load(f)
    f.close()
    binPath = ""
    os = platform.system()
    print(os)
    if(os == "Linux"): binPath = data["driver"]["Linux"]
    elif(os == "Windows"): binPath = data["driver"]["Windows"]
    else: binPath = data["driver"]["Darwin"]
    print(binPath)
    driver = webdriver.Chrome(executable_path=binPath, chrome_options=chrome_options)
    atexit.register(before_exit, driver)
    return driver

def before_exit(driver):
    print("Closing driver before exit!")
    try:
        driver.quit()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        print('Already closed')
    print("Bye")

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def fetch_both_companies_and_details(driver, url):
    print("inside fetch_both_companies_and_details")
    companies = fetch_companies(driver, url)
    print("after companies")
    for company_id in companies:
        print(company_id)
        details = fetch_details(driver, company_id)
        companies[company_id] = merge_two_dicts(details, companies[company_id])
    return companies

if __name__ == '__main__':
    driver = get_shared_chrome_session()
    # results = fetch_companies(driver)
    # print(results)
    fetch_details(driver)
