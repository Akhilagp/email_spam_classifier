import sys
import requests
from bs4 import BeautifulSoup
import re
def scrape_blacklist_fun():
	url=[]
	lim=[]
	ur=[]
	with open('links.txt') as f:
		url=f.readlines()
	try:
		l=''
		for i in url[:-1]:	
			i=i.replace('\n','')
			page=requests.get(i)
			soup=BeautifulSoup(page.content,'lxml')
			table_b=soup.find('table').select('td')
			for i in table_b:
				s=(i.text).encode('utf-8').strip().lower()
				l=l+s+'\n'
		url_last=url[-1].replace('\n','')	
		page=requests.get(url_last)
		soup=BeautifulSoup(page.content,'lxml')
		table_b=soup.find('ul').select('li')
		for i in table_b:
	   		b=i.text.encode('utf-8').lower()
	   		b=re.sub(r'\[.*?\]','',b)
	   		b=re.sub(r'\(.*?\)','',b)
	   		b=b.replace('\n','').strip()
	   		l=l+b+'\n'
		ur=set(l.split('\n'))
		ur=list(ur)
		ur.sort()
		l=''
		with open('scrape1.txt','w') as f:
			for i in ur:
				l=l+i+'\n'
			f.write("{0}".format(l))
		return ("Successfully Scraped!", "Click the button for scraped content")
	except:
		return ("Error in connection!" ,"Click the button for previously scraped content")
	
def scrape_stopwords_fun():
	try:
		url="https://kb.yoast.com/kb/list-stop-words/"
		lim=[]
		ur=[]
		l=''
		page=requests.get(url)
		soup=BeautifulSoup(page.content,'lxml')
		table_b=soup.find('section',class_='index-list')
		table_b=table_b.select('li')
		for i in table_b:
			s=(i.text).encode('utf-8').strip().lower()
			l=l+s+'\n'
		ur=set(l.split('\n'))
		ur=list(ur)
		ur.sort()
		l=''
		with open('scrape2.txt','w') as f:
			for i in ur:
				l=l+i+'\n'
			f.write("{0}".format(l))
		return ("Successfully Scraped!", "Click the button for scraped content")
	except:
		return ("Error in connection!" ,"Click the button for previously scraped content")

