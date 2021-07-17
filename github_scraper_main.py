import time

from selenium import webdriver
webdriver_path = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(webdriver_path)
driver.implicitly_wait(15)


def search_repos(candidates):

    # get all profiles of page
    profiles = driver.find_elements_by_css_selector('div.d-flex.hx_hit-user.px-0.Box-row')
    for profile in profiles:
        data = profile.find_elements_by_css_selector('div.mr-3')
        precise_location = data[0].text

        primary_info = profile.find_element_by_css_selector('a.mr-1')

        profile_url = primary_info.get_attribute('href')
        name = primary_info.text

        email = None
        if len(data) > 1:                   # if email is directly available
            email = data[1].text

        # else:                               # else visit them
            # email = get_email_from_patch(profile)
            # emails.append(email)
        candidate = [profile_url, name, precise_location]
        candidates.append(candidate)
        # print(profile_url, name, precise_location, email)


def get_url_for_search(page):
    language = 'javascript'
    location = 'India'
    url = f'https://github.com/search?p={page}&q=language%3A{language}+location%3A{location}'
    return url


def extract_commit_urls_from_profiles(candidates):
    for candidate in candidates:
        url = candidate[0]
        url += '?tab=repositories&type=source'     # to go to recent repo which he sourced
        driver.get(url)
        time.sleep(2)

        try:
            recent_repo = driver.find_element_by_xpath('//*[@id="user-repositories-list"]/ul/li[1]/div[1]/div[1]/h3/a').get_attribute('href')     # going to recent repo
            master_commit = recent_repo+'/commits'
            # print(master_commit)
            driver.get(master_commit)
            time.sleep(1)
            commit_link = driver.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/ol/li/div[2]/div[1]/a').get_attribute('href')
            print(commit_link)

        except Exception as e:
            print(e)
            commit_link = None

        candidate.append(commit_link)


def get_emails_from_commit_urls(candidates):
    for candidate in candidates:
        commit_url = candidate[3]

        if commit_url:
            patch_link = commit_url+'.patch'
            driver.get(patch_link)
            content = driver.find_element_by_xpath('/html/body/pre').text
            content = content.split('\n')

            email = content[1].split(" ")[-1][1:-1]
            if '.com' not in email and '@' not in email:
                email = content[2][2:-1]

            print(email)
            time.sleep(1)

        else:
            email = None
        candidate.append(email)
    # return email


candidates = []
for page_num in range(1, 2):
    base_url = get_url_for_search(page_num)
    driver.get(base_url)
    search_repos(candidates)
    time.sleep(2)
    

extract_commit_urls_from_profiles(candidates)
# print(candidates)

get_emails_from_commit_urls(candidates)
print(candidates)
