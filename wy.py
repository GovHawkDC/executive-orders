import dateutil.parser
import requests
import logging
import lxml.html
import re
from executiveorder import executiveorder
from executiveorder.utils import create_gdrive_download_link

url = "https://governor.wyo.gov/state-government/executive-orders"
graphql_url = "https://governor.wyo.gov/api/cms/graphql"

body = {
    'operationName': 'PageQuery',
    'variables': {'path': "executive-orders"},
    'query': 'query PageQuery($path: String!) {\n  page(where: {path_ends_with: $path}, orderBy: {publishedUtc: DESC}) {\n    ...Page\n    __typename\n  }\n}\n\nfragment Page on Page {\n  displayText\n  render\n  parentRoute\n  path\n  __typename\n}',
}

headers = {
    'Content-Type': 'application/json'
}

page = requests.post(graphql_url, json=body, headers=headers).json()
page = page['data']['page'][0]['render']
page = lxml.html.fromstring(page)
page.make_links_absolute(url)

for row in page.xpath("//p[contains(@class,'CDt4Ke')]"):
    whole_title = row.text_content().strip()
    if whole_title == "":
        continue
    pdf_url = row.xpath(".//a[1]/@href")[0]
    pdf_url = create_gdrive_download_link(pdf_url)
    title = row.xpath(".//a[1]")[0].text_content()

    identifier = re.findall(r"\d{4}\-\d+", whole_title)
    identifier = identifier[0]

    title = title.replace(identifier, "").strip()

    eo = executiveorder.executiveorder(
        abbr="wy",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:wy",
        pdf_url=pdf_url,
        source_url=url,
        title=title,
        published="2023-01-01",
    )
    logging.info(eo)
    eo.save()
