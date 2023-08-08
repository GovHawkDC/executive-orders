import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://www.sos.ms.gov/communications-publications/executive-orders"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//table[@class='table']/tbody/tr"):
    identifier = row.xpath("td[1]")[0].text_content()
    pdf_url = row.xpath("td[2]/a/@href")[0]
    pubdate = row.xpath("td[3]")[0].text_content()

    if pubdate.strip() == "":
        pubdate = previous_date

    previous_date = pubdate
    pubdate = dateutil.parser.parse(pubdate)

    governor = row.xpath("preceding::h4")[-1].text_content()
    governor = governor.replace("Governor", "").strip()

    eo = executiveorder.executiveorder(
        abbr="ms",
        executive=governor
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:ms",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
    )
    logging.info(eo)
    eo.save()
