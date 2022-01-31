# To activate the venv use:
# source scraping/bin/activate

# To make HTTP requests
import requests
import lxml.html as html
# To crate a folder
import os
# To get the date
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="col mb-4"]/div/a[1]/@href'
# the response command, used latter, change h2 to text-fill
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
# | is for logic OR
# Here is needed because links are contained in <u> label inside <p> label
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()|//div[@class="html-content"]/p[not(@class)]/u/text()'

def parse_notice(link,today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                # ereasing \n
                body = [paragraps for paragraps in body if paragraps != '\n']
                # print(body)
            except IndexError:
                return

            # with es un manejador contextual de Python 
            # evita se corrompa un archivo si el scrip se cierra
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # decode transform especial symbols and letters like ñ 
            home = response.content.decode('utf-8')
            # fromstring transform into a file that can be used by XPath
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # Cleaning black spaces
            links_to_notices = [link for link in links_to_notices if link != '']
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%y')
            today = 'news/'+today
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
            
        else:
            raise ValueError(f'Error: {response.status_code}') 

    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()