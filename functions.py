from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time
from constants import gsheet_scope,webdriver_path
from selenium import webdriver

driver = webdriver.Chrome(webdriver_path)
driver.implicitly_wait(15)


def get_url_for_search(page, language, location):
    url = f'https://github.com/search?p={page}&q=language%3A{language}+location%3A{location}'
    return url


def search_repos(candidates, language):
    # get all profiles of page
    profiles = driver.find_elements_by_css_selector('div.d-flex.hx_hit-user.px-0.Box-row')
    for profile in profiles:
        data = profile.find_elements_by_css_selector('div.mr-3')
        precise_location = data[0].text

        time.sleep(1)
        primary_info = profile.find_element_by_css_selector('a.mr-1')

        profile_url = primary_info.get_attribute('href')
        name = primary_info.text

        candidate = [profile_url, name, precise_location, language]
        candidates.append(candidate)
        # print(profile_url, name, precise_location, email)


def extract_commit_urls_from_profiles(candidates):
    for candidate in candidates:
        url = candidate[0]
        url += '?tab=repositories&type=source'  # to go to recent repo which he sourced
        driver.get(url)
        time.sleep(3)

        try:
            recent_repo = driver.find_element_by_xpath(
                '//*[@id="user-repositories-list"]/ul/li[1]/div[1]/div[1]/h3/a').get_attribute(
                'href')  # going to recent repo
            master_commit = recent_repo + '/commits'
            # print(master_commit)
            driver.get(master_commit)
            time.sleep(2)
            commit_link = driver.find_element_by_xpath(
                '//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/ol/li/div[2]/div[1]/a').get_attribute(
                'href')
            # print(commit_link)

        except Exception as e:
            print(e)
            commit_link = None

        candidate.append(commit_link)


def get_emails_from_commit_urls(candidates):
    for candidate in candidates:
        commit_url = candidate[3]

        if commit_url:
            patch_link = commit_url + '.patch'
            driver.get(patch_link)
            content = driver.find_element_by_xpath('/html/body/pre').text
            content = content.split('\n')

            email = content[1].split(" ")[-1][1:-1]
            if '.com' not in email and '@' not in email:
                email = content[2][2:-1]

            # print(email)
            time.sleep(2)

        else:
            email = None
        candidate.append(email)
    # return email


def github_scraper(candidates, language, location, page_limit):
    for page_num in range(1, page_limit):
        base_url = get_url_for_search(page_num, language, location)

        driver.get(base_url)
        search_repos(candidates, language)
        time.sleep(3)

    extract_commit_urls_from_profiles(candidates)

    get_emails_from_commit_urls(candidates)
    print(candidates)


def gsheet_setup():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials_gsheet.json', gsheet_scope)
    client = gspread.authorize(credentials)
    return client


def sheet_updation(candidates):
    client = gsheet_setup()
    sheet = client.open('Github Scrapped Data').worksheet('Sheet1')

    # this can be made dynamic if the code is pushed into server
    sheet.insert_rows(values=candidates, row=2)
