import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder
from executiveorder.utils import create_gdrive_download_link

url = "https://www.colorado.gov/governor/2023-executive-orders"

page = requests.get(url).content
page = lxml.html.fromstring(page)

for row in page.xpath("//table/tbody/tr"):
    link = row.xpath("td[1]/a")[0]
    identifier = link.text_content()
    pdf_url = link.xpath("@href")[0]
    title = row.xpath("td[3]")[0].text_content()
    pubdate = row.xpath("td[2]")[0].text_content()
    published = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="co",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:co",
        pdf_url=create_gdrive_download_link(pdf_url),
        published=published,
        source_url=url,
        title=title,
    )
    logging.info(f"{eo}")
    eo.save()
