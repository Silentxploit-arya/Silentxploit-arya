from concurrent.futures import ThreadPoolExecutor as work
import requests as req, os, re
from bs4 import BeautifulSoup as par
from time import sleep
saved = "grabext.txt"

class ExtDom(object):
	def __init__(self):
		self.tuple  = []
		self.header = {"user-agent": "chrome"}

	def GetOne(self):
		cek = par(req.get("https://www.greensiteinfo.com/domain_extensions/", headers=self.header).text, "html.parser")
		tbody = cek.find("tbody")
		for tr in tbody.find_all("td"):
			a_hr = tr.find("a")
			self.tuple.append([a_hr.get("href"), a_hr.text])
		return self.tuple

	def GetTwo(self):
		cek = par(req.get("https://www.topsitessearch.com/domains/", headers=self.header).text, "html.parser")
		findDiv = cek.findAll("div", {"class": "col-md-12 col-xs-12"})[-1]
		for yz in findDiv.find_all("a", {"class": "btn btn-secondary"}):
			getHr = yz.get("href")
			teks  = yz.find("strong").text
			self.tuple.append([getHr, teks])
		return self.tuple

def write(name, content):
	try:
		if content in str(open(name, "r").read()):
			pass
		else:
			open(name, "a+").write(content.replace("\n","")+"\n")
	except:
		open(name, "a+").write(content.replace("\n","")+"\n")

def backorder():
	ses = req.Session()
	cek = ses.get("https://www.dynadot.com/market/backorder/", headers={"user-agent": "chrome"})
	parser = par(cek.text, "html.parser")

	#-> find form post
	cekForm = parser.find("form", {"method": "post"})
	data, dataL = {}, []
	for inp in cekForm.find_all("input"):
		if inp.get("name") in ["keyword", "domain_list", "tld_search_keyword", "cc_invl_start", "cc_invl_end", "cc_exact", "order_by", "login-url", "abi", "pagesubmit", "page_jump_to", "cc_invl_start_xs", "cc_invl_end_xs", "cc_exact_xs"]:
			if "abi" in inp.get("name"):
				dataL.append(inp.get("value"))
			else:
				if inp.get("value") is None:
					data.update({inp.get("name"): ""})
				else:
					data.update({inp.get("name"): inp.get("value")})
		else:
			pass
	data.update({"abi": dataL, "page_size": "1000", "page_index": "0"})
	posted = par(ses.post("https://www.dynadot.com" + cekForm.get("action"), headers={"user-agent": "chrome"}, cookies=cek.cookies.get_dict(), data=data).text, "html.parser")
	num = 0
	for domain in posted.find_all("a", {"class": "link-domain-name"}):
		num += 1
		print("\r   [*] Collect "+str(num)+" domain ", end="")
		write(saved, domain.text)


def randomDomain():
	count = 0
	cek = par(req.get("https://siterankdata.com/show/detected/2017-07-23", headers={"user-agent": "chrome"}).text, "html.parser")
	if "404" in str(cek):
		print("\r [×] Domain not found, next proses.. ")
	else:
		try:
			while True:
				for h4 in cek.find_all("h4", {"class": "m-b-xs"}):
					count += 1
					domain = h4.find("a").text
					for x in list("\|/-"):
						print("\r   ["+x+"] Collect "+str(count)+" Domain.. ", end="")
						sleep(0.01)
					write(saved, domain)

				pagination = cek.find("ul", {"class": "pagination"})
				if "Next" in str(pagination):
					urla = pagination.find("a", string="Next").get("href")
					cek = par(req.get("https://siterankdata.com"+urla, headers={"user-agent": "chrome"}).text, "html.parser")
					continue
				else:
					break
		except KeyboardInterrupt:
			pass
	return True

def chusMenu():
	chus_one = ExtDom().GetOne()
	chus_two = ExtDom().GetTwo()
	add = {}
	for menu in chus_one:
		add.update({menu[-1].replace(".",""): menu[0]})
	for menu2 in chus_two:
		add.update({menu2[-1].replace(".",""): menu2[0]})
	return add


def SiteScraper(urls):
	cek = par(req.get(urls, headers={"user-agent": "chrome"}).text, "html.parser")
	count = 0
	if str(len(cek.find("tbody").text.strip())) == 0:
		print("   [*] Domain not found ")
	else:
		try:
			while True:
				tbody = cek.find("tbody")
				for hrf in tbody.find_all("a"):
					count += 1
					for x in list("\|/-"):
						print("\r   ["+x+"] Collect "+str(count)+" Domain.. ", end="")
						sleep(0.01)
					write(saved, hrf.text.strip())

				pagination = cek.find("div", {"style": "text-align:center"})
				if "Next Page" in str(pagination):
					gets = pagination.find("a")["href"]
					cek = par(req.get(gets, headers={"user-agent": "chrome"}).text, "html.parser")
					continue
				else:
					break
		except KeyboardInterrupt:
			pass
	return True

def startMenu():
	print("""\n
 
             Ḁ̷̢̤̥̹̮̬̠̰̞̌̚͝R̷͕̱̥̖̟͔̥͉̃̈̇͜ͅY̸̨̛̞̮̮͎͚̥̰̱͛͒̾̚͜A̷̧̨̡̼̫̭̠͇̼̎͊͂̀͂͘X̸̢̨̯̥̗͕͖̹͖̒͋̈́́̕ͅZ̷̡̮͇̹̝͕͕̻͂̽̊̊͗͌̕͝ͅ
                                     
                    
     OWNER @arya
menu:
	1. Target Domain anti galau
	2.  Mass Random Domain anti meteor
	""")
	plih = input("choose > ")
	while plih == "" or not plih.isdigit():
		print("× WTF bro!!")
		plih = input("choose > ")
	if plih == "1":
		print("Please wait..")
		add = chusMenu()
		pil = input("domain (extension: id,edu,gov)>> ")
		while pil == "":
			pil = input("domain (Extension: go.id ac.id)>> ")
		try:
			key = add[pil]
		except:
			exit("× Domain not available\n")
		with work(max_workers=5) as sub:
			sub.submit(SiteScraper, key)
		print("\nProcess completed")
		print("Result save: "+saved)
	elif plih == "2":
		print("Please wait..\nCtrl + C to stop process\n\n")
		chusget = ExtDom().GetOne()
		with work(max_workers=20) as sub:
			randomDomain()
			backorder()
			for chus in chusget:
				try:
					sub.submit(SiteScraper, chus[0])
				except KeyboardInterrupt:
					pass
		print("\nProcess completed")
		print("Result save: "+saved)

if __name__=="__main__":
	os.system("clear")
	startMenu()

