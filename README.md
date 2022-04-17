# Example of web_scrapin

This is a script designed to retrieve the main news of the newspapaer "La Repúlica"

The information that retrieves are:

- Titles
- Summary
- Body

Just run scraper.py to obtain a folder with the date and the news of that day.

## 04-17-2022 Update
New example added
### in_stock.py

This script tells you if a book is available, or not, under a specified topic on the webpage: http://books.toscrape.com/.

It works by following these steps::

1. Verify if the topic that was entered by the user is in the list
1. Retrieving a list of topics on the main page
1. If true, the script verifies the number of web pages for this topic. If false, the script returns False, prints a message on screen, and stops.
1. Then the script retrieves all books under that topic.
1. Check if the title entered by the user is in the list of books
1. If true, the script returns True, prints a message on screen, and stops.
1. If false, the script returns False, prints a message on screen, and stops.

The code has commented print for debugging purposes
