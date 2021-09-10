# GitHub_Scraper
An advance github scraper which scrapes various data items from github based on various preferences. The primary search query is based on language and location. Based on that, profiles' github id, name, commit url, precise location, email and some other items are extracted through this.

After this, the data extracted is saved in a Google Sheet via Google Sheet API advance options. With github search rate limit as 30 queries/min, around 1000 entries (around 5000 data items) from various domains were extracted in a time duration of 100min (approx). The addition to google sheet was made quite faste and it hardly took more a min to push it to the sheet. 
