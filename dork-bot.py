import requests
import re


class Google_dork_bot:
    #Atributes
    query = ''
    count = 0
    num = 100
    end_search = False

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'}
    proxies_list = []
    proxy_fail = []
    proxy_detected_by_google_bots = []
    proxy_item = 0
    no_proxy = False

    request = ''
    html_page = []
    google_url = 'http://www.google.com.br/search'
    

    #Constructor
    def __init__(self, query, proxies_list = []):
        self.query = query
        self.proxies_list = proxies_list


    #Methods
    def clean_html(self, raw_html):
        clean_raw = re.compile('<.*?>')
        clean_text = re.sub(clean_raw, '', raw_html)
        clean_text.replace('&nbsp;', ' ').replace('&amp;', '&')
        return clean_text


    def check_proxies(self):
        if len(self.proxies_list) == 0:
            self.no_proxy = True
        else:
            self.proxy = False


    def init_bot(self):
        while True:
            params = {'q': self.query, 'start': self.count, 'num': self.num}

            self.check_proxies()
            if self.no_proxy:
                self.request = requests.get(self.google_url, headers=self.headers, params=params)
            elif self.proxy_item < len(self.proxies_list):
                proxy = { "http": self.proxies_list[self.proxy_item]}
                try:
                    self.request = requests.get(self.google_url, heders=self.headers, params=params, proxies=proxy)
                except:
                    self.proxy_fail.append(self.proxies_list[self.proxy_item])
                    self.proxy_item += 1
                    continue
            else:
                break
                
            self.html_page = self.request.text
            if ("Our systems have detected unusual traffic from your computer network" in self.html_page):
                self.proxy_item += 1
                proxy_detected_by_google_IP = self.html_page[self.html_page.find("IP address") +12: self.html_page.rfind('<br>Time:')]
                self.proxy_detected_by_google_bots.append(proxy_detected_by_google_IP)
                self.no_proxy = False
                continue
            
            count_cite = self.html_page.count('<cite')
            if(count_cite == 0):
                self.end_search = True
                break

            end = 0
            for i in range(count_cite):
                start = self.html_page.find('<div class="g">', end)
                if start == -1:
                    continue
                
                end = self.html_page.find('<div class="g">', start+1)
                page = self.html_page[start:end]

                tittle = page[page.find(">", page.find('href')) +1: page.find('</a>')]
                print('\033[1;32mTitle --> ', self.clean_html(tittle))

                page_url = page[ page.find('"', page.find('<a href=') ) +1: page.find('"', page.find('<a href=') +9) ]
                print("\033[1;32m URL --> ", self.clean_html(page_url))

                page_text = page[ page.find('<span class="st">') : page.find('</span></div>')]
                print("\033[1;32mText --> ", self.clean_html(page_text))
                print("\n")

            self.count += 100

        if len(self.proxy_fail) != 0 or len(self.proxy_detected_by_google_bots) != 0:
            print('\033[1;31mThe following proxies / IPs have failed, change them: ')
            for i in range(len(self.proxy_fail)):
                print(" --> " + self.proxy_fail[i])

        if len(self.proxy_detected_by_google_bots) != 0:
           print('\033[1;31mThe following proxies / IPs have been detected by Google, please change them:') 
           for i in range(self.proxy_detected_by_google_bots):
               print(" --> " + self.proxy_detected_by_google_bots[i])
        
        if not self.end_search:
            print("\033[1;31mChange the value of the 'count' variable to ", self.count)




def without_proxies():
    dork = str(input("\033[1;92mType a dork --> "))
    gdork = Google_dork_bot(dork)
    gdork.init_bot()


def with_proxies():
    number_of_proxies = int(input("\033[1;92mType a number of proxies --> "))

    list_proxies = []
    for i in range(len(number_of_proxies)):
        number_of_proxies[i] = str(input(f"\033[1;92mType the {i+1} proxy --> "))

    dork = str(input("\033[1;92mType a dork --> "))
    gdork = Google_dork_bot(dork, list_proxies)
    gdork.init_bot()


def init():
    while(1):
        print("\n\033[1;34m ###### Welcome to GOOGLE DORK BOT ######\n")
        print("1 --> Without proxies")
        print("2 --> With Proxies")
        print("3 --> Exit")

        option = int(input("\nChoose a option --> "))

        if option == 1:
            without_proxies()
        elif option == 2:
            with_proxies()
        elif option == 3:
            print("BYE...")
            break
        else:
            print("\033[1;31m Invalid option")


init()
