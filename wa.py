import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://governor.wa.gov/office-governor/office/official-actions/executive-orders"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//table[contains(@class,'tablesaw')]/tbody/tr"):
    identifier = row.xpath("td[1]")[0].text_content()
    pdf_url = row.xpath("td[3]/a[1]/@href")[0]
    title =row.xpath("td[3]/a[1]")[0].text_content()
    pubdate = row.xpath("td[2]")[0].text_content().strip()
    pubdate = dateutil.parser.parse(pubdate)
    governor = row.xpath("td[5]")[0].text_content()
    status = row.xpath("td[4]")[0].text_content()

    superceded = False
    if "superseded" in status.lower():
        superceded = True

    eo = executiveorder.executiveorder(
        abbr="wa",
        executive=governor,
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:wa",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        superceded=superceded,
        title=title,
    )
    logging.info(eo)
    eo.save()
