# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import itertools
from soupselect import select
from bs4 import BeautifulSoup
import re
import sys
import re 
import tweepy, time
import random
reload(sys)
sys.setdefaultencoding('utf-8')

url="http://press.unian.ua/announcement/"
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read(),"lxml")

#зчитування з сайту дату, назву, лінк, час публікації
title_data=soup.select('div.other_news span.title')
time_data=soup.select('div.other_news span.time')
date_link=soup.select('div.other_news span.date')
link_data=soup.select('div.other_news ul li a')


# full_dict словник, у якому ключ - лінк на статтю
full_dict = {"http://press.unian.ua"+a['href']: [] for a in link_data}

# список, що складається із словників. Словник має наступну структуру: ключ - лінк на базу псевдосоціолога, значення - список із усіма можливими варіантами запису пріхвища та ім*я 
fake_sociologists=[{'url': 'http://goo.gl/6i4K4g','keywords':["Радчук", "апро"]},{'url':"", 'keywords':["Бала Віталій","Віталій Бала","B. Бала","B.Бала","Бала B."]},{'url':"http://goo.gl/w8Cq2O", 'keywords':["Балюк Світлана","Світлана Балюк","C. Балюк","C.Балюк","Балюк C."]},{'url':"http://goo.gl/W2hwwR", 'keywords':["Бауман Юрій","Юрій Бауман","Ю. Бауман","Ю.Бауман","Бауман Ю."]},{'url':"http://goo.gl/r4m24U", 'keywords':["Берест Віктор","Віктор Берест","В. Берест","В.Берест","Берест В."]},{'url':"http://goo.gl/n8FV7W", 'keywords':["Бєлашко Сергій","Сергій Бєлашко","С. Бєлашко","С.Бєлашко","Бєлашко С."]},{'url':"http://goo.gl/40UdNQ", 'keywords':["Біловол Олексій","Олексій Біловол","О. Біловол","О.Біловол","Біловол О."]},{'url':"http://goo.gl/rKKA6U", 'keywords':["Бондаренко Володимир","Володимир Бондаренко","В. Бондаренко","В.Бондаренко","Бондаренко В."]},{'url':"http://goo.gl/Vrw47B", 'keywords':["Бондаренко Кость","Кость Бондаренко","К. Бондаренко","К.Бондаренко","Бондаренко К."]},{'url':"http://goo.gl/k0US0P", 'keywords':["Бузаров Андрій","Андрій Бузаров","А. Бузаров","А.Бузаров","Бузаров А."]},{'url':"http://goo.gl/zQqcsY", 'keywords':["Вигівський Сергій","Сергій Вигівський","Вигівський С.","С. Вигівський","С.Вигівський"]},{'url':"http://goo.gl/HBAL4U", 'keywords':["Вітмен Бернард","Бернард Вітмен","Вітмен Б.","Б. Вітмен","Б.Вітмен"]},{'url':"http://goo.gl/X4XKQp", 'keywords':["Воронцов Геннадій","Геннадій Воронцов","Воронцов Г.","Г. Воронцов","Г.Воронцов"]},{'url':"http://goo.gl/bpwjU2", 'keywords':["Голобуцький Олексій","Олексій Голобуцький","Голобуцький О.","О. Голобуцький","О.Голобуцький"]},{'url':"http://goo.gl/gr53YE", 'keywords':["Гончарук Валерій","Валерій Гончарук","Гончарук В.","В. Гончарук","В.Гончарук"]},{'url':"http://goo.gl/ZgPzlu", 'keywords':["Горбач Володимир","Володимир Горбач","Горбач В.","В. Горбач","В.Горбач"]},{'url':"http://goo.gl/mjkKPC", 'keywords':["Городецька Олена","Олена Городецька","Городецька О.","О. Городецька","О.Городецька"]},{'url':"http://goo.gl/U2G5xC", 'keywords':["Громаков Дмитро","Дмитро Громаков","Громаков Д.","Д. Громаков","Д.Громаков"]},{'url':"http://goo.gl/P0BdOu", 'keywords':["Данилюк Ростислав","Ростислав Данилюк","Данилюк Р.","Р. Данилюк","Р.Данилюк"]},{'url':"http://goo.gl/8Ix9cT", 'keywords':["Дем’янов Сергій","Сергій Дем’янов","Дем’янов С.","С. Дем’янов","С.Дем’янов"]},{'url':"http://goo.gl/f8ecsi", 'keywords':["Дементьєв Ігор","Ігор Дементьєв","Дементьєв І.","І. Дементьєв","І.Дементьєв"]},{'url':"http://goo.gl/vy8LXb", 'keywords':["Дзюба Олена","Олена Дзюба","Дзюба О.","О. Дзюба","О.Дзюба"]},{'url':"http://goo.gl/y5meQQ", 'keywords':["Дімсков В’ячеслав","В’ячеслав Дімсков","Дімсков В.","В. Дімсков","В.Дімсков"]},{'url':"http://goo.gl/MLbhwh", 'keywords':["Єременко Андрій","Андрій Єременко","Єременко А.","А. Єременко","А.Єременко"]},{'url':"http://goo.gl/329At4", 'keywords':["Житняк Юрій","Юрій Житняк","Житняк Ю.","Ю. Житняк","Ю.Житняк"]},{'url':"http://goo.gl/vKGsFj", 'keywords':["Загороднюк Валерій","Валерій Загороднюк","Загороднюк В.","В. Загороднюк","В.Загороднюк"]},{'url':"http://goo.gl/ZYwWcn", 'keywords':["Золотарьов Андрій","Андрій Золотарьов","Золотарьов А.","А. Золотарьов","А.Золотарьов"]},{'url':"http://goo.gl/VsRGRl", 'keywords':["Іванов В’ячеслав","В’ячеслав Іванов","Іванов В.","В. Іванов","В.Іванов"]},{'url':"http://goo.gl/gIIQrb", 'keywords':["Іващенко Олена","Олена Іващенко","Іващенко О.","О. Іващенко","О.Іващенко"]},{'url':"http://goo.gl/wY2nJX", 'keywords':["Камінник Ігор","Ігор Камінник","Камінник І.","І. Камінник","І.Камінник"]},{'url':"http://goo.gl/ajGtgD", 'keywords':["Карасьов Вадим","Вадим Карасьов","Карасьов В.","В. Карасьов","В.Карасьов"]},{'url':"http://goo.gl/civKx5", 'keywords':["Клаунінг Наталія","Наталія Клаунінг","Клаунінг Н.","Н. Клаунінг","Н.Клаунінг"]},{'url':"http://goo.gl/hIqiBT", 'keywords':["Коваленко Олена","Олена Коваленко","Коваленко О.","О. Коваленко","О.Коваленко"]},{'url':"http://goo.gl/D3lYV5", 'keywords':["Ковтун Олексій","Олексій Ковтун","Ковтун О.","О. Ковтун","О.Ковтун"]},{'url':"http://goo.gl/KCgKFu", 'keywords':["Корж Костянтин","Костянтин Корж","Корж К.","К. Корж","К.Корж"]},{'url':"http://goo.gl/8aPblQ", 'keywords':["Коровніченко Максим","Максим Коровніченко","Коровніченко М.","М. Коровніченко","М.Коровніченко"]},{'url':"http://goo.gl/qB7v2B", 'keywords':["Кузка Сергій","Сергій Кузка","Кузка С.","С. Кузка","С.Кузка"]},{'url':"http://goo.gl/dqvhez", 'keywords':["Кулик Віталій","Віталій Кулик","Кулик В.","В. Кулик","В.Кулик"]},{'url':"http://goo.gl/YTgVhH", 'keywords':["Кушнір Світлана","Світлана Кушнір","Кушнір С.","С. Кушнір","С.Кушнір"]},{'url':"http://goo.gl/s3rdE5", 'keywords':["Лапшин Віктор","Віктор Лапшин","Лапшин В.","В. Лапшин","В.Лапшин"]},{'url':"http://goo.gl/57q4hI", 'keywords':["Левицький Леонард","Леонард Левицький","Левицький Л.","Л. Левицький","Л.Левицький"]},{'url':"http://goo.gl/UI09qg", 'keywords':["Луків Геннадій","Геннадій Луків","Луків Г.","Г. Луків","Г.Луків"]},{'url':"http://goo.gl/4z4Ipf", 'keywords':["Лукінова Людмила","Людмила Лукінова","Лукінова Л.","Л. Лукінова","Л.Лукінова"]},{'url':"http://goo.gl/4116LK", 'keywords':["Лупова Тетяна","Тетяна Лупова","Лупова Т.","Т. Лупова","Т.Лупова"]},{'url':"http://goo.gl/cH9MtM", 'keywords':["Ляпкало Олександр","Олександр Ляпкало","Ляпкало О.","О. Ляпкало","О.Ляпкало"]},{'url':"http://goo.gl/NV0NFh", 'keywords':["Малєєв Костянтин","Костянтин Малєєв","Малєєв К.","К. Малєєв","К.Малєєв"]},{'url':"http://goo.gl/jrCJ3M", 'keywords':["Мартинюк Ігор","Ігор Мартинюк","Мартинюк І.","І. Мартинюк","І.Мартинюк"]},{'url':"http://goo.gl/2ZCrr8", 'keywords':["Марунич Дмитро","Дмитро Марунич","Марунич Д.","Д. Марунич","Д.Марунич"]},{'url':"http://goo.gl/8HSfux", 'keywords':["Михальченко Микола","Микола Михальченко","Михальченко М.","М. Михальченко","М.Михальченко"]},{'url':"http://goo.gl/y9PU8y", 'keywords':["Мішин Андрій","Андрій Мішин","Мішин А.","А. Мішин","А.Мішин"]},{'url':"http://goo.gl/w24huz", 'keywords':["Мороз Віталій","Віталій Мороз","Мороз В.","В. Мороз","В.Мороз"]},{'url':"http://goo.gl/IM26E1", 'keywords':["Павленко Руслан","Руслан Павленко","Павленко Р.","Р. Павленко","Р.Павленко"]},{'url':"http://goo.gl/SI01BP", 'keywords':["Павловський Ярослав","Ярослав Павловський","Павловський Я.","Я. Павловський","Я.Павловський"]},{'url':"http://goo.gl/mlP8bt", 'keywords':["Парахонська Олена","Олена Парахонська","Парахонська О.","О. Парахонська","О.Парахонська"]},{'url':"http://goo.gl/8fIAho", 'keywords':["Пащенко Віктор","Віктор Пащенко","Пащенко В.","В. Пащенко","В.Пащенко"]},{'url':"http://goo.gl/aJ258V", 'keywords':["Пиголенко Ігор","Ігор Пиголенко","Пиголенко І.","І. Пиголенко","І.Пиголенко"]},{'url':"http://goo.gl/sYCJBP", 'keywords':["Піньковський Володимир","Володимир Піньковський","Піньковський В.","В. Піньковський","В.Піньковський"]},{'url':"http://goo.gl/txabFE", 'keywords':["Позняк Майя","Майя Позняк","Позняк М.","М. Позняк","М.Позняк"]},{'url':"http://goo.gl/FLifAm", 'keywords':["Пом’яновський Ігор","Ігор Пом’яновський","Пом’яновський І.","І. Пом’яновський","І.Пом’яновський"]},{'url':"http://goo.gl/vObrHv", 'keywords':["Притула Михайло","Михайло Притула","Притула М.","М. Притула","М.Притула"]},{'url':"http://goo.gl/5ND9my", 'keywords':["Прокопенко Андрій","Андрій Прокопенко","Прокопенко А.","А. Прокопенко","А.Прокопенко"]},{'url':"http://goo.gl/aCsL2D", 'keywords':["Резнік Володимир","Володимир Резнік","Резнік В.","В. Резнік","В.Резнік"]},{'url':"http://goo.gl/qMnVYQ", 'keywords':["Сагалаков Борис","Борис Сагалаков","Сагалаков Б.","Б. Сагалаков","Б.Сагалаков"]},{'url':"http://goo.gl/kuKOdJ", 'keywords':["Синаюк Олег","Олег Синаюк","Синаюк О.","О. Синаюк","О.Синаюк"]},{'url':"http://goo.gl/Aw22fY", 'keywords':["Сірий Євген","Євген Сірий","Сірий Є.","Є. Сірий","Є.Сірий"]},{'url':"http://goo.gl/RCDfPr", 'keywords':["Слесаренко Юлія","Юлія Слесаренко","Слесаренко Ю.","Ю. Слесаренко","Ю.Слесаренко"]},{'url':"http://goo.gl/3G0eWF", 'keywords':["Стоякін Василь","Василь Стоякін","Стоякін В.","В. Стоякін","В.Стоякін"]},{'url':"http://goo.gl/tT79DS", 'keywords':["Ткач Руслан","Руслан Ткач","Ткач Р.","Р. Ткач","Р.Ткач"]},{'url':"http://goo.gl/dlPcil", 'keywords':["Тудвасєва Тамара","Тамара Тудвасєва","Тудвасєва Т.","Т. Тудвасєва","Т.Тудвасєва"]},{'url':"http://goo.gl/HRdIaz", 'keywords':["Фесенко Володимир","Володимир Фесенко","Фесенко В.","В. Фесенко","В.Фесенко"]},{'url':"http://goo.gl/8Qwv3T", 'keywords':["Фіщенко Дмитро","Дмитро Фіщенко","Фіщенко Д.","Д. Фіщенко","Д.Фіщенко"]},{'url':"http://goo.gl/weUM4q", 'keywords':["Хамітов Назіп","Назіп Хамітов","Хамітов Н.","Н. Хамітов","Н.Хамітов"]},{'url':"http://goo.gl/5Ylm3q", 'keywords':["Цибулько Володимир","Володимир Цибулько","Цибулько В.","В. Цибулько","В.Цибулько"]},{'url':"http://goo.gl/J5d5CR", 'keywords':["Цируль Павло","Павло Цируль","Цируль П.","П. Цируль","П.Цируль"]},{'url':"http://goo.gl/j7n3EB", 'keywords':["Черкасова Марія","Марія Черкасова","Черкасова М.","М. Черкасова","М.Черкасова"]},{'url':"http://goo.gl/Baf8kL", 'keywords':["Чигрин Віктор","Віктор Чигрин","Чигрин В.","В. Чигрин","В.Чигрин"]},{'url':"http://goo.gl/XDKqcE", 'keywords':["Чиркіна Ольга","Ольга Чиркіна","Чиркіна О.","О. Чиркіна","О.Чиркіна"]},{'url':"http://goo.gl/oznVkc", 'keywords':["Якубін Олексій","Олексій Якубін","Якубін О.","О. Якубін","О.Якубін"]},{'url':"http://goo.gl/m4Psza",'keywords':["Ярова Тетяна","Тетяна Ярова","Ярова Т.","Т. Ярова","Т.Ярова"]}]
#fake_sociologists=[{'url': 'ttp://texty.org.ua/d/тут ключ','keywords':["Майкл Амзель", "апро"]}]

# створення списків із датою, часом, повнотексту та списком, що влючає весь загадний перелік. 
list_with_time=[time.getText() for time in time_data]
list_of_full_news=[]
list_with_article=[]
list_with_title=[]
list_with_date=[]


# заповнення списку
for key in full_dict.keys():
	url=key 
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read(),"lxml")
	article_body=soup.select('div.article_body')
	for text_body in article_body:
		list_with_article.append(text_body.getText())

for key in full_dict.keys():
	url=key 
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read(),"lxml")
	date=soup.select('div.central_article span.date')
	for date_data in date:
		list_with_date.append(date_data.getText())

for key in full_dict.keys():
	url=key 
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read(),"lxml")
	title=soup.select('div.central_article h1')
	for title_data in title:
		list_with_title.append(title_data.getText())


# додавання до списку всіх атрибутів
for i in range(len(list_with_time)):
	news=[]
	news.append(list_with_date[i])
	news.append(list_with_time[i]) 
	news.append(list_with_title[i]) 
	news.append(list_with_article[i])
	list_of_full_news.append(news)
#print repr(list_of_full_news).decode("unicode_escape")


# додавання до словника список. результат: словник ключем-лінком, значення - список із атрибутами тексту 
n=0
for key in full_dict.keys():
	full_dict[key]=list_of_full_news[n]
	n+=1


#--find keywords.

file_for_=open('/media/mariia/Data/TEXTY/bot/file_with_massage.txt', 'r')
f=file_for_.readline()

search=u'Тарас Стецьків|Борисенко|Степан Хмара|Тудвасєва Тамара|Бала Віталій|Тримбач*|Радчук'
#search=u"Віталій Бала|Бала Віталій|В.Бала|Бала В.|В. Бала|Балюк С.|Cвітлана Балюк|C.Балюк|C. Балюк|Балюк Cвітлана|Бауман Юрій|Юрій Бауман|Ю.Бауман|Ю. Бауман| Бауман Ю.|Берест Віктор|Віктор Берест|Берест В.|В.Берест |В. Берест|Бєлашко Сергій|Бєлашко С.|С.Бєлашко |С. Бєлашко|Сергій Бєлашко|Біловол Олексій|О. Біловол|Біловол О.|Олексій Біловол|О.Біловол|Бондаренко Володимир|Бондаренко В.|В.Бондаренко|В. Бондаренко|Володимир Бондаренко|Бондаренко Кость|Бондаренко К.|К. Бондаренко|К. Бондаренко|Кость Бондаренко|Бузаров Андрій|Бузаров А.|А.Бузаров|А. Бузаров|Андрій Бузаров|Вигівський Сергій|Вітмен Бернард|Воронцов Геннадій|Голобуцький Олексій|Гончарук Валерій|Горбач Володимир|Городецька Олена|Громаков Дмитро|Данилюк Ростислав|Дем’янов Сергій|Дементьєв Ігор|Дзюба Олена|Дімсков В’ячеслав|Єременко Андрій|Житняк Юрій|Загороднюк Валерій|Золотарьов Андрій|Сергій Вигівський|Бернард Вітмен|Геннадій Воронцов|Олексій Голобуцький|Валерій Гончарук|Володимир Горбач|Олена Городецька|Дмитро Громаков|Ростислав Данилюк|Сергій Дем’янов|Ігор Дементьєв|Олена Дзюба|В’ячеслав Дімсков|Андрій Єременко|Юрій Житняк|Валерій Загороднюк|Андрій Золотарьов|Вигівський С.|Вітмен Б.|Воронцов Г.|Голобуцький О.|Гончарук В.|Горбач В.|Городецька О.|Громаков Д.|Данилюк Р.|Дем’янов С.|Дементьєв І.|Дзюба О.|Дімсков В.|Єременко А.|Житняк Ю.|Загороднюк В.|Золотарьов А.|С. Вигівський|Б. Вітмен|Г. Воронцов|О. Голобуцький|В. Гончарук|В. Горбач|О. Городецька|Д. Громаков|Р. Данилюк|С. Дем’янов|І. Дементьєв|О. Дзюба|В. Дімсков|А. Єременко|Ю. Житняк|В. Загороднюк|А. Золотарьов|С.Вигівський|Б.Вітмен|Г.Воронцов|О.Голобуцький|В.Гончарук|В.Горбач|О.Городецька|Д.Громаков|Р.Данилюк|С.Дем’янов|І.Дементьєв|О.Дзюба|В.Дімсков|А.Єременко|Ю.Житняк|В.Загороднюк|А.Золотарьов|Іванов В’ячеслав|Іващенко Олена|Камінник Ігор|Карасьов Вадим|Клаунінг Наталія|Коваленко Олена|Ковтун Олексій|Корж Костянтин|Коровніченко Максим|Кузка Сергій|Кулик Віталій|Кушнір Світлана|Лапшин Віктор|Левицький Леонард|Луків Геннадій|Лукінова Людмила|Лупова Тетяна|Ляпкало Олександр|Малєєв Костянтин|Мартинюк Ігор|Марунич Дмитро|Михальченко Микола|Мішин Андрій|Мороз Віталій|Павленко Руслан|Павловський Ярослав|Парахонська Олена|Пащенко Віктор|Пиголенко Ігор|Піньковський Володимир|Позняк Майя|Пом’яновський Ігор|Притула Михайло|Прокопенко Андрій|Резнік Володимир|Сагалаков Борис|Синаюк Олег|Сірий Євген|Слесаренко Юлія|Стоякін Василь|Ткач Руслан|Тудвасєва Тамара|Фесенко Володимир|Фіщенко Дмитро|Хамітов Назіп|Цибулько Володимир|Цируль Павло|Черкасова Марія|Чигрин Віктор|Чиркіна Ольга|Якубін Олексій|Ярова Тетяна|В’ячеслав Іванов|Олена Іващенко|Ігор Камінник|Вадим Карасьов|Наталія Клаунінг|Олена Коваленко|Олексій Ковтун|Костянтин Корж|Максим Коровніченко|Сергій Кузка|Віталій Кулик|Світлана Кушнір|Віктор Лапшин|Леонард Левицький|Геннадій Луків|Людмила Лукінова|Тетяна Лупова|Олександр Ляпкало|Костянтин Малєєв|Ігор Мартинюк|Дмитро Марунич|Микола Михальченко|Андрій Мішин|Віталій Мороз|Руслан Павленко|Ярослав Павловський|Олена Парахонська|Віктор Пащенко|Ігор Пиголенко|Володимир Піньковський|Майя Позняк|Ігор Пом’яновський|Михайло Притула|Андрій Прокопенко|Володимир Резнік|Борис Сагалаков|Олег Синаюк|Євген Сірий|Юлія Слесаренко|Василь Стоякін|Руслан Ткач|Тамара Тудвасєва|Володимир Фесенко|Дмитро Фіщенко|Назіп Хамітов|Володимир Цибулько|Павло Цируль|Марія Черкасова|Віктор Чигрин|Ольга Чиркіна|Олексій Якубін|Тетяна Ярова|В. Іванов|О. Іващенко|І. Камінник|В. Карасьов|Н. Клаунінг|О. Коваленко|О. Ковтун|К. Корж|М. Коровніченко|С. Кузка|В. Кулик|С. Кушнір|В. Лапшин|Л. Левицький|Г. Луків|Л. Лукінова|Т. Лупова|О. Ляпкало|К. Малєєв|І. Мартинюк|Д. Марунич|М. Михальченко|А. Мішин|В. Мороз|Р. Павленко|Я. Павловський|О. Парахонська|В. Пащенко|І. Пиголенко|В. Піньковський|М. Позняк|І. Пом’яновський|М. Притула|А. Прокопенко|В. Резнік|Б. Сагалаков|О. Синаюк|Є. Сірий|Ю. Слесаренко|В. Стоякін|Р. Ткач|Т. Тудвасєва|В. Фесенко|Д. Фіщенко|Н. Хамітов|В. Цибулько|П. Цируль|М. Черкасова|В. Чигрин|О. Чиркіна|О. Якубін|Т. Ярова|Іванов В.|Іващенко О.|Камінник І.|Карасьов В.|Клаунінг Н.|Коваленко О.|Ковтун О.|Корж К.|Коровніченко М.|Кузка С.|Кулик В.|Кушнір С.|Лапшин В.|Левицький Л.|Луків Г.|Лукінова Л.|Лупова Т.|Ляпкало О.|Малєєв К.|Мартинюк І.|Марунич Д.|Михальченко М.|Мішин А.|Мороз В.|Павленко Р.|Павловський Я.|Парахонська О.|Пащенко В.|Пиголенко І.|Піньковський В.|Позняк М.|Пом’яновський І.|Притула М.|Прокопенко А.|Резнік В.|Сагалаков Б.|Синаюк О.|Сірий Є.|Слесаренко Ю.|Стоякін В.|Ткач Р.|Тудвасєва Т.|Фесенко В.|Фіщенко Д.|Хамітов Н.|Цибулько В.|Цируль П.|Черкасова М.|Чигрин В.|Чиркіна О.|Якубін О.|Ярова Т.|В.Іванов|О.Іващенко|І.Камінник|В.Карасьов|Н.Клаунінг|О.Коваленко|О.Ковтун|К.Корж|М.Коровніченко|С.Кузка|В.Кулик|С.Кушнір|В.Лапшин|Л.Левицький|Г.Луків|Л.Лукінова|Т.Лупова|О.Ляпкало|К.Малєєв|І.Мартинюк|Д.Марунич|М.Михальченко|А.Мішин|В.Мороз|Р.Павленко|Я.Павловський|О.Парахонська|В.Пащенко|І.Пиголенко|В.Піньковський|М.Позняк|І.Пом’яновський|М.Притула|А.Прокопенко|В.Резнік|Б.Сагалаков|О.Синаюк|Є.Сірий|Ю.Слесаренко|В.Стоякін|Р.Ткач|Т.Тудвасєва|В.Фесенко|Д.Фіщенко|Н.Хамітов|В.Цибулько|П.Цируль|М.Черкасова|В.Чигрин|О.Чиркіна|О.Якубін|Т.Ярова"


# у значені словника шукає ключові слова, якщо знайдені формує повідомлення, яке рамдомно вибирається зі списку і записує у файл 
for key, value in full_dict.items():
	str_value=','.join(value).decode('utf-8')
	find_word=set(re.findall(search,str_value))
	if len(find_word)!=0:
		str_fw=' '.join(find_word)
		for dict_fs in fake_sociologists:
			if dict_fs['keywords']:
				str_key=','.join(dict_fs['keywords']).decode('utf-8')
				fw=re.findall(str_fw,str_key)
				if len(fw)!=0:
					link_texty=dict_fs['url'].decode('utf-8')
					tems=[[ur'Фігурант бази псевдосоціологів', str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n'],[ur'Псевдосоціолог', str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n']]
					items=[[ur'Фігурант бази псевдосоціологів', str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n'],[ur'Псевдосоціолог', str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n'],[ur'"Соціолог"', str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n'],[ur'Фальшивий соціолог', str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n'],[value[0], ur'o', value[1], ur' виступить в УНІАН', ur'фальшивий соціолог', str_fw, ur'Деталі про особу: ', link_texty, '\n'], [value[0], ur'o', value[1], ur' виступить в УНІАН', ur'фігурант бази псевдосоціологів', str_fw, ur'Деталі про особу: ', link_texty, '\n'],[value[0], ur'o', value[1], ur' виступить в УНІАН', ur'псевдосоціолог', str_fw, ur'Деталі про особу: ', link_texty, '\n'],[value[0], ur'o', value[1],ur' виступить в УНІАН', ur'"Соціолог"', str_fw, ur'Деталі про особу: ', link_texty, '\n'],[ur'B УНІАН o', value[1],ur', ',value[0], ur'виступить фальшивий соціолог', str_fw, ur'Деталі про особу: ', link_texty, '\n'], [ur'B УНІАН o', value[1],ur', ',value[0], ur'виступить фігурант бази псевдосоціологів', str_fw, ur'Деталі про особу: ', link_texty, '\n'], [ur'B УНІАН o', value[1],ur', ',value[0], ur'виступить "соціолог"', str_fw, ur'Деталі про особу: ', link_texty, '\n'], [ur'B УНІАН o', value[1],ur', ',value[0], ur'виступить псевдосоціолог', str_fw, ur'Деталі про особу: ', link_texty, '\n']]
					message = items[random.randrange(len(items))]
					print message
					msg=repr(message).decode("unicode_escape")
					#message=[rand_item, str_fw,  ur' виступить в УНІАН о ', value[1],ur', ',value[0], ur'Деталі про особу: ', link_texty, '\n' ]
					
					#msg=repr(message).decode("unicode_escape")
					print msg
					str_message=''.join(message)
					str_message1=str(str_message)
					file_for_message=open('/media/mariia/Data/TEXTY/bot/file_with_massage.txt', 'w')
					if f==str_message1:
						space=''
						file_for_message.write (space)
					else:
						file_for_message.write (str_message1)					
					file_for_message.close()


# твітить записане повідомлення у файл 

CONSUMER_KEY ='qMqBdVBC9eHVuW38CFL6AOp07'
CONSUMER_SECRET ='7N4IPZAYt5dl5shaJc837SWmRHTeGJs2cmzi46S5fS25HvJSmR'

ACCESS_KEY='700665188702289921-K5SqBYmRiR4N9f3YpdhxAUfafjBMmgk'
ACCESS_SECRET='a8jlHkrHsGK5cDRRZm6bXUyYObUWsv18wbRcDmWVQA5GD'



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api=tweepy.API(auth)
#line='Hello world 4!'#api.update_status(line)

filename=open('/media/mariia/Data/TEXTY/bot/file_with_massage.txt', 'r')
f=filename.readlines()
filename.close()

for line in f:
	api.update_status(line)


