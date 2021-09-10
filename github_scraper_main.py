from functions import github_scraper,sheet_updation

if __name__ == '__main__':

    # github profile link, name, location, language, commit url, email
    # followers, stars etc can also be easily appended in it

    candidates = []
    
    # scope of adding more languages/location clearly lies here.
    languages = ['javascript', 'kotlin', 'python'] 
    location = 'India'
    page_limit = 30

    for language in languages:
        print(language)
        try:
            github_scraper(candidates, language, location, page_limit)
        except Exception as e:
            print(e)

    sheet_updation(candidates)


