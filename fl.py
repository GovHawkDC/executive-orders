import dateutil.parser
import requests
import logging
import lxml.html
import re
from executiveorder import executiveorder

url = "https://www.flgov.com/2023-executive-orders/"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//div[@class='textcontent']/table/tbody/tr")[1:]:
    if not row.xpath("td[1]/a"):
        row_text = row.xpath("td[1]")[0].text_content()
        logging.warning(f"Skipping row: {row_text}")
        continue

    title_link = row.xpath("td[1]/a")[0]
    full_title = title_link.text_content().strip()
    pdf_url = title_link.xpath("@href")[0]
    

    matches = re.findall(r"(\#\d+\-\d+)[\s|,]*(.*)", full_title)
    identifier = matches[0][0].replace("#","")
    title = matches[0][1].strip().capitalize()

    pubdate = row.xpath("td[2]")[0].text_content()
    pubdate = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="fl",
        ocd_id="ocd-division/country:us/state:fl",
        identifier=identifier,
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()

# TODO: pagination