import dateutil.parser
import requests
import logging
import lxml.html
import re
from executiveorder import executiveorder

urls = [
    "https://governor.hawaii.gov/category/newsroom/executive-orders/",
    "https://governor.hawaii.gov/category/newsroom/emergency-proclamations/",
]

for url in urls:
    page = requests.get(url).content
    page = lxml.html.fromstring(page)
    page.make_links_absolute(url)

    for row in page.xpath("//div[@id='content']/div[@class='post']"):

        id_link = row.xpath(".//h3/a")[0]
        pdf_url = id_link.xpath("@href")[0]
        pdf_url = pdf_url.replace("#new_tab", "")
        id_str = id_link.text_content().strip()

        pubdate = row.xpath(".//p[@class='meta-info']")[0].text_content()
        pubdate = re.findall(r"Posted on (\w+\s\d+,\s\d+) in", pubdate)
        pubdate = pubdate[0]
        pubdate = dateutil.parser.parse(pubdate)

        classification = "proclamation" if "proclamations" in url else "executive-order"

        eo = executiveorder.executiveorder(
            abbr="hi",
            classification=classification,
            ocd_id="ocd-division/country:us/state:hi",
            identifier=id_str,
            pdf_url=pdf_url,
            published=pubdate,
            source_url=url,
        )
        logging.info(eo)
        eo.save()

    # TODO: pagination
