import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://governor.vermont.gov/document-types/executive-orders"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//article"):
    identifier = row.xpath("h2/a/span")[0].text_content()
    html_url = row.xpath("h2/a/@href")[0]
    title =row.xpath("div/div[3]")[0].text_content()
    pubdate = row.xpath("div/div[2]")[0].text_content().strip()
    pubdate = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="vt",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:vt",
        html_url=html_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
