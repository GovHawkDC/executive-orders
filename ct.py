import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://portal.ct.gov/Office-of-the-Governor/Governors-Actions/Executive-Orders/Governor-Lamonts-Executive-Orders/"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//ul[@class='list--desc']/li"):
    pubdate = row.xpath("span[@class='date']")[0].text_content()
    pubdate = dateutil.parser.parse(pubdate)
    link = row.xpath("a[1]")[0]

    identifier = link.text_content()

    pdf_url = link.xpath("@href")[0]
    title = row.xpath("p[1]")[0].text_content()
    eo = executiveorder.executiveorder(
        abbr="ct",
        ocd_id="ocd-division/country:us/state:co",
        identifier=identifier,
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()

#TODO: Pagination