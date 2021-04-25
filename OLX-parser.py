import requests
from bs4 import BeautifulSoup
print("OLX-parser    |    Специально для Данила)\n\n")
URL =input("Ссылка / Название : ")
is_URL=True

head = {
	'authorization': "Bearer 633212cabb11c349924e6fca40a6f5ec104954e2"
}
def getPagesCount(html):
	soup = BeautifulSoup(html,'html.parser')
	pagination = soup.find_all('a',class_='block br3 brc8 large tdnone lheight24')
	if pagination:
		return int(pagination[-1].get_text())
	else:
		return 1

def getId(rq):
	req = requests.get(rq)
	soup = BeautifulSoup(req.text,'html.parser')
	# print(soup)
	href= soup.find('div', class_="clm-samurai").get("data-item")
	print(href)
	return href

def getPhone(id,hd):
	try:
		r = requests.get(f"https://www.olx.kz/api/v1/offers/{id}/phones/", headers = hd)
		return r.json()['data']['phones'][0].replace(' ','').replace('+','')
	except:
		return 'не найден'

def checkSearch(URll):
	soup = BeautifulSoup(requests.get(URll).text,'html.parser')
	try:
		check = soup.find('span',class_='marker').get_text()
		if check == "Проверьте правильность написания или введите другие параметры поиска":
			return True
	except:
		return False

if URL == "":
	URL = "https://www.olx.kz/list/"
	is_URL=True
	print(f"Вы ничего не ввели, ссылка автоматически выставлена https://www.olx.kz/list/")

elif "olx.kz" in URL:
	is_URL=True

else:
	is_URL=False
	URL = f"https://www.olx.kz/list/q-{URL}/"


if checkSearch(URL):
	print("По запросу ничего не найдено, ссылка автоматически выставлена https://www.olx.kz/list/")
	URL = "https://www.olx.kz/list/"

allPages = getPagesCount(requests.get(URL).text)
print(f'Обнаружено {allPages} страниц, сколько парсить: ')
pages_input =input("Кол-во страниц: ")

if pages_input.isdigit():
	pages_input=int(pages_input)
	if pages_input >allPages:
		print(f"Вы ввели {pages_input} страниц(у), автоматически переведено на {allPages}")
		pages_input = allPages
		
	if pages_input <1:
		print(f"Вы ввели {pages_input} страниц(у), автоматически переведено на 1")
		pages_input = 1
		

elif not pages_input.isdigit():
	pages_input = 1
	print(f"Вы ввели либо ничего, либо ввели некорректно, автоматически переведено на 1")

isurl="ссылка" if is_URL else "Название"
print(f"\n\nПарсинг {URL}({isurl})")

def getCont(html):
	soup = BeautifulSoup(html,'html.parser')
	items = soup.find_all('table',summary="Объявление") 
	shops = []
	for item in items:
		if item.find('small',class_="breadcrumb breadcrumb--job-type x-normal"):
			break
		try:
			price = item.find('p',class_="price").get_text()
		except:
			price = "договорная"
		href = item.find('a',class_="marginright5").get('href')
		title = item.find('a',class_="marginright5").get_text().replace("\n","")
		adress= item.find_all('small',class_="breadcrumb x-normal")[1].get_text()
		aueId = getId(href)
		number = getPhone(aueId,head)
		shops.append({'title':title, 'price':price ,'adress':adress,'href':href , 'number': number})
	return shops

def parse():
	shops = []
	pages_count=int(pages_input)
	if pages_count > allPages:
		pages_count= allPages
		print(f"Найдено всего {allPages} страниц, автоматически изменено.")
	for page in range(1,pages_count+1):
		print(f"Парсинг: {page-1} из {pages_count} страниц")
		html = requests.get(URL,params={"page":page})

		shops.extend(getCont(html.text))
	print(f"Найдено {len(shops)} результатов")
	f = open("результат.html","w",encoding='utf-8')
	f.write("<table border=\"1\">")
	f.write(f"<tr><td><strong>ID</strong></td><td align=\"center\"><strong>НАЗВАНИЕ | ССЫЛКА</strong></td><td align=\"center\" ><strong>АДРЕС</strong></td><td align=\"center\"><strong>ЦЕНА(тенге)</strong></td><td align=\"center\"><strong>НОМЕР</strong></td></tr>")
	for item in shops:
		f.write(f"<tr><td>{shops.index(item)+1}</td><td><a href=\"{str(item['href'])}\">{str(item['title'])}</a></td><td>{str(item['adress'])}</td><td><strong>{str(item['price'])}</strong></td><td><strong>{str(item['number'])}</strong></td></tr>")
	f.write("</table>")
parse()
input("Завершено")