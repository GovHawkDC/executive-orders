import dateutil.parser
import requests
import logging
import lxml.html
import re
from executiveorder import executiveorder

url = "https://gov.georgia.gov/executive-action/executive-orders/2023"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//table[@id='datatable']/tbody/tr"):

    id_link = row.xpath("td[1]//a")[0]
    pdf_url = id_link.xpath("@href")[0]
    id_str = id_link.text_content().strip()

    pubdate = id_str[0:8]
    pubdate = dateutil.parser.parse(pubdate)

    title = row.xpath("td[2]")[0].text_content().strip()

    eo = executiveorder.executiveorder(
        abbr="ga",
        ocd_id="ocd-division/country:us/state:ga",
        identifier=id_str,
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()

# TODO: pagination
