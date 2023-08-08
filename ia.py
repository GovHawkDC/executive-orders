import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://www.legis.iowa.gov/publications/otherResources/executiveOrders"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//table[contains(@class,'sortable')]/tbody/tr"):

    id_link = row.xpath("td[2]/a")[0]
    pdf_url = id_link.xpath("@href")[0]
    identifier = id_link.text_content().strip()

    pubdate = row.xpath("td[1]")[0].text_content()
    pubdate = dateutil.parser.parse(pubdate)

    title = row.xpath("td[3]")[0].text_content().strip()
    governor = row.xpath("td[4]")[0].text_content()

    extras = row.xpath("td[5]")[0].text_content().lower()

    rescinded = True if ("rescinded" in extras or "repealed" in extras) else False
    amended = True if "amended" in extras else False

    eo = executiveorder.executiveorder(
        abbr="ia",
        amended=amended,
        identifier=identifier,
        executive=governor,
        ocd_id="ocd-division/country:us/state:ia",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
        rescinded=rescinded,
    )
    logging.info(eo)
    eo.save()
