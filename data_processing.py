import requests
from bs4 import BeautifulSoup
import pandas as pd

# Import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import undetected_chromedriver as uc

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Helper Functions
def MakeSoup(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text)

    return soup

# Ideal driver to use (needed for ESPN) but may be slower
def create_sneaky_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    #if the previous line doesn't work uncomment the next line and update with the chrome version that you have
    #driver = uc.Chrome(version_main=148) 

    return driver

# Fallback if uc driver doesn't work
def create_driver(): 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def MakeSelenium(url, driver=None):
    if not driver:
        driver = create_sneaky_driver()
    try:
        driver.get(url)
    
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        driver.quit()
    
    return soup

def NFL(url):

  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')
  p = art.find_all('p')
  st = ""
  for ps in p:
      text = ps.get_text()
      st += text
  return st

def BBC(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text)

    Text = soup.find('div', 'ssrcss-nqezkk-RichTextContainer e5tfeyi1')

    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')

    return Text
'''
  divs = art.find_all('div', "ssrcss-oyhass-Spacer e1aon0op0")

  st = ""
  for div in divs:
      paragraphs = div.find_all('p')
      for p in paragraphs:
          st += p.get_text()

  return st
  '''

def BD(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div')

  st = ""
  for div in divs:
      paragraphs = div.find_all('p')
      for p in paragraphs:
          st += p.get_text()

  return st

def NFLDD(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'body-content post-content-wrap')

  st = ""
  for div in divs:
      paragraphs = div.find_all('p', recursive=False)
      for p in paragraphs:
          st += p.get_text()

  return st

def NYP(url):


  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'single__content entry-content m-bottom')

  st = ""
  for div in divs:
      paragraphs = div.find_all('p')
      for p in paragraphs:
          st += p.get_text()

  return st

def PFF(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')
  divs = art.find_all('div', 'm-longform-copy')

  st = ""

  for div in divs:
      elements = div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
      for el in elements:
          st += el.get_text()

  return st

def SI(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'article-content')

  st = ""

  for div in divs:
      elements = div.find_all('p', recursive=False)
      for el in elements:
          st += el.get_text()

  return st

def NBCP(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'article-content rich-text')

  st = ""

  for div in divs:
      elements = div.find_all('p', recursive=False)
      for el in elements:
          st += el.get_text()

  return st

def ITI(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'article-content [&_p]:leading-[30px] [&_p]:md:leading-[28px] [&_li]:leading-[30px] [&_li]:md:leading-[28px]')

  st = ""

  for div in divs:
      elements = div.find_all('p', recursive=False)
      for el in elements:
          st += el.get_text()

  return st

def ATZ(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  divs = soup.find_all('div', 'entry-content has-global-padding single-layout-with-rail wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow')

  st = ""

  for div in divs:
      elements = div.find_all('p', recursive=False)
      for el in elements:
          st += el.get_text()

  return st

def LAT(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'ct-rich-text-children font-cms-font-brand-text font-normal text-lg leading-7.75 [&_>p]:text-cms-story-body-color-text clearfix max-w-170 mt-7.5 mb-10 mx-auto')

  st = ""

  for div in divs:
      elements = div.find_all('p', recursive=False)
      for el in elements:
          st += el.get_text()

  return st

def FD(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'portableText_typography__S8q5x')

  st = ""

  for div in divs:
      elements = div.find_all('p', recursive=False)
      for el in elements[:len(elements)-4]:
          st += el.get_text()

  return st

def NFLM(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find_all('div', 'flex flex-wrap justify-center lg:justify-normal md:mx-10')

  st = ""

  for div in divs:
      elements = div.find_all('p')
      for el in elements[:len(elements)-4]:
          st += el.get_text()

  return st

def NBC(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  div = soup.find('div', 'RichTextArticleBody RichTextBody')

  p = div.find_all('p')
  st = ""
  for ps in p:
        text = ps.get_text()
        if text[0] == '_':
            return st
        st += text
  return st

def CP(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article', 'article-body prose max-w-none pb-7 pt-5 prose-figure:max-w-full prose-ol:pl-10 prose-img:max-w-full prose-video:max-w-full md:prose-ol:pl-6 [&_iframe]:m-auto [&_iframe]:block [&_iframe]:max-w-full')

  p = art.find_all('p', recursive=False)

  st = ""

  for ps in p:
        text = ps.get_text()
        if text[0] == '_':
            return st
        st += text
  return st

def CC(url):
  response = requests.get(url, headers=headers)

  soup = BeautifulSoup(response.text)

  art = soup.find('article')

  divs = art.find('div', 'article-content [&_p]:leading-[30px] [&_p]:md:leading-[28px] [&_li]:leading-[30px] [&_li]:md:leading-[28px]')
  st = ""

  elements = divs.find_all('p')
  for el in elements:
          st += el.get_text()

  return st

def AXIOS(url):
    soup = MakeSelenium(url)

    elements = soup.find('span', attrs={'data-schema': 'smart-brevity'})

    st = ""
    for element in elements:
        text = element.get_text()
        st += text
    
    elements = soup.find('span', attrs={'data-nosnippet': True, 'class': 'gated-content'}).find_all(['p', 'ul'])

    for element in elements:
        if element.name == 'ul':
            for li in element.find_all('li'):
                st += li.get_text()
        else:
            st+=element.get_text()
   
    return st

def AP(url):
    soup = MakeSoup(url)

    p = soup.find('bsp-story-page').find_all('p')
    st = ""
    for ps in p:
        text = ps.get_text()
        if text[0] == '_':
            return st
        st += text
        
    return st

def CBS(url):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text)

    p = soup.find('div', class_='Article-content').find_all('p')
    st = ""
    for ps in p:
        text = ps.get_text()
        st += text

    clean_text = st.replace("\xa0", "")
        
    return clean_text

def ESPN(url):
    soup = MakeSelenium(url)
    
    elements = soup.find('div', class_='article-body').find_all('p')

    st = ""
    for element in elements:
        text = element.get_text()
        st += text + " "

    # Clean the text
    clean_text = st.replace('\xa0', ' ')
    clean_text = clean_text.replace("\\'", "'")
    clean_text = clean_text.replace('\n', ' ')
    clean_text = clean_text.replace('\t', ' ')
    clean_text = ' '.join(clean_text.split())

    return clean_text

def F13(url):
    soup = MakeSoup(url)

    p = soup.find('div', class_='article-body').find_all('p')
    st = ""
    for ps in p:
        text = ps.get_text()
        st += text

    clean_text = st.replace("\xa0", "")
        
    return clean_text

def FS(url):
    soup = MakeSoup(url)
    '''
    p = soup.find('div', class_='article-content-body flex-col').find_all('p')
    st = ""
    for ps in p:
        text = ps.get_text()
        st += text

    clean_text = st.replace("\xa0", "")
        
    return clean_text
    '''
    art = soup.find('article')
    st = ""

    if art:
        divs = art.find_all('div')

        for div in divs:
            paragraphs = div.find_all('p')
            for p in paragraphs:
                st += p.get_text()
        st = st.replace("\xa0", "")
    else:
        iden = soup.find(id = 'article-content')
        divs = iden.find_all('div')

        for div in divs:
            paragraphs = div.find_all('p')
            for p in paragraphs:
                st += p.get_text()
        st = st.replace("\xa0", "")

    return st

def GE(url):
    soup = MakeSelenium(url)

    content_div = (soup.find('div', class_='gnt_ar_b'))

    p = content_div.find_all('p')

    st = ""
    for ps in p:
        text = ps.get_text()
        st += text
    clean_text = st.replace("\xa0", "")
        
    return clean_text

def NYT(url):
    soup = MakeSoup(url)

    p = soup.find('div', class_='Article_ContentContainer__jBNW3 article-content-container bodytext1').find_all('p')
    st = ""
    for ps in p:
        text = ps.get_text()
        if text == 'Advertisement':
            text = " "
        st += text

    clean_text = st.replace("\xa0", "")
        
    return clean_text 

def AL(url):
    soup = MakeSelenium(url)

    elements = soup.find('div', class_='entry-content').find_all('p')

    st = ""
    for element in elements:
        text = element.get_text()
        if text.isupper():
            text = " "
        st += text
   
    return st

def NTS(url):
    soup = MakeSelenium(url)

    elements = soup.find('div', class_='server-rendered').find('article').find_all('p')

    st = ""
    for element in elements:
        text = element.get_text()
        st += text

    clean_text = st.replace("\n", "")
        
    return clean_text

def CLE(url):
    soup = MakeSelenium(url)

    p = soup.find('div', class_='entry-content').find_all('p')

    st = ""
    for ps in p:
        text = ps.get_text()

        if text == 'More Browns coverage':
            break      
        st += text
        st += " "

    clean_text = st.replace("\xa0", "")
        
    return clean_text

def NBCNY(url):
    soup = MakeSoup(url)

    Text = soup.find('div', class_ = "article-content rich-text")

    Ad = Text.find('div', class_ = "recirc-module")
    Ad.decompose()

    Text = Text.get_text(separator = ' ', strip = True)

    Text = Text.replace('\xa0', ' ')

    #Text = Text.replace("\'", "'")

    return Text

def Sports247(url):
    soup = MakeSoup(url)
    
    Text = soup.find('section', class_ = 'article-body is-guest')
    
    for trash in Text.css.select('div', class_ = ['embedVideo', 'in-content-ad advertisement', 'GamblingPartnerAd', 'in-content-ad']):
        trash.decompose()
    
    Ad = Text.find('strong')
    Ad.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def WebZone49er(url):
    soup = MakeSoup(url)
    
    Text = soup.find('div', class_ = 'article-text autolink')
    
    for trash in Text.css.select('div', class_ = 'adblock_container article-hide'):
        trash.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def NinersNation(url):
    soup = MakeSoup(url)
    
    article = soup.findAll('div', class_ = 'duet--article--article-body-component')

    Text = ''

    for text in article:
        Text += text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def SportingNews(url):
    soup = MakeSoup(url)
    
    Text = soup.find('div', class_ = 'text-body-1')
    
    for trash in Text.css.select('div', class_ = ['zephr-feature_video-player', 'image-wrapper', 'adPlaceholder-0', 'adPlaceholder-1', 'adPlaceholder-2', 'adPlaceholder-3', 'adPlaceholder-4', 'adPlaceholder-5', 'adPlaceholder-6', 'link-stack-slot']):
        trash.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def WCVB(url):
    soup = MakeSoup(url)
    
    for tweet_widget in soup.find_all('div', {'class': 'embed-inner'}):
        tweet_widget.decompose()
    
    Text = soup.find('div', class_ = 'article-content--body-text')

    for trash in Text.css.select('div', class_ = 'screen-reader-only'):
        trash.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def SBNation(url):
    soup = MakeSoup(url)
    
    Text = soup.find('div', class_ = '_1nfb3k411')

    Ad = Text.find('div', class_ = '_8kam0j0')
    Ad.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def LASportsHub(url):
    soup = MakeSoup(url)
    
    Text = soup.find('div', class_ = 'nfl-c-article__body d3-l-grid--inner')

    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def FootballGuys(url):
    soup = MakeSoup(url)
    
    Text = soup.find('div', class_ = 'col col-12 col-lg-8 article-content')
    
    for trash in Text.find_all('div', class_ = ['article-image-credit my-3', 'mb-4']):
        trash.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def JustBlogBaby(url):
    soup = MakeSoup(url)
    
    Text = soup.find('div', class_ = 'article-content [&_p]:leading-[30px] [&_p]:md:leading-[28px] [&_li]:leading-[30px] [&_li]:md:leading-[28px]')

    for trash in Text.find_all('div', class_ = ['flex min-w-0 flex-1 items-center gap-3']):
        trash.decompose()

    Ad = Text.find('h2', id = 'inline-text-11')
    Ad.decompose()
    
    for hidden_tag in Text.select('[style*="display:none"], [style*="visibility:hidden"], .hidden'):
        hidden_tag.decompose()
    
    Text = Text.get_text(separator = ' ', strip = True)
    
    Text = Text.replace('\xa0', ' ')
    
    return Text

def YahooSports(url):  
    soup = MakeSoup(url)
    
    for tweet_widget in soup.find_all('div', {'class': 'tweet-wrapper'}):
        tweet_widget.decompose()
    
    Text = soup.find('div', class_ = 'content-body')
    st = ""

    if Text:
        for trash in Text.css.select('figcaption', class_ = 'fig-caption'):
            trash.decompose()

        for hidden_tag in Text.select('[style*="display:none"], [style*="visibility:hidden"], .hidden'):
            hidden_tag.decompose()

        Text = Text.get_text(separator = ' ', strip = True)
    
        Text = Text.replace('\xa0', ' ')

        return Text
    else:
        art = soup.find('article')

        divs = art.find_all('div')

        for div in divs:
            paragraphs = div.find_all('p')
            
            for p in paragraphs:
                st += p.get_text()
                
        st = st.replace("\xa0", "")

        return st
    '''
    does not work T-T
    for hidden_div in Text.select('p div'):
        hidden_div.decompose()
    '''
    
    return

df = pd.read_csv('https://raw.githubusercontent.com/anjalinambudiri-jpg/NFL-Sentiment-Analysis/refs/heads/Web-scraping-Function/Training%20Set%20Final.csv')

df = df[['Date','Topic/Name', 'Source', 'Link', 'Sentiment']]

df['Text'] = ""

source_function_map = {
    'NFL': NFL,
    'NYP': NYP,
    'NBC': NBC,
    'BBC': BBC,
    'BD': BD,
    'NFLDD': NFLDD,
    'PFF': PFF,
    'SI': SI,
    'NBCP': NBCP,
    'ITI': ITI,
    'ATZ': ATZ,
    'LAT': LAT,
    'FD': FD,
    "NFLM": NFLM,
    'CP': CP,
    'CC': CC,
    'AX' : AXIOS,
    'AP': AP,
    'CBS' : CBS,
    'ESPN' : ESPN,
    'F13' : F13,
    'FS' : FS,
    'GE' : GE,
    'NYT' : NYT,
    'AL' : AL,
    'NTS' : NTS,
    'CLE' : CLE,
    'NBCNY' : NBCNY,
    'SPO247' : Sports247,
    'WZ' : WebZone49er,
    'NN' : NinersNation,
    'SN' : SportingNews,
    'WCVB' : WCVB,
    'YS' : YahooSports
}

def process_row(row):
    source = row['Source']
    # Force the Link to a string to ensure it has quotes/string properties
    link_str = str(row['Link'])

    # Check if we have a registered function for this source
    if source in source_function_map:
        run_function = source_function_map[source]
        return run_function(link_str)

    # If the source isn't in our dictionary, keep the existing Text
    return row['Text']

df['Text'] = df.apply(process_row, axis=1)

df.to_csv('ScrapedTraining.csv', index=False)