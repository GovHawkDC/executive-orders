import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://gov.mt.gov/Documents/GovernorsOffice/executiveorders/"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//div[contains(@class,'card-text')]"):
    identifier = row.xpath("h5")[0].text_content()
    pdf_url = row.xpath("h3/a[1]/@href")[0]
    title =row.xpath("h3/a[1]")[0].text_content()
    pubdate = row.xpath("p[1]")[0].text_content().strip()
    pubdate = dateutil.parser.parse(pubdate)

    governor = "Greg Gianforte"

    eo = executiveorder.executiveorder(
        abbr="mt",
        executive=governor,
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:mt",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
