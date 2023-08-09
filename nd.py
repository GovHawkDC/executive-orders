# https://www.governor.nd.gov/executive-orders

import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://www.governor.nd.gov/executive-orders"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//div[contains(@class,'field--name-field-wysiwyg-text')]//li"):
    identifier = ""

    if row.xpath("strong"):
        identifier = row.xpath("strong")[0].text_content()

    if not row.xpath("a"):
        data = row.text_content()
        logging.warning(f"No PDF link for {data}, skipping")
        continue

    pdf_url = row.xpath("a[1]/@href")[0]

    title_parts = row.xpath("a[1]")[0].text_content().strip()
    title_parts = title_parts.replace("\xa0", " ")

    # strip occasional leading -
    if title_parts[0] == "-":
        title_parts = title_parts[1:]

    if " - " in title_parts and title_parts.count(" - ") == 1:
        title_parts = title_parts.split(" - ")
        title = title_parts[1].strip()
        pubdate = title_parts[0].strip()
    elif title_parts.count(" - ") > 1:
        title_parts = row.text_content()
        title_parts = title_parts.split(" - ")
        title = title_parts[2].strip()
        pubdate = title_parts[1].strip()
    else:
        data = row.text_content()
        logging.warning(f"Unable to extract date from {data}, skipping")
        continue

    pubdate = dateutil.parser.parse(pubdate)

    governor = ""
    if "burgum" in title.lower():
        governor = "Doug Burgum"
    elif "dalrymple" in title.lower():
        governor = "Jack Dalrymple"

    eo = executiveorder.executiveorder(
        abbr="nd",
        executive=governor,
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:nd",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
