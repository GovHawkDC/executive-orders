import dateutil.parser
import json
import requests
import logging
import lxml.html
import re
from executiveorder import executiveorder

url = "https://governor.ohio.gov/media/executive-orders"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

json_url = "https://governor.ohio.gov/wps/wcm/connect/gov/Ohio Content English/governor?source=library&srv=cmpnt&cmpntid=aa7a4aa9-f871-4f6e-a646-3b6a162a51dd&location=Ohio+Content+English//governor/media/executive-orders"
page = requests.get(json_url, headers=headers).content
page = json.loads(page)

for row in page:
    identifier = row["title"]
    title = row["summary"]
    html_url = f"https://governor.ohio.gov/{row['url']}"
    pubdate = dateutil.parser.parse(row['startTimeWCM'])


    eo = executiveorder.executiveorder(
        abbr="oh",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:oh",
        html_url=html_url,
        published=pubdate,
        source_url=url,
        title=title,
    )
    logging.info(eo)
    eo.save()

# TODO: pagination