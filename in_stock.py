"""
This script verifies if a Book is available under the specified topic in http://books.toscrape.com/
"""

import re
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def get_topics():
    # variable to store website link as string
    HOME_URL = "http://books.toscrape.com/"    
    # grab website and store in variable uclient
    u_client = uReq(HOME_URL)
    # read and close HTML
    page_html = u_client.read()
    u_client.close()
    # call BeautifulSoup for parsing
    page_soup = soup(page_html, "html.parser")
    # grabs all the topics and URL under a dictionary                 
    topics_getting = page_soup.find_all('ul', {"class": "nav nav-list"})
    topics_getting = topics_getting[0].find_all('li')
    topics_getting.pop(0)
    topics_dict = {}
    for topic in topics_getting:
        key = topic.a.text.replace("\n","").strip().lower()
        topics_dict[key] = "https://books.toscrape.com/"+topic.a['href']
        
    return topics_dict
  
def get_books_from_page(url,pages_n):
    # grab website and store in variable uclient
    u_topic = uReq(url)
    # read and close HTML
    page_html = u_topic.read()
    u_topic.close()
    page_soup = soup(page_html, "html.parser")
    if pages_n > 1:
        # Change to next page
        # -get next page URL
        print(url)
        next_page_url = url
        # erase until "/"
        url_inv = url[::-1]
        #print(next_page_url2)
        for letter in url_inv:
            if letter == "/":
                break
            else:
                next_page_url = next_page_url[:-1]
        
        next_page_url = next_page_url + page_soup.find_all("li", {"class": "next"})[0].a["href"]
        print(next_page_url)
        # -recursivity
        book_list = get_books_from_page(next_page_url,pages_n-1)
        page_soup = soup(page_html, "html.parser")
        
    else:
        # -NO recursivity
        book_list = []        
    #("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    # Colecting books titles
    bookshelf = page_soup.find_all("article", {"class": "product_pod"})
    #print(bookshelf)
    for book in bookshelf:
        book_list.append(book.h3.a["title"].lower())
    #print(book_list)            
    return book_list  
  
def get_allbooks(url):    
    # grab website and store in variable uclient
    u_topic = uReq(url)    
    # read and close HTML
    page_html = u_topic.read()
    u_topic.close()    
    # call BeautifulSoup for parsing
    page_soup = soup(page_html, "html.parser")    
    # each page show 20 books
    # verifying if there is only one page
    books_n = page_soup.find_all("strong")
    #print(books_n)
    books_n = int(books_n[1].text)    
    #print(books_n)
    if books_n > 20:
        if books_n % 20 == 0:
            pages_n = int(books_n/20)
        else:
            pages_n = int(books_n//20+1)
            #print(pages_n)
    else:
        pages_n = 1
    books = get_books_from_page(url,pages_n)
    #print(len(books))
    return books

def in_stock(title, topic):
    topics_dict = get_topics()    
    #print(topics_dict)
    if topic.lower() in topics_dict.keys():
        #print(topics_dict[topic.lower()])
        book_list = get_allbooks(topics_dict[topic.lower()])
        #print(book_list)
        if title.lower() in book_list:
            print(f"{title} is available in {topic}")
            return True
        else:
            print(f"{title} is not available in {topic}")
            return False
        
    else:
        print(f"{title} is not available in {topic}")
        return False

if __name__ == "__main__":
    topic = input("In with topic is the book you are interested in?" )
    title = input("What is the title of the book you are interested in?")
    in_stock(title, topic)
