import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver

def geturls():
    #homepage = 'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results'
    #homepage = 'https://www.espncricinfo.com/series/ipl-2019-1165643/match-results'
    homepage='https://www.espncricinfo.com/series/ipl-2018-1131611/match-results'
    page = requests.get(homepage)
    soup = BeautifulSoup(page.content, 'html.parser')
    fixtures = soup.find(class_='card content-block league-scores-container').findAll(class_='match-info-link-FIXTURES')
    commentaryUrls = []
    for fixture in fixtures:
        href = fixture.get('href')
        url = 'https://www.espncricinfo.com'+href.replace('full-scorecard','ball-by-ball-commentary')
        commentaryUrls.append(url)
    return commentaryUrls

def process_short(short_text):
    short = short_text.split(",")[1]
    #as no ball will lead to 0, but it should be 1 for this alone is startswith
    if short.startswith(" no"):
        return 0
    if "1" in short:
        return 1
    elif "2" in short:
        return 2
    elif "3" in short:
        return 3
    elif "4" in short:
        return 4
    elif "FOUR" in short:
        return 4
    elif "5" in short:
        return 5
    elif "6" in short:
        return 6
    elif "SIX" in short:
        return 6
    return short

def convert_pd(driver):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    header = soup.find(class_='match-header')
    teams = header.find(class_='teams')
    team_names = teams.findAll(class_='name')
    team_scores = teams.findAll(class_='score')
    team_scores = [name.text.split('/')[0] for name in team_scores]
    chasing_team_won = 1 if team_scores[1] > team_scores[0] else 0
    header_info = soup.find(class_='header-info').find(class_='description').text
    ground_name = header_info.split(",")[1]
    comments = soup.find(class_='match-body').findAll(class_='match-comment')
    overs = []
    short_texts = []
    #short_texts_test = []
    for comment in comments:
        over = comment.find(class_='match-comment-over').text
        short_text = comment.find(class_='match-comment-short-text').text
        short_text= process_short(short_text)
        overs.append(over)
        short_texts.append(short_text)
        #short_texts_test.append(short_text_test)

    #10.2%1 is coming as 1.99999999999 so using round,
    balls_remaining = [int(int(float(over)) * 6 + round(float(over) % 1 * 10)) for over in overs]

    commentary_data = pd.DataFrame({
        "first_batting":team_names[0],
        "second_batting":team_names[1],
        "ground_name": ground_name,
        "ball_number":balls_remaining,
        "current_ball_run":short_texts,
        "chasing_team_won": chasing_team_won,
        #"short_test":short_texts_test,
    })
    return commentary_data

def getMatchCommentary(url):

    driver.get(url)
    #Adding below line to handle super overs, Super over is actually li[3] so li[2] selects second innings as usual
    driver.find_element_by_xpath(
        "//section[@id='main-container']/div/div/div[2]/div[2]/div/div[2]/div/div/div/button/i").click()
    driver.find_element_by_xpath(
        "//section[@id='main-container']/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/ul/li[2]").click()

    commentary_data_first = convert_pd(driver)
    return commentary_data_first

if __name__ == '__main__':
    chrome_driver = r'D:\Downloads\chromedriver\chromedriver.exe'
    #chrome_service = Service(chrome_driver)
    driver = webdriver.Chrome(executable_path=chrome_driver)
    mainDF = pd.DataFrame(columns=["first_batting","second_batting","ground_name","ball_number", "current_ball_run","chasing_team_won"])
    commentaryUrls = ["https://www.espncricinfo.com/series/ipl-2019-1165643/chennai-super-kings-vs-royal-challengers-bangalore-1st-match-1175356/ball-by-ball-commentary"
                      ,"https://www.espncricinfo.com/series/ipl-2020-21-1210595/delhi-capitals-vs-sunrisers-hyderabad-qualifier-2-1237180/ball-by-ball-commentary"]
    #commentaryUrls = geturls()
    for url in commentaryUrls:
        commentary = getMatchCommentary(url)
        mainDF = pd.concat([mainDF, commentary], axis=0)
    driver.quit()
    mainDF.to_csv(r'data\commentary_data.csv', index = None, header=True)
