import re
import requests
from bs4 import BeautifulSoup
from db import User, session


def scrapehtml(filename):
    # Load the HTML file
    with open(f"{filename}.html", "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "lxml")

    all_text_html = soup.get_text()
    scripts = soup.find_all("script")
    for script in scripts:
        all_text_html += script.string or " "

    # grabbing every tag availiable from the content
    # soup.findall
    # tag (element) loop through attributes tied to the element
    # value elements grab the string value and concatinate it to  our All_text
    for tag in soup.find_all(True):
        for attr in tag.attrs:
            value = tag.attrs[attr]
            if isinstance(value, str):
                all_text_html += value

    username_pattern = r'\b[a-zA-Z0-9._-]{3,20}\b'
    usernames = set(re.findall(username_pattern, all_text_html))
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    emails = set(re.findall(email_pattern, all_text_html))
    return usernames, emails


def webscrape(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        all_text_web = soup.get_text()

        # Find usernames (example: words 3-20 chars, alphanumeric with some symbols)
        username_pattern = r'\b[a-zA-Z0-9._-]{3,20}\b'
        usernames = set(re.findall(username_pattern, all_text_web))

        # Find emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = set(re.findall(email_pattern, all_text_web))
        return usernames, emails
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return set(), set()

def scrape_website(url):
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content (modify selectors based on website structure)
        text_content = soup.get_text(strip=True)

        # Find usernames (example: words 3-20 chars, alphanumeric with some symbols)
        username_pattern = r'\b[a-zA-Z0-9._-]{3,20}\b'
        usernames = set(re.findall(username_pattern, text_content))

        # Find emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = set(re.findall(email_pattern, text_content))

        return usernames, emails
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return set(), set()

def check_matches(usernames, emails):
    matches = {'usernames': [], 'emails': []}

    # Query database for matching usernames
    for username in usernames:
        if session.query(User).filter_by(username=username).first():
            matches['usernames'].append(username)

    # Query database for matching emails
    for email in emails:
        if session.query(User).filter_by(email=email).first():
            matches['emails'].append(email)

    return matches

