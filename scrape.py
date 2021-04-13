import requests
from bs4 import BeautifulSoup

def scrape_job():
  url = requests.get('https://malaysia.indeed.com/jobs?q=python&l=').text
  soup = BeautifulSoup(url, 'html.parser')
  job_name = soup.find('h2', class_='title').a.text.replace("\n", '')
  comp_name = soup.find('span', class_='company').text.replace("\n", '')
  location = soup.find('span', class_='location accessible-contrast-color-location').text.replace("\n",'')

  idict = {}
  idict['Job name'] = job_name
  idict['Company name'] = comp_name
  idict['Location'] = location

  return idict