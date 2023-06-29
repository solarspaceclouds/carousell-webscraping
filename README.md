# carousell-webscraping

## Overview
### Product Search Listings Compilation
product_search.py provides an automated way to get the details of a particular search with the argument 'search_query'
#### Motivation for product search function: 
Searching through listings on carousell can be tedious and time-consuming for someone who prefers to view the details of many listings at once (without images filling up a large area of the screen). 

### Mylikes Listings Compilation
mylikes_scrape.py is an automated way to get the details of your liked items  (note: needs user to complete CAPTCHA verification in browser UI)
#### Motivation for mylikes listings compilation:
Mylikes section in Carousell doesn't provide a way for the user to search through the liked listings to find particular ones through filters/search queries. 

Details scraped include: product name, product price, product description and seller's carousell username, 

The output generated is a csv file. You can use it to filter the search results in ways that suit your needs. (filters which may not be offered by carousell app, e.g. sort by user name)

## To use:
python mylikes_scrape.py

python product_search.py --search_query <your search query>

## Example output
fresh_samples.csv # search queries with spaces work too
sulwhasoo.csv
mylikes_scrape.csv

On a personal note:
I started this project because I wanted to find a way to find good bargains for the products I'm interested in.
It was tedious to scroll through my likes every time i wanted to compare liked listings to decide on what to buy. 
