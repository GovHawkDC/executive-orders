import dateutil.parser
import requests
import logging
from number_parser import parse
import lxml.html
import re
from executiveorder import executiveorder

url = "https://gov.nv.gov/Newsroom/ExecOrders/Executive-Orders/"

page = requests.get(url).content
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//div[contains(@class,'col-12 bg-light')]"):
    identifier = row.xpath("div//h2")[0].text_content()
    html_url = row.xpath("div/div/a[not(@href = '')]/@href")[0]
    title = (
        row.xpath("div/div/a[not(@href = '')]")[0]
        .text_content()
        .replace(identifier, "")
        .strip()
    )

    # they don't provide a publish date, but it's in the plain text
    # so download it and parse it out
    eo_page = requests.get(html_url).text
    eo_page = lxml.html.fromstring(eo_page)

    closing = eo_page.xpath("//p[contains(text(),'IN WITNESS WHEREOF, I have')]")[
        0
    ].text_content()
    closing = closing.replace("\n", " ")
    closing = re.sub(r"\s+", " ", closing)

    pubdate_text = re.findall(
        r"State Capitol in Carson City, this (.*)\.", closing, flags=re.IGNORECASE
    )
    pubdate_text = parse(pubdate_text[0])
    pubdate_text = pubdate_text.replace("in the year", "")
    pubdate_text = pubdate_text.replace("day of", "of")
    pubdate = dateutil.parser.parse(pubdate_text)

    eo = executiveorder.executiveorder(
        abbr="nv",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:nv",
        html_url=html_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()
