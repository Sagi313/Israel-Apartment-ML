# Israel Apartment Rental ML Project
#### By Lior Nissan & Sagi Buria

## Introduction

#### Research question
Our goal was to predict the renting price of an apartment, based of its features. This is relevant for apartments located
in Israel.
We chose this subject out of a personal need. We are both at that stage in life where we are constantly looking for 
apartments, and we found, that understanding what is considered as a "good price" can be a very difficult task for those
who have no experience in that field. We hope that this project will help us (and maybe even others) find a good apartment
in a good price.

[Link to Jupyter notebook](http://sagi313.github.io/Israel-Apartment-ML/main-notebook.html)

## Data sources
using crawling and web-scraping techniques we managed to get records of XXX apartments that are listed for rent in Israel.

### Homeless
(Homeless web-scraper Jupyter Notebook)[http://sagi313.github.io/Israel-Apartment-ML/homeless-notebook.html]

We managed to get more than XXX records out of www.homeless.com, one of the biggest sites that provides listing for renting apartments.
Because each post in the site had its own web page with a serial number at the URL, it was easy to iterate the post numbers 
in order to scrape the data and analyze it.

### Yad2 :v:
(Yad2 crawler Jupyter Notebook)[http://sagi313.github.io/Israel-Apartment-ML/yad2-notebook.html]

www.yad2.co.il is the biggest site in that field, with many relevant data for us. Getting the data out of Yad2 wasn't easy,
because they have a bot detection system, which blocks known bots signatures. Inorder to bypass this protection we used 
Selenium with an [undetectable Chrome driver](https://github.com/ultrafunkamsterdam/undetected-chromedriver). Although this
allowed us to access the site and get the HTML template. Because the site renders the HTML DOM of each post using JS, we 
had to crawl over each post, click on it to get the full HTML DOM, and then use the rendered template.

:v:

## Struggles and difficulties

## Summary