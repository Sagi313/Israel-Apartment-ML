# Israel Apartment Rental ML Project
#### By Lior Nissan & Sagi Buria

:bangbang:	:bangbang: **PLEASE NOTE THAT FULL INFO ON THE PROJECT CAN BE FOUND IN THE PTT UNDER THE MAIN BRANCH**	:bangbang:	:bangbang:	

## Introduction

#### Research question
Our goal was to predict the renting price of an apartment, based of its features. This is relevant for apartments located
in Israel.
We chose this subject out of a personal need. We are both at that stage in life where we are constantly looking for 
apartments, and we found, that understanding what is considered as a "good price" can be a very difficult task for those
who have no experience in that field. We hope that this project will help us (and maybe even others) find a good apartment
in a good price. :department_store:

[Link to Jupyter notebook](http://sagi313.github.io/Israel-Apartment-ML/docs/main.html)

## Data sources
using crawling and web-scraping techniques we managed to get records of 7,221 apartments that are listed for rent in Israel.

### Homeless :tent:
[Homeless web-scraper Jupyter Notebook](http://sagi313.github.io/Israel-Apartment-ML/docs/HomelessScraper.html)

We managed to get more than XXX records out of www.homeless.com, one of the biggest sites that provides listing for renting apartments.
Because each post in the site had its own web page with a serial number at the URL, it was easy to iterate the post numbers 
in order to scrape the data and analyze it.

### Yad2 :v:
[Yad2 crawler Jupyter Notebook](http://sagi313.github.io/Israel-Apartment-ML/docs/Yad2Scraper.html)

www.yad2.co.il is the biggest site in that field, with many relevant data for us. Getting the data out of Yad2 wasn't easy,
because they have a bot detection system, which blocks known bots signatures. Inorder to bypass this protection we used 
Selenium with an [undetectable Chrome driver](https://github.com/ultrafunkamsterdam/undetected-chromedriver). Although this
allowed us to access the site and get the HTML template. Because the site renders the HTML DOM of each post using JS, we 
had to crawl over each post, click on it to get the full HTML DOM, and then use the rendered template.

_Example of how the crawler work-_

![How the scraper work](scraper.gif)

## Summary


You can checkout the code for the project in the main branch of this repository :)
