# Instagram Data Scraper

This Python script is a tool for scraping data from Instagram. By entering your own username and password, you can access another user's account and retrieve the following information:

- Number of followers
- Number of following
- Number of posts
- Link and number of likes and comments for each post

## Installation

1. Install the required packages: selenium, BeautifulSoup, and requests.
2. Download the chromedriver.exe file for your operating system and place it in an appropriate location.

## Usage

To use the script, simply call the `instagram_data_scraper` function and provide your own username and password as well as the target user's username.

```python
username = "your_username"
password = "your_password"

instagram_data_scraper(username, password, "target_username")
```

The data will be saved to a JSON file named after the target user's username.

Please note that the script uses Selenium to automate interaction with the Instagram website, which may be against their terms of service. Use at your own risk.

## Improvements

- Use automated login with cookies for a better user experience.
- Avoid using hardcoded patterns in favor of CSS classes for increased flexibility and robustness.
