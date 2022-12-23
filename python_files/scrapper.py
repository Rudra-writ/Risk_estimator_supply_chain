from pydoc import classname
import requests
from requests_html import AsyncHTMLSession
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from googletrans import Translator, constants
from geopy.geocoders import Nominatim
import pandas as pd
import glob,os
import re
import nltk
from nltk.tokenize import word_tokenize
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from nltk import pos_tag
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def scroll_down(driver):
    start = time.time()
    initialScroll = 0
    finalScroll = 1000
    while True:
            driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")
        
            initialScroll = finalScroll
            finalScroll += 1000

            time.sleep(1)
            end = time.time()
        
            if round(end - start) > 12:
                break

def basicInfo_scrape(company_name):
        

        company = []
        company = company_name.lower().split()
        company = ('+').join(company)+'+'+'linkedin'
        company2 = company_name.lower().split()
        company2 = ('-').join(company2)
        print(company2)

        driver.get("https://www.google.com/search?q="+company+"&oq="+company+"&aqs=chrome..69i57j0i19i22i30l7.7380j0j15&sourceid=chrome&ie=UTF-8")

        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        google_link_div = soup.find_all('div', {'class':'yuRUbf'})

        links = []
        
        for div in google_link_div:
            links.append(div.find('a', href = True)['href'] if (set(['de.linkedin.com', company2]).issubset( re.split( '/|-', div.find('a', href = True)['href'])) or set(['de.linkedin.com', company2]).issubset( re.split( '/', div.find('a', href = True)['href']))  or set([ 'company', "linkedin",company2]).issubset( re.split( '/|.', div.find('a', href = True)['href'])) or set([ 'company', "www.linkedin.com"]).issubset( re.split( '/', div.find('a', href = True)['href']))               )  else 0 )
        print(links)
        URL = links[0] if links[0] != 0 else "None"
        URL = links[1] if (links[1] != 0  and links[0] == 0) else URL
        URL = links[2] if (links[2] != 0  and links[1] == 0 and links[0] == 0) else URL

        print( URL)


        return URL





#-------------------------------------------------------------------------------------------------------
def linkedin_scrape(URL, company_name,driver):

    if URL != 'None':

        company = company_name.lower().split()
        company = ('%20').join(company)
        driver.get("https://linkedin.com/uas/login")

        time.sleep(5)

        username = driver.find_element("id", "username")
        username.send_keys("rudrawrit.majumdar@stud.eah-jena.de") 
        pword = driver.find_element("id","password")
        pword.send_keys("abc#ABC0")
        driver.find_element("xpath","//button[@type='submit']").click()
    
        print(URL)

        #HOME page scraping
        driver.get(URL+"/home")
        scroll_down(driver)

        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')


        info = soup.find('div', {'class': 'mb4'})

        basic_info = soup.find_all('div', {'class': 'org-top-card-summary-info-list__info-item'})

        basics = []
        for basic in basic_info:
            basics.append(basic.text.strip())
        followers = basics[2] if len(basics) >= 3 else "Not Available"
        

        No_of_investors_Total_hcg_time = soup.find_all('p', {'class': 't-14 t-black--light'} )
        p_tags = []
        for p_tag in No_of_investors_Total_hcg_time:
            p_tags.append(p_tag.text.strip())
        
    
        No_of_investors = p_tags[0]  if (len(p_tags) != 0) else "Not Available"
        
        Total_head_count_growth_Median_tenure = soup.find_all('span', {'class': 't-24 v-align-middle'} )
        span_tags = []
        for span_tag in Total_head_count_growth_Median_tenure:
            span_tags.append(span_tag.text.strip())

        Total_head_count_growth = span_tags[0] if len(span_tags) != 0 else "Not Available"
        Median_tenure = span_tags[1] if (len(span_tags)>=1) else "Not Available"

        hires = soup.find('div', {'class': 't-bold t-16 t-black'} ).text.strip() if (soup.find('div', {'class': 't-bold t-16 t-black'} ) != None) else "Not Available"
       

        #ABOUT page scraping
        driver.get(URL+"/about/")
        scroll_down(driver)

        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        Company_size = soup.find('dd', {'class': 'text-body-small t-black--light mb1'} ).text.strip() if (soup.find('dd', {'class': 'text-body-small t-black--light mb1'} ) != None) else "Not Available"
        No_of_employees_linkedin = soup.find('dd', {'class': 'text-body-small t-black--light mb4'} ).text.strip().split()[0]  if (soup.find('dd', {'class': 'text-body-small t-black--light mb4'}) != None) else "Not Available"


        #POSTs page scraping
        driver.get(URL+"/posts/")
        scroll_down(driver)

        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        raw_posts = soup.find_all('span', {'class': 'break-words'})
        raw_post_div = soup.find_all('div', {'class': 'feed-shared-actor__meta relative'})

        posts = []
        for post in raw_posts:
            posts.append(post.text.strip())
            
        posts = posts[5:]

        post_dates = []
        for post_date in raw_post_div:
            post_dates.append(post_date.find('span', {'class': 'visually-hidden'}).text.strip())



        #Posts from other sources scraping
        driver.get("https://www.linkedin.com/search/results/content/?keywords="+company+"&origin=SWITCH_SEARCH_VERTICAL&position=1&searchId=dbb63914-db32-48c3-9036-22bcb989731f&sid=A5%3B")
        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        raw_posts2 = soup.find_all('span', {'class': 'break-words'})
        raw_post_div2 = soup.find_all('div', {'class': 'feed-shared-actor__meta relative'})
      
        posts2 = []
        for post2 in raw_posts2:
            posts2.append(post2.text.strip())
            
        posts2 = posts2[5:]
        post_dates2 = []
        for post_date2 in raw_post_div2:
            post_dates2.append(post_date2.find('span', {'class': 'visually-hidden'}).text.strip())
        
    else:
        followers = 'None'
        Company_size = 'None'
        No_of_employees_linkedin = 'None'
        No_of_investors = 'None'
        Total_head_count_growth = 'None'
        Median_tenure = 'None'
        hires = 'None'
        posts = 'None'
        post_dates = 'None'
        posts2 = 'None'
        post_dates2 = 'None'



    
    return followers, Company_size, No_of_employees_linkedin, No_of_investors, Total_head_count_growth, Median_tenure, hires, posts, post_dates,posts2, post_dates2



#-------------------------------------------------------------------------------------------------------


def google_finance_scrape(company_name,driver):
# Google Scraping to check if google finance data exists for the Company, if yes, grab the link
        company = []
        company = company_name.lower().split()
        company = ('+').join(company)+'+'+'google'+'+'+'finance'

        driver.get("https://www.google.com/search?q="+company+"&oq="+company+"&aqs=chrome..69i57j0i19i22i30l7.7380j0j15&sourceid=chrome&ie=UTF-8")

        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        google_link_div = soup.find_all('div', {'class':'yuRUbf'})

        links = []

        for div in google_link_div:
            links.append(div.find('a', href = True)['href'] if set(['www.google.com', 'finance', 'quote']).issubset(div.find('a', href = True)['href'].split('/')) else 0 )

        link = links[0] if links[0] != 0 else "None"


        #Enter Google Finace page
        if(link != 'None'):
                driver.get(link)

                scroll_down(driver)
                src = driver.page_source
                driver.find_element("xpath","//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']").click()
                scroll_down(driver)
                src = driver.page_source
                soup = BeautifulSoup(src, 'lxml')
                news__ = soup.find_all('div', {'class':'Yfwt5'})
                current_USD = soup.find('div', {'class':'YMlKec fxKbKc'}).get_text()
                interest_table = soup.find('table', {'class':'slpEwd'})
                interest_table2 = soup.find_all('table', {'class':'slpEwd'})[2]


                actuals = interest_table.find_all('tr',{'class':'roXhBd'})[1:]
                actuals2 = interest_table2.find_all('tr',{'class':'roXhBd'})[1:]


                Q_value = []
                Y_Y_change = []

                Q_value2 = []
                Y_Y_change2 = []

                for row in actuals:
                    Q_value.append(row.find('td', {'class': 'QXDnM'}).get_text())
                    Y_Y_change.append(row.find('td', {'class': 'gEUVJe'}).get_text())

                for row2 in actuals2:
                    Q_value2.append(row2.find('td', {'class': 'QXDnM'}).get_text())
                    Y_Y_change2.append(row2.find('td', {'class': 'gEUVJe'}).get_text())


                news = []
                for row in news__:
                    news.append(row.get_text())

        current_USD = current_USD if link != 'None' else 'None'
        q_revenue = Q_value[0] if link != 'None' else 'None'
        y_y_revenue = Y_Y_change[0] if link != 'None' else 'None'
        q_operating_expense = Q_value[1] if link != 'None' else 'None'
        y_y_operating_expense = Y_Y_change[1] if link != 'None' else 'None'
        q_net_income = Q_value[2] if link != 'None' else 'None'
        y_y_net_income = Y_Y_change[2] if link != 'None' else 'None'
        q_net_profit_margin = Q_value[3] if link != 'None' else 'None'
        y_y_net_profit_margin = Y_Y_change[3] if link != 'None' else 'None'
        q_earnings_per_share = Q_value[4] if link != 'None' else 'None'
        y_y_earnings_per_share = Y_Y_change[4] if link != 'None' else 'None'
        q_ebitda = Q_value[5] if link != 'None' else 'None'
        y_y_ebitda = Y_Y_change[5] if link != 'None' else 'None'
        q_effective_tax_rate = Q_value[6] if link != 'None' else 'None'
        y_y_effective_tax_rate = Y_Y_change[6] if link != 'None' else 'None'
        q_net_profit = Q_value2[0] if link != 'None' else 'None'
        y_y_net_profit = Y_Y_change2[0] if link != 'None' else 'None'
        q_operating_cash_flow = Q_value2[1] if link != 'None' else 'None'
        y_y_operating_cash_flow = Y_Y_change2[1] if link != 'None' else 'None'
        news = news if link != 'None' else 'None'
        return current_USD, q_revenue, y_y_revenue,q_operating_expense,y_y_operating_expense,q_net_income,y_y_net_income,q_net_profit_margin,y_y_net_profit_margin,q_earnings_per_share,y_y_earnings_per_share,q_ebitda,y_y_ebitda,q_effective_tax_rate,y_y_effective_tax_rate,q_net_profit,y_y_net_profit,q_operating_cash_flow,y_y_operating_cash_flow,news
        
#-------------------------------------------------------------------------------------------------------
# Google Scraping to check if CSR Hub exists for the Company, if yes, grab the link

def CSR_Hub_Scrape(comp,driver):
        
        company = comp.lower().split()
        company = ('+').join(company)+'+'+'csr'+'+'+'hub'
        driver.get("https://www.google.com/search?q="+company+"&rlz=1C1YTUH_enDE999DE999&oq="+company+"&aqs=chrome..69i57j0i546l2j69i60.3259j0j15&sourceid=chrome&ie=UTF-8")
        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        google_link_div = soup.find_all('div', {'class':'yuRUbf'})

        links__ = []
        links = []
        for div in google_link_div:
            links.append(div.find('a', href = True)['href'] if set(['www.csrhub.com', 'CSR_and_sustainability_information',comp.split(' ')[0].capitalize() ]).issubset(re.split('/|-',(div.find('a', href = True)['href']))) else 0 )
        link = links[0] if links[0] != 0 else 'None'
            

        #Enter CSR Hub page
        if (link != 'None'):
                driver.get(link+'/ESG_news')

                scroll_down(driver)
                src = driver.page_source
                soup = BeautifulSoup(src, 'lxml')
                ESG_news = soup.find_all('p', {'class':'bwalignc'})
                news = []

                for row in ESG_news:
                    news.append(row.get_text())
        else:
            news = 'None'

        return news


#World NEWS Scraping:
def news_media(company,city,driver):
        #BBC NEWS
        
        driver.get("https://www.bbc.com/news/world")
        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        head_line_live = soup.find('h3', {'class':'gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text'})
        head_line_links = soup.find_all('h3', {'class':'gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text'})
        latest_updates = soup.find_all('span', {'class':'lx-stream-post__header-text gs-u-align-middle'})
        bullet = soup.find_all('span', {'class':'nw-c-related-items__text gs-u-align-bottom'})

        headlines_bbc = []
        updates = []
        bullets = []
        for item1 in head_line_links:
            headlines_bbc.append(item1.get_text())


        for item2 in latest_updates:
            updates.append(item2.get_text())

        for item3 in bullets:
            bullets.append(item3.get_text())


        headlines_bbc.extend(updates)
        headlines_bbc.extend(bullets)
        headlines_bbc = list(set(headlines_bbc))

        #Google NEWS
        '''driver.get("https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en")
        scroll_down(driver)
        src = driver.page_source
        #driver.find_element("xpath","//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']").click()
        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        head_line_google = soup.find_all('h3', {'class':'ipQwMb ekueJc RD0gLb'})
        detailed_lines_google = soup.find_all('a', {'class':'DY5T1d RZIKme'})
        headlines_google = []
        detailedlines_google = []
        for content in head_line_google:
            headlines_google.append(content.get_text())

        for content in detailed_lines_google:
            detailedlines_google.append(content.get_text())

        headlines_google.extend(detailedlines_google)
        headlines_google = list(set(headlines_google ))'''

        #CNN NEWS
        driver.get("https://edition.cnn.com/")
        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        head_lines_CNN = soup.find_all('span', {'class':'cd__headline-text vid-left-enabled'})

        headlines_CNN = []

        for content in head_lines_CNN:
            headlines_CNN.append(content.get_text())
        headlines_CNN = list(set(headlines_CNN))


        headlines = []
        headlines.extend(headlines_bbc)
        #headlines.extend(headlines_google)
        headlines.extend(headlines_CNN)



        #Specific news

        company_1 = company.lower().split()
        company_1 = ('+').join(company_1)
        city = city.lower()
        geolocator = Nominatim(user_agent = "geoapiExercises")
        location = str(geolocator.geocode(city)).split(',')
        new_location = []
        translator = Translator()
        for loc in location:
            new_location.append(translator.translate(loc).text)

      
        country = new_location[-1].lower()

        driver.get("https://www.google.com/search?q="+company_1+"+"+city+"+"+country+"&client=firefox-b-d&biw=1920&bih=1032&tbm=nws&ei=pisbY-zFD6KExc8PjIar-AU&ved=0ahUKEwjssKa21Yf6AhUiQvEDHQzDCl8Q4dUDCAw&uact=5&oq=rocket+factory+augsburg+augsburg+germany&gs_lcp=Cgxnd3Mtd2l6LW5ld3MQAzIFCAAQogQyBwgAEB4QogQ6BQgAEJECOgUIABCABDoECAAQQzoGCAAQHhAWOgQIABANOgUIIRCgAToICCEQHhAWEB06CgghEB4QDxAWEB06BAghEBU6BQgAEIYDOgYIABAeEA1Q-nxY26kCYJCsAmgIcAB4AIABeogBlxqSAQQ0Ni4ymAEAoAEBsAEAwAEB&sclient=gws-wiz-news")
        scroll_down(driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')

        head_lines_specific = soup.find_all('div', {'class':'mCBkyc y355M ynAwRc MBeuO nDgy9d'})

        headlines_specific = []

        for content in head_lines_specific:
            headlines_specific.append(content.get_text())
        headlines_specific = list(set(headlines_specific))

        headlines_translated = []
        for ht in headlines_specific:
            headlines_translated.append(translator.translate(ht).text)

        headlines.extend(headlines_translated)

       

        # 'basic' search for issues from the news:
        company = company.lower()
        city = city.lower()
        geolocator = Nominatim(user_agent = "geoapiExercises")
        location = str(geolocator.geocode(city)).split(',')
        new_location = []
        translator = Translator()
        for loc in location:
            new_location.append(translator.translate(loc).text)

        state = new_location[-2].lower()
        country = new_location[-1].lower()
        search_list = [company,city,state,country, company+"'s",city+"'s",state+"'s", country+"'s"]
        print(search_list)
 

       
        issues = []
        count = 0
        for news in headlines:
            count = 0
            for element in search_list:
                if re.search(r'\b'+element+r'\b', news.lower()):
                    count = count + 1
                
            if count >= 1:
                issues.append(news)
            

        if len(issues) == 0:
            remark = "No current affairs affect this company at present."
        else:
            remark = "The company, city or country appeared in following news: "
            remark = remark + '\n' + '\n' + '\n'.join(issues)

        
        return headlines,remark,issues



#Ranking of companies begin here----------------------------------------------------------------------------------------------------------------------------------------------------------


df_excel = pd.read_excel('P:\Scrapper_suuplyChain\company_ranks.xlsx')
df_excel.reset_index(drop=True, inplace =True)
df_excel = df_excel.loc[:,'company':'date_time']


#df_excel = df_excel.rename(columns = { 1: 'company', 2: 'net_income', 3:'net_profit', 4:'quarterly_revenue', 5:'operating_cash_flow', 6:'total_head_count_growth', 7:'earning_per_share', 8:'operating_expense', 9:'net_profit_margin', 10:'median_tenure', 11:'number_of_employees', 12:'score'})
print(df_excel.head(50))
print("Please Enter the name of a company: ")
company_name = input()
print("Please enter the city: ")
city = input()
translator = Translator()
URL = basicInfo_scrape(company_name)
followers, Company_size, No_of_employees_linkedin, No_of_investors, Total_head_count_growth, Median_tenure, hires, posts, post_dates, posts2, post_dates2= linkedin_scrape(URL,company_name,driver)
current_USD, q_revenue, y_y_revenue,q_operating_expense,y_y_operating_expense,q_net_income,y_y_net_income,q_net_profit_margin,y_y_net_profit_margin,q_earnings_per_share,y_y_earnings_per_share,q_ebitda,y_y_ebitda,q_effective_tax_rate,y_y_effective_tax_rate,q_net_profit,y_y_net_profit,q_operating_cash_flow,y_y_operating_cash_flow,news = google_finance_scrape(company_name,driver)
ESG_news = CSR_Hub_Scrape(company_name,driver)
headlines,remarks,issues = news_media(company_name,city,driver)

df = pd.DataFrame(columns=['company','net_income','net_profit', 'quarterly_revenue', 'operating_cash_flow', 'total_head_count_growth', 'earning_per_share', 'operating_expense', 'net_profit_margin', 'median_tenure', 'number_of_employees', 'net_income_actual','net_profit_actual', 'quarterly_revenue_actual','operating_cash_flow_actual', 'score', 'flag', 'Overall_linkedIn_sentiment', 'news_issues', 'News_sentiment','date_time'])

y_y_net_income2 = y_y_net_income
y_y_net_profit2 = y_y_net_profit
y_y_revenue2 = y_y_revenue
y_y_operating_cash_flow2 = y_y_operating_cash_flow
df.at[0,'company'] = company_name.lower()
if  (y_y_net_income != 'Not Available' and y_y_net_income != 'None' and y_y_net_income != '—' ):
    y_y_net_income = y_y_net_income.replace(',', '.') if ',' in y_y_net_income else y_y_net_income
    df.at[0,'net_income'] = float(y_y_net_income.split('%')[0].split('.')[0] + '.' + y_y_net_income.split('%')[0].split('.')[1]) * 1.77
else:
    df.at[0,'net_income'] = 0

if (y_y_net_profit != 'Not Available' and y_y_net_profit != 'None' and y_y_net_profit != '—'):
    y_y_net_profit = y_y_net_profit.replace(',', '.') if ',' in y_y_net_profit else y_y_net_profit
    df.at[0,'net_profit'] = float(y_y_net_profit.split('%')[0].split('.')[0] + '.' + y_y_net_profit.split('%')[0].split('.')[1]) * 1.52
else:
    df.at[0,'net_profit'] = 0

if (y_y_revenue != 'Not Available' and y_y_revenue != 'None' and y_y_revenue != '—' ):
    print("--------------------------------------------------------------------------------------------------------------", y_y_revenue)
    y_y_revenue = y_y_revenue.replace(',', '.') if ',' in y_y_revenue else y_y_revenue
    df.at[0,'quarterly_revenue'] = float(y_y_revenue.split('%')[0].split('.')[0] + '.' + y_y_revenue.split('%')[0].split('.')[1]) * 1.52
else:
    df.at[0,'quarterly_revenue'] = 0

if (y_y_operating_cash_flow != 'Not Available' and y_y_operating_cash_flow != 'None' and y_y_operating_cash_flow != '—'):
    y_y_operating_cash_flow = y_y_operating_cash_flow.replace(',', '.') if ',' in y_y_operating_cash_flow else y_y_operating_cash_flow
    df.at[0,'operating_cash_flow'] = float(y_y_operating_cash_flow.split('%')[0].split('.')[0] + '.' + y_y_operating_cash_flow.split('%')[0].split('.')[1]) * 1.27 
else:
    df.at[0,'operating_cash_flow'] = 0

if (Total_head_count_growth != 'Not Available' and Total_head_count_growth != 'None'  and Total_head_count_growth != '—'):
    print(Total_head_count_growth)
    df.at[0,'total_head_count_growth'] = float(Total_head_count_growth.split('%')[0] ) * 1.25 
else:
    df.at[0,'total_head_count_growth'] = 0


if (y_y_earnings_per_share != 'Not Available' and y_y_earnings_per_share != 'None' and y_y_earnings_per_share != '—' ):
    y_y_earnings_per_share = y_y_earnings_per_share.replace(',', '.') if ',' in y_y_earnings_per_share else y_y_earnings_per_share
    df.at[0,'earning_per_share'] = float(y_y_earnings_per_share.split('%')[0].split('.')[0] + '.' + y_y_earnings_per_share.split('%')[0].split('.')[1]) * 1.02 
else:
    df.at[0,'earning_per_share'] = 0

if (y_y_operating_expense != 'Not Available' and y_y_operating_expense != 'None' and y_y_operating_expense != '—'):
    y_y_operating_expense = y_y_operating_expense.replace(',', '.') if ',' in y_y_operating_expense else y_y_operating_expense
    df.at[0,'operating_expense'] = float(y_y_operating_expense.split('%')[0].split('.')[0] + '.' + y_y_operating_expense.split('%')[0].split('.')[1]) * 0.77 
else:
    df.at[0,'operating_expense'] = 0

if (y_y_net_profit_margin != 'Not Available' and y_y_net_profit_margin != 'None' and y_y_net_profit_margin != '—'):
    y_y_net_profit_margin = y_y_net_profit_margin.replace(',', '.') if ',' in y_y_net_profit_margin else y_y_net_profit_margin
    df.at[0,'net_profit_margin'] = float(y_y_net_profit_margin.split('%')[0].split('.')[0] + '.' + y_y_net_profit_margin.split('%')[0].split('.')[1])  * 0.52 
else:
    df.at[0,'net_profit_margin'] = 0

if (Median_tenure != 'Not Available' and Median_tenure != 'None' and Median_tenure != '—' ):
    df.at[0,'median_tenure'] = float(Median_tenure.split('y')[0]) * 0.27 
else:
    df.at[0,'median_tenure'] = 0

if (No_of_employees_linkedin != 'Not Available' and No_of_employees_linkedin != 'None' and No_of_employees_linkedin != '—' ):
    df.at[0,'number_of_employees'] = ((df_excel['number_of_employees'].sum() + ((float(No_of_employees_linkedin.replace(',', '')) )  if ',' in No_of_employees_linkedin else (float(No_of_employees_linkedin) )) )/ df_excel['number_of_employees'].max()) * 0.07
else:
    df.at[0,'number_of_employees'] = 0

df['score'] = df.loc[:, 'net_income':'number_of_employees'].sum(axis = 1)

df.at[0,'net_income_actual'] = y_y_net_income
df.at[0,'net_profit_actual'] = y_y_net_profit
df.at[0,'quarterly_revenue_actual'] = y_y_revenue
df.at[0,'operating_cash_flow_actual'] = y_y_operating_cash_flow


y_y_net_income2 = y_y_net_income2.replace(',', '.') if ',' in y_y_net_income2 else y_y_net_income2
y_y_net_profit2 = y_y_net_profit2.replace(',', '.') if ',' in y_y_net_profit2 else y_y_net_profit2
y_y_revenue2 = y_y_revenue2.replace(',', '.') if ',' in y_y_revenue2 else y_y_revenue2
y_y_operating_cash_flow2 = y_y_operating_cash_flow2.replace(',', '.') if ',' in y_y_operating_cash_flow2 else y_y_operating_cash_flow2
if  (y_y_net_income2 != 'Not Available' and y_y_net_income2 != 'None' and y_y_net_income2 != '—' ):
    y_y_net_income2 = float(y_y_net_income2.split('%')[0].split('.')[0] + '.' + y_y_net_income2.split('%')[0].split('.')[1])
else:
    y_y_net_income2 = 0

if (y_y_net_profit2 != 'Not Available' and y_y_net_profit2 != 'None' and y_y_net_profit2 != '—'):
    y_y_net_profit2 = float(y_y_net_profit2.split('%')[0].split('.')[0] + '.' + y_y_net_profit2.split('%')[0].split('.')[1])
else:
    y_y_net_profit2 = 0

if (y_y_revenue2 != 'Not Available' and y_y_revenue2 != 'None'  and y_y_revenue2 != '—'):
    y_y_revenue2 = float(y_y_revenue2.split('%')[0].split('.')[0] + '.' + y_y_revenue2.split('%')[0].split('.')[1])
else:
    y_y_revenue2 = 0

if (y_y_operating_cash_flow2 != 'Not Available' and y_y_operating_cash_flow2 != 'None'  and y_y_operating_cash_flow2 != '—' ):
    y_y_operating_cash_flow2 = float(y_y_operating_cash_flow2.split('%')[0].split('.')[0] + '.' + y_y_operating_cash_flow2.split('%')[0].split('.')[1])
else:
    y_y_operating_cash_flow2 = 0

if( (y_y_net_income2 < 0 )  or (y_y_net_profit2 < 0 ) or (y_y_revenue2 < 0) or (y_y_operating_cash_flow2 < 0)):
       df.at[0,'flag'] = 'red'
elif((y_y_net_income2 == 0 ) and (y_y_net_profit2 == 0 ) and (y_y_operating_cash_flow2 == 0)):
       df.at[0,'flag'] = 'Z'
else:
    df.at[0,'flag'] = 'green'



#Sentiment Analysis of linkedin posts............................................................
if(len(posts2) != 0):
        senti_df = pd.DataFrame(columns=['review'])

        for index, post in zip( range(len(posts2)), posts2):
            senti_df.at[index,'review'] = translator.translate(post).text


        def clean(text):

            text = re.sub('[^A-Za-z]+', ' ', text)
            return text


        senti_df['Cleaned Reviews'] = senti_df['review'].apply(clean)


        pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

        def token_stop_pos(text):
            tags = pos_tag(word_tokenize(text))
            newlist = []
            for word, tag in tags:
                if word.lower() not in set(stopwords.words('english')):
                    newlist.append(tuple([word, pos_dict.get(tag[0])]))
            return newlist

        senti_df['POS tagged'] = senti_df['Cleaned Reviews'].apply(token_stop_pos)


        wordnet_lemmatizer = WordNetLemmatizer()
        def lemmatize(pos_data):
            lemma_rew = " "
            for word, pos in pos_data:
                if not pos:
                    lemma = word
                    lemma_rew = lemma_rew + " " + lemma
                else:
                    lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
                    lemma_rew = lemma_rew + " " + lemma
            return lemma_rew

        senti_df['Lemma'] = senti_df['POS tagged'].apply(lemmatize)


        analyzer = SentimentIntensityAnalyzer()

        def vadersentimentanalysis(review):
            vs = analyzer.polarity_scores(review)
            return vs['compound']
        senti_df['Vader Sentiment'] = senti_df['Lemma'].apply(vadersentimentanalysis)

        def vader_analysis(compound):
            if (compound >= 0.5 and posts2 != 'None'):
                return 'Positive'
            elif (compound <= -0.5 and posts2 != 'None'):
                return 'Negative'
            elif(compound > -0.5 and compound < 0.5 and posts2 != 'None'):
                return 'Neutral'
            else:
                return 'None'
        senti_df['Vader Analysis'] = senti_df['Vader Sentiment'].apply(vader_analysis)


        Neutral = senti_df.loc[senti_df['Vader Analysis']=='Neutral', 'Vader Analysis' ].count()
        Negative = senti_df.loc[senti_df['Vader Analysis']=='Negative', 'Vader Analysis' ].count()
        Positive = senti_df.loc[senti_df['Vader Analysis']=='Positive', 'Vader Analysis' ].count()

        if ((Neutral > Negative) and (Neutral > Positive)):
            print("-------------------------------------------------------------------------------------", Neutral)
            df.at[0, 'Overall_linkedIn_sentiment'] = 'Neutral'
        elif((Positive > Negative) and ( Positive > Neutral)):
            print("------------------------------------------------------------------------------------",Positive)
            df.at[0, 'Overall_linkedIn_sentiment'] = 'Positive'
        elif((Negative > Neutral) and ( Negative > Positive)):
            print("----------------------------------------------------------------------------------------",Negative)
            df.at[0, 'Overall_linkedIn_sentiment'] = 'Negative'
else:
    df.at[0, 'Overall_linkedIn_sentiment'] = 'Not available'






#News Analysis............................................................

dictionary = pd.read_excel("P:/Scrapper_suuplyChain/dictionary.xlsx")
all_news = pd.DataFrame()

issues.extend(ESG_news)

if (len(issues) != 0):

        for index, news in zip( range(len(issues)), issues):
            all_news.at[index,'news'] = translator.translate(news).text

        print(all_news.head(50))
        def clean(text):

            text = re.sub('[^A-Za-z]+', ' ', text)
            return text


        all_news['Cleaned_news'] = all_news['news'].apply(clean)
        print (all_news.head(50))

        pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

        def token_stop_pos(text):
            tags = pos_tag(word_tokenize(text))
            newlist = []
            for word, tag in tags:
                if word.lower() not in set(stopwords.words('english')):
                    newlist.append(tuple([word, pos_dict.get(tag[0])]))
            return newlist

        all_news['POS_tagged_news'] = all_news['Cleaned_news'].apply(token_stop_pos)

        wordnet_lemmatizer = WordNetLemmatizer()
        def lemmatize(pos_data):
            lemma_rew = " "
            for word, pos in pos_data:
                if not pos:
                    lemma = word
                    lemma_rew = lemma_rew + " " + lemma
                else:
                    lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
                    lemma_rew = lemma_rew + " " + lemma
            return lemma_rew

        all_news['Lemma_news'] = all_news['POS_tagged_news'].apply(lemmatize)


        print(all_news.head(50))
        all_news = all_news.drop(['news', 'POS_tagged_news'], axis=1)

        print(all_news.head(50))
        dictionary.columns = ['key1', 'key2', 'key3']
        dictionary.fillna('none', inplace = True)
        print(dictionary.head(50))
        news_issues = []
        for index, rows in all_news.iterrows():
            for index, row in dictionary.iterrows():
                if ((row['key1'] in rows['Lemma_news'].lower()) or (row['key2'] in rows['Lemma_news'].lower()) or (row['key3'] in rows['Lemma_news'].lower())):
                    news_issues.append(rows['Cleaned_news'])
                

        news_issues = list(set(news_issues))

        filtered_news = pd.DataFrame()

        for index, rows in zip( range(len(news_issues)), news_issues):
            filtered_news.at[index,'sentiments'] = rows
        
        print("------------------------------------------filtered_news----------------------------------------------------------")
        print(filtered_news)
        if(len(news_issues) != 0):
                def vader_analysis2(compound):
                    if (compound >= 0.5):
                        return 'Positive'
                    elif (compound <= -0.5):
                        return 'Negative'
                    elif(compound > -0.5 and compound < 0.5):
                        return 'Neutral'
                    else:
                        return 'None'

                filtered_news['Vader Sentiment'] = filtered_news['sentiments'].apply(vadersentimentanalysis)
                filtered_news['Vader Analysis'] = filtered_news['Vader Sentiment'].apply(vader_analysis2)

                Neutral_news = filtered_news.loc[filtered_news['Vader Analysis']=='Neutral', 'Vader Analysis' ].count()
                Negative_news = filtered_news.loc[filtered_news['Vader Analysis']=='Negative', 'Vader Analysis' ].count()
                Positive_news = filtered_news.loc[filtered_news['Vader Analysis']=='Positive', 'Vader Analysis' ].count()
                print('---------------Neutral news-------------------------', Neutral_news)
                print('---------------Negative news-------------------------', Negative_news)
                print('---------------Positive news-------------------------', Positive_news)

                if ((Neutral_news > Negative_news) and (Neutral_news > Positive_news)):
                    df.at[0, 'News_sentiment'] = 'Negative'
                elif((Positive_news > Negative_news) and ( Positive_news > Neutral_news)):
                    df.at[0, 'News_sentiment'] = 'Positive'
                elif((Negative_news > Neutral_news) and ( Negative_news > Positive_news)):
                    df.at[0, 'News_sentiment'] = 'Negative'
                else:
                    df.at[0, 'News_sentiment'] = 'could not interpret'
        else:
            df.at[0, 'News_sentiment'] = 'no issues found'

else:
    df.at[0, 'News_sentiment'] = 'News not available'


news_issues = ','.join(news_issues)
df.at[0, 'news_issues'] = news_issues
df.at[0,'date_time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(news_issues)

print(df_excel.head(50))

df_excel1 = pd.DataFrame()
df_excel2 = pd.DataFrame()
df_excel = pd.concat([df_excel,df], axis = 0)

df_excel1 = df_excel.loc[df_excel['flag'] == 'Z',:]

df_excel2 = df_excel.loc[df_excel['flag'] != 'Z', :]

df_excel2 = df_excel2.sort_values('score', ascending = False)
df_excel1 = df_excel1.sort_values('score', ascending = False)

df_excel = pd.concat([df_excel2, df_excel1], axis = 0)

df_excel.reset_index(drop = True, inplace=True)
df_excel.drop_duplicates(inplace = True)
df_excel.drop(0)
df = df[0:0]
df_excel.to_excel('P:\Scrapper_suuplyChain\company_ranks.xlsx')



#-----------------------------printing--------------------------------------------



'''print ('-------------------LinkedIN----------------------------------')
print("\n")
print( "Number of followers on linkedin: {0}".format(followers))

print("Company Size: {0}".format(Company_size))

print("Number of employees as per linkedin: {0}".format(No_of_employees_linkedin))

print("Number of investors till date: {0}".format(No_of_investors))

print ("Total head count growth is {0} in 6 months".format(Total_head_count_growth))

print("Median Tenure is: {0}".format(Median_tenure))

print("Hires: {0}".format(hires))
print("\n\n LINKEDIn POSTS: ")
for post, date in zip(posts,post_dates):

    print(translator.translate(post).text + " ({0})".format(date) )
    print("\n")

print("\n\n LINKEDIn POSTS By other sources: ")
translated_post2 = []
for post, date in zip(posts2,post_dates2):
    print(translator.translate(post).text + " ({0})".format(date) )
    print("\n")'''
    



'''print ('-------------------GOOGLE FINANCE----------------------------------')
print('Todays price: {0}'.format(current_USD))
print('The quarterly revinue is: {0} and Y/Y change: {1}'.format(q_revenue,y_y_revenue ))
print('The Operating expenses is: {0} and Y/Y change: {1}'.format(q_operating_expense,y_y_operating_expense))
print('The Net Income is: {0} and Y/Y change: {1}'.format(q_net_income, y_y_net_income))
print('The Net profit margin is: {0} and Y/Y change: {1}'.format(q_net_profit_margin,y_y_net_profit_margin))
print('The Earnings per share is: {0} and Y/Y change: {1}'.format(q_earnings_per_share,y_y_earnings_per_share))
print('The EBITDA is: {0} and Y/Y change: {1}'.format(q_ebitda,y_y_ebitda))
print('The Effective tax rate is: {0} and Y/Y change: {1}'.format(q_effective_tax_rate,y_y_effective_tax_rate))
print('The net profit is: {0} and Y/Y change: {1}'.format(q_net_profit,y_y_net_profit))
print('The operating cash flow is: {0} and Y/Y change: {1}'.format(q_operating_cash_flow,y_y_operating_cash_flow))
print("In the news: ")'''
'''for row in news:
    print(row)'''
    
'''print('-----------------------ESG NEWS---------------------------------------')
for row in ESG_news:
    print(row)'''

print('--------------------------Global News------------------------------------')

print('The lastes news headlines are: ')
for row in headlines:
    print(row)
    print('\n')

print('\n')
print('\n')
print(remarks)

print(issues)




