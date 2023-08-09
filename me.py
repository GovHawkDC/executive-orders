import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "https://www.maine.gov/governor/mills/official_documents"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//ul[@class='plain']/li"):
    link = row.xpath(".//a")[0]
    title = link.text_content().strip()
    href = link.xpath("@href")[0]

    if href.lower().endswith(".pdf"):
        pdf_url = href
        html_url = ""
    else:
        html_url = href
        pdf_url = ""


    pubdate = row.text_content().split("-")[-1].strip()
    try:
        pubdate = dateutil.parser.parse(pubdate, dayfirst=False)
    except dateutil.parser._parser.ParserError:
        pubdate = row.xpath("text()")[-1]
        pubdate = pubdate.replace("-","").replace(")","").strip()
        pubdate = dateutil.parser.parse(pubdate, dayfirst=False)

    eo = executiveorder.executiveorder(
        abbr="me",
        ocd_id="ocd-division/country:us/state:me",
        pdf_url=pdf_url,
        html_url=html_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    eo.save()

# TODO: some weird nested ones here