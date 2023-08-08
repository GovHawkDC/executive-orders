import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://governor.delaware.gov/executive-orders/"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//div[@id='main_content']/div[@class='row']")[1:]:
    id_link = row.xpath("div[1]/a")[0]
    identifier = id_link.text_content().strip()
    identifier = f"Executive Order {identifier}"
    html_url = id_link.xpath("@href")[0]

    title = row.xpath("div[2]/a")[0].text_content()

    pubdate = row.xpath("div[3]/em")[0].text_content()
    pubdate = dateutil.parser.parse(pubdate)

    eo_page = requests.get(html_url).content
    eo_page = lxml.html.fromstring(eo_page)
    eo_page.make_links_absolute(html_url)

    pdf_url = eo_page.xpath("//div[@id='main_content']//a[contains(@href,'.pdf')]/@href")[0]
    
    eo = executiveorder.executiveorder(
        abbr="de",
        ocd_id="ocd-division/country:us/state:de",
        html_url=html_url,
        identifier=identifier,
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()