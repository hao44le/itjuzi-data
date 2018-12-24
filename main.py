from itjuzi_chrome import *
from mongo import *
import coloredlogs, logging
import sys

# Init logger
log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=log)

def get_content(driver, db, url):
    log.info("before fetch")
    companies = fetch_both_companies_and_details(driver, url)
    if companies is None: return
    for company_id in companies:
        if check_company_id_exist_or_not(db, company_id):
            continue
        tmp_dict = companies[company_id]
        tmp_dict['company_id'] = company_id
        inserts(db, [tmp_dict])

if __name__ == '__main__':
    driver = get_shared_chrome_session()
    url = sys.argv[1]
    print(url)
    # Get all existing question ids
    company_db = get_companies_connections()
    get_content(driver, company_db, url)
