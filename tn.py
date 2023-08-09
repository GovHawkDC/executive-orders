import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://sos.tn.gov/publications/services/executive-orders-governor-bill-lee"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//div[contains(@class,'field--name-field-info-text')]//table/tbody/tr")[1:]:
    identifier = row.xpath("td[1]/a[1]")[0].text_content()
    pdf_url = row.xpath("td[1]/a[1]/@href")[0]
    title = row.xpath("td[2]")[0].text_content()
    pubdate = row.xpath("td[3]")[0].text_content().strip()
    pubdate = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="tn",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:tn",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
