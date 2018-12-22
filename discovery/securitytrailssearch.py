import securitytrailsparser
import requests
import sys
import time

class search_securitytrail:

    def __init__(self, word):
        self.word = word
        self.key = ""
        if self.key == "":
            print("You need an API key in order to use the SecurityTrails search engine. You can get one here: https://securitytrails.com/")
            sys.exit()
        self.results = ""
        self.totalresults = ""
        self.database = "https://api.securitytrails.com/v1/"
        self.info = ()

    def authenticate(self):
        # method to authenticate api key before sending requests
        headers = {'APIKEY': self.key}
        url = self.database + 'ping'
        r = requests.get(url, headers=headers).text
        if 'False' in r:
            print('\t Key could not be authenticated exiting program')
            sys.exit(-2)
        time.sleep(2)

    def do_search(self):
        url = ''
        headers = {}
        try:
            # https://api.securitytrails.com/v1/domain/domain.com
            url = self.database + 'domain/' + self.word
            headers = {'APIKEY': self.key}
            r = requests.get(url, headers=headers)
            time.sleep(2) #not random delay because 2 seconds is required due to rate limit
        except Exception as e:
            print(e)
        self.results = r.text
        self.totalresults += self.results
        url += '/subdomains'  # get subdomains now
        r = requests.get(url, headers=headers)
        time.sleep(2)
        self.results = r.text
        self.totalresults += self.results

    def process(self):
        self.authenticate()
        self.do_search()
        parser = securitytrailsparser.parser(word=self.word, text=self.totalresults)
        self.info = parser.parse_text()
        #create parser and set self.info to tuple returned from parsing text
        print('\tDone Searching Results')

    def get_ips(self):
        return self.info[0]

    def get_hostnames(self):
        return self.info[1]