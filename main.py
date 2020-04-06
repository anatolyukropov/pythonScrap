import requests
import pprint
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


class Advert:
    """
    This is an advert class
    """

    def __init__(self, img_links, title, price_month, price_year, nds, class_of_service, metro, distance_from_metro,
                 bc_name,
                 address, ad_comment, agency):
        self.agency = agency
        self.address = address
        self.bc_name = bc_name
        self.distance_from_metro = distance_from_metro
        self.metro = metro
        self.class_of_service = class_of_service
        self.nds = nds
        self.price_year = price_year
        self.price_month = price_month
        self.title = title
        self.img_links = img_links
        self.ad_comment = ad_comment

    def __str__(self):
        return f'img_links = { self.img_links}, \n title = { self.title}, \n price_month = {self.price_month}, \n price_year = {self.price_year}, \n nds = {self.nds},\n class_of_service = {self.class_of_service},\n metro = {self.metro},\n distance_from_metro = {self.distance_from_metro},\n bc_name = {self.bc_name},\n address = {self.address},\n ad_comment = {self.ad_comment},\n agency = {self.agency}\n\n'


class Scraper:
    """
    Scraper Class
    """

    def __init__(self, url):
        """
            Constructor
        """
        self.url = url
        self.cards_html = []
        self.cards_data = []

    def scrape(self):
        self.get_cards()
        self.get_main_data()

    def get_cards(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, "lxml")
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
            print(response.text)
            self.cards_html = soup.select("._93444fe79c--commercialWrapper--fYaWL")
            self.cards_html.pop()

    def get_main_data(self):
        if self.cards_html and len(self.cards_html) > 0:
            for card in self.cards_html:
                img_links = self.scrap_img_links(card)
                title = self.scrap_title(card)
                price_month, class_of_service = self.scrap_price_month_and_service_class(card)
                nds, price_year = self.scrap_dns_and_price_year(card)
                metro = self.scrap_metro(card)
                distance_from_metro = self.scrap_distance_from_metro(card)
                bc_name = self.scrap_bc_name(card)
                address = self.scrap_address(card)
                ad_comment = self.scrap_ad_comment(card)
                agency = self.scrap_agency(card)
                self.cards_data.append(Advert(img_links, title, price_month, price_year, nds, class_of_service, metro,
                                              distance_from_metro, bc_name, address, ad_comment, agency))
                self.print_result()

    def print_result(self):
        for item in self.cards_data:
            pprint.pprint(item.__dict__)
            print('\n\n')

    @staticmethod
    def scrap_img_links(card):
        if card.select(".c6e8ba5398--image--3ua1b"):
            return list(map(lambda img: img['src'], card.select(".c6e8ba5398--image--3ua1b")))
        return []

    @staticmethod
    def scrap_title(card):
        """
        :param card: BeautifulSoup element of advert block
        :return: {'text': String, 'href': String}
        """
        if card.select_one(".c6e8ba5398--header-link--3XZlV"):
            text, href = ['', '']
            if card.select_one(".c6e8ba5398--header-link--3XZlV").text:
                text = card.select_one(".c6e8ba5398--header-link--3XZlV").text
            if card.select_one(".c6e8ba5398--header-link--3XZlV")['href']:
                href = card.select_one(".c6e8ba5398--header-link--3XZlV")['href']
            return {'text': text,
                    'href': href}
        else:
            return {'text': '',
                    'href': ''}

    @staticmethod
    def scrap_price_month_and_service_class(card):
        """
        :param card: BeautifulSoup element of advert block
        :return: [price_month: String, class_of_service: String ]
        """
        if card.select_one(".c6e8ba5398--header-subtitle--24WXl") and card.select_one(
                ".c6e8ba5398--header-subtitle--24WXl").text:
            list_value = card.select_one(".c6e8ba5398--header-subtitle--24WXl").text.split('Класс')
            if len(list_value) > 1:
                return [list_value[0], list_value[1]]
            else:
                return [list_value[0], '']
        else:
            return ['', '']

    @staticmethod
    def scrap_dns_and_price_year(card):
        """
        :param card: BeautifulSoup element of advert block
        :return: [nds: String, price_year: String]
        """
        if card.select_one(".c6e8ba5398--header-subTerm-list--2yW02"):
            list_value = card.select_one(".c6e8ba5398--header-subTerm-list--2yW02")
            try:
                nds, price = [e.text for e in list_value.children if e.text is not None]
            except Exception as err:
                print(f'error occurred: {err}')
            else:
                return [nds, price]

    @staticmethod
    def scrap_metro(card):
        if card.select_one(".c6e8ba5398--underground-name--1efZ3"):
            return card.select_one(".c6e8ba5398--underground-name--1efZ3").text
        return ''

    @staticmethod
    def scrap_distance_from_metro(card):
        if card.select_one(".c6e8ba5398--remoteness--3bptF"):
            return card.select_one(".c6e8ba5398--remoteness--3bptF").text
        return ''

    @staticmethod
    def scrap_bc_name(card):
        """
        :param card: BeautifulSoup element of advert block
        :return: {'text': String, 'href': String}
        """
        bc_name_html = card.select_one(".c6e8ba5398--building-link--1EYYP")
        if bc_name_html:
            text, href = ['', '']
            if bc_name_html.text:
                text = bc_name_html.text
            if bc_name_html['href']:
                href = bc_name_html['href'] if bc_name_html['href'].startswith('http') else 'https://www.cian.ru' + \
                                                                                            bc_name_html['href']
            return {'text': text,
                    'href': href}
        else:
            return {'text': '',
                    'href': ''}

    @staticmethod
    def scrap_address(card):
        address_html = card.select_one(".c6e8ba5398--address-path--2Y559")
        if address_html and address_html.span:
            return address_html.span['content']
        return ''

    @staticmethod
    def scrap_ad_comment(card):
        html = card.select_one(".c6e8ba5398--description--3cIMh.c6e8ba5398--description-top--36Tdr")
        if html:
            return html.text
        return ''

    @staticmethod
    def scrap_agency(card):
        """
        :param card: BeautifulSoup element of advert block
        :return:  {'name': String, 'checked': Boolean, 'img_link': String, 'phone': String}
        """
        html_name = card.select_one(".c6e8ba5398--userInfo-name--1ZiDD")
        html_img = card.select_one(".c6e8ba5398--userAvatar--36Lg7")
        checked = True if card.select_one(".c6e8ba5398--userInfo-badge--2FzGi") else False
        name = html_name.text if html_name and html_name.text else ''
        img = html_img.img['src'] if html_img and html_img.img else ''
        return {'name': name, 'checked': checked, 'img_link': img}


cian = Scraper('https://www.cian.ru/snyat-ofis/')
cian.scrape()
