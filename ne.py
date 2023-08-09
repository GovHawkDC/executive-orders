import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "http://govdocs.nebraska.gov/docs/pilot/pubs/EOIndex.html"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//table[contains(@class,'MsoNormalTable')]/tr")[1:]:
    identifier = ""
    if row.xpath("td[1]/a"):
        identifier = row.xpath("td[1]/a")[0].text_content()

    if not row.xpath("td[2]//a[1]"):
        title = row.xpath("td[2]")[0].text_content()
        logging.warning(f"No PDF file for {title}, skipping")
        continue

    pdf_url = row.xpath("td[2]//a[1]/@href")[0]
    title = row.xpath("td[2]//a[1]")[0].text_content()
    pubdate = row.xpath("td[3]")[0].text_content().strip()

    try:
        pubdate = dateutil.parser.parse(pubdate)
    except dateutil.parser._parser.ParserError:
        logging.warning(f"Unable to parse date {pubdate}, for {title} skipping")
        continue

    eo = executiveorder.executiveorder(
        abbr="ne",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:ne",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
