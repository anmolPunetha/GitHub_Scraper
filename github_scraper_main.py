from selenium import webdriver
webdriver_path = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(webdriver_path)
driver.implicitly_wait(15)

import time

# def github_login():
#
#     driver.get('https://github.com/login')
#     login = driver.find_element_by_xpath('//*[@id="login_field"]')
#     login.send_keys('anmolTestAcc')
#
#     pswd = driver.find_element_by_xpath('//*[@id="password"]')
#     pswd.send_keys('ap.anm129@gmail.com*123')
#
#     button = driver.find_element_by_xpath('//*[@id="login"]/div[4]/form/div/input[12]')
#     button.click()
#     time.sleep(2)
#
#     # 2factor auth
#     # using recovery code
#     driver.find_element_by_xpath('//*[@id="login"]/div[7]/ul/li[1]/a').click()
#     time.sleep(5)
#     recovery_input = driver.find_element_by_xpath('//*[@id="recovery_code"]')
#     recovery_input.send_keys('402ff-accee')
#     time.sleep(5)
#     driver.find_element_by_xpath('//*[@id="login"]/form/div[3]/button').click()
#     time.sleep(5)
#
#
# def enter_search(language, location):
#     search = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div[2]/div[1]/div/div/form/label/input[1]')  # search
#     search.send_keys(f'language:{language} location:{location}')
#     time.sleep(1)
#     search.send_keys(Keys.ENTER)


# def get_email_from_patch(profile):
#     # visit the profile
#     profile.find_element_by_css_selector('div.f4.text-normal').click()
#
#     # go to repos
#     driver.find_element_by_xpath('//*[@id="js-pjax-container"]/div[1]/div/div/div[2]/div/nav/a[2]').click()
#     time.sleep(1)
#
#     # go to recent repo
#     driver.find_element_by_xpath('//*[@id="user-repositories-list"]/ul/li[1]/div[1]/div[1]/h3/a').click()
#     time.sleep(2)
#
#     # go to commits->recent commit url
#     driver.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/div[3]/div[1]/div/div[4]/ul/li/a').click()
#     time.sleep(1)
#     link = driver.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div[2]/div[1]/div[2]/ol/li[1]/div[2]/div[1]/a').get_attribute('href')
#     print('got commit link')
#
#     # patch link
#     link = link+'.patch'
#     driver.get(link)
#     time.sleep(1)
#     content = driver.find_element_by_xpath('/html/body/pre').text
#     email = content.split['\n'][1]
#     return email
#     # start splitting


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

# print(candidates)
# '?tab=repositories&type=source'                # removes folk case
# profile->repo (source not fork)->get master commit page->go to recent commit (topmost)->that is the commit url

# 'https://github.com/geohacker?tab=repositories&type=source'
# 'https://github.com/github_username_here/repo_name_here/commits/master'

extract_commit_urls_from_profiles(candidates)
# print(candidates)

get_emails_from_commit_urls(candidates)
print(candidates)


