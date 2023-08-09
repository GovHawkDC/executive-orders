import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://governor.ri.gov/executive-order-archive"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//table[contains(@class,'views-table')]/tbody/tr"):
    identifier = row.xpath("td[2]/a[1]")[0].text_content()
    html_url = row.xpath("td[2]/a[1]/@href")[0]
    title = row.xpath("td[3]")[0].text_content()
    pubdate = row.xpath("td[1]")[0].text_content().strip()
    pubdate = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="ri",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:ri",
        html_url=html_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
