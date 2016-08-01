from bs4 import BeautifulSoup

from scrapy.crawler import CrawlerProcess

from scrapy.spider import CrawlSpider
from scrapy.http import FormRequest
from loginform import fill_login_form
from scrapy.http import Request, TextResponse

from selenium import webdriver

import time


def parse(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def scrape(base_url, page, user, password):
    class LoginSpider(CrawlSpider):
        name = base_url
        start_urls = [base_url + "login.action?os_destination=%2Findex.action&permissionViolation=true"]
        login_user = user
        login_pass = password

        def parse(self, response):
            args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
            return FormRequest(url, method=method, formdata=args, callback=self.after_login)

        def after_login(self, response):
            return Request(
                url="%s%s" % (base_url, page),
                callback=self.parse_tastypage)

        def __init__(self):
            CrawlSpider.__init__(self)
            self.verificationErrors = []
            self.selenium = webdriver.Firefox()

        def __del__(self):
            print(self.verificationErrors)
            self.selenium.quit()

        def parse_tastypage(self, response):
            sel = self.selenium
            sel.get(response.url)

            # Wait for javscript to load in Selenium
            time.sleep(2.5)

            elem = sel.find_element_by_name('os_username')  # Find the search box
            elem.send_keys(user)
            elem = sel.find_element_by_name('os_password')  # Find the search box
            elem.send_keys(password)
            sel.find_element_by_id('loginButton').click()

            # Do some crawling of javascript created content with Selenium
            time.sleep(4.5)

            el = sel.find_element_by_class_name('metadata-summary-macro')
            contents = el.get_attribute('innerHTML')

            with open('table_dump.html', 'w') as table_dump:
                table_dump.write('<table>')
                table_dump.write(contents)
                table_dump.write('</table>')
            yield TextResponse(contents)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(LoginSpider)
    process.start()