import requests
from bs4 import BeautifulSoup

URL = input("Ссылка: ")
MinPrice = input("Минимальная цена: ")
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 YaBrowser/20.9.0.933 Yowser/2.5 Safari/537.36',
'accept':'*/*'}



def getPagesCount(html):
	soup = BeautifulSoup(html,'html.parser')
	pagination = soup.find_all('a',class_='block br3 brc8 large tdnone lheight24')
	if pagination:
		return int(pagination[-1].get_text())
	else:
		return 1
def getHtml(url, parm=None):
	r = requests.get(url, headers=HEADERS, params=parm)
	return r
def getCont(html):
	soup = BeautifulSoup(html,'html.parser') 
	items = soup.find_all('table',summary="Объявление")
	shops = []
	for item in items:
		try:
			price = int(item.find('p',class_="price").get_text().replace("тг.","").replace(" ","").replace("\n",""))
		except:
			price = -1
		if price>=int(MinPrice):
			href = item.find('a',class_="marginright5").get('href')
			title = item.find('a',class_="marginright5").get_text().replace("\n","")
			shops.append({
				'title':title,
				'price':price,
				'href':href
			})
	return shops

def parse():
	html = getHtml(URL)
	if html.status_code == 200:
		shops = []
		pages_count = getPagesCount(html.text)
		for page in range(1,pages_count+1):
			print(f'Пошла залупа страница: {page} из {pages_count}')
			html = getHtml(URL,parm={"page":page})
			shops.extend(getCont(html.text))
		print(len(shops))
		f = open("penis.html","w",encoding='utf-8')
		f.write("<table border=\"1\">")
		for item in shops:
			f.write(f"<tr><td>{str(item['title'])}</td><td><strong>{str(item['price'])}тг.</strong></td><td><a href=\"{str(item['href'])}\">ССЫЛКА</a></td></tr>")
		f.write("</table>")
	else:
		print("ЗАЛУПА АШЫБКА АШЫБКА КОД : "+html.status_code)

parse()
