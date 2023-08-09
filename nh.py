import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://www.governor.nh.gov/news-and-media?category=Executive%20Order"
ajax_url = "https://www.governor.nh.gov/views/ajax?category=Executive%20Order&_wrapper_format=drupal_ajax"

data = 'view_name=news&view_display_id=list&view_args=*%2F*%2F*%2F*%2F*%2F*&view_path=%2Fnode%2F115&view_base_path=&view_dom_id=f2a89c059e52b77f1c48000ed4ba58afca2843583a5b5d7b472b14eb0fa1b170&pager_element=0&category=Executive+Order&page=1&_drupal_ajax=1&ajax_page_state%5Btheme%5D=state_of_nh_core&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=classy%2Fbase%2Cclassy%2Fmessages%2Cclassy%2Fnode%2Ccore%2Fnormalize%2Cgoogle_analytics%2Fgoogle_analytics%2Clayout_discovery%2Fonecol%2Cstate_of_nh_core%2Fglobal-scripts%2Cstate_of_nh_core%2Fglobal-styling%2Cstate_of_nh_core%2Fjquery%2Csystem%2Fbase%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module'

headers = {
    'authority': 'www.governor.nh.gov',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'dnt': '1',
    'origin': 'https://www.governor.nh.gov',
    'referer': 'https://www.governor.nh.gov/news-and-media?category=Executive%20Order',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'category': 'Executive Order',
    '_wrapper_format': 'drupal_ajax',
}

page = requests.post(ajax_url, params=params, data=data, headers=headers).json()
page = page[2]["data"]
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//article[contains(@class,'news-item')]"):
    identifier = row.xpath("div[@class='title']")[0].text_content()
    html_url = row.xpath("div[@class='title']/a/@href")[0]
    title =row.xpath("div[@class='description']")[0].text_content()
    pubdate = row.xpath(".//div[contains(@class,'date')]/text()")[1].strip()
    pubdate = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="nh",
        html_url=html_url,
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:nh",
        # pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()

# todo: pagination, fetch pdf url