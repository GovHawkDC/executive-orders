import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder

url = "http://web.sos.ky.gov/execjournal/jrnl.aspx"

# GET the page once to pull the viewstate vars
page = requests.get(url).content
page = lxml.html.fromstring(page)

viewstate = page.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
viewstategenerator = page.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value')[0]
eventvalidation = page.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]

data = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__LASTFOCUS": "",
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategenerator,
    "__EVENTVALIDATION": eventvalidation,
    "_ctl0:ContentPlaceHolder1:ddlSearchType": "ALL",
    "_ctl0:ContentPlaceHolder1:cbHideInstructions": "on",
    "_ctl0:ContentPlaceHolder1:ddlSearchFields": "EONumber",
    "_ctl0:ContentPlaceHolder1:tbSearch": "2023",
    "_ctl0:ContentPlaceHolder1:ddlAdmin": "All",
    "_ctl0:ContentPlaceHolder1:ddlMatchType": "AnyKeywords",
    "_ctl0:ContentPlaceHolder1:ddlOrderBy": "DateFiled, RType, Class, ID",
    "_ctl0:ContentPlaceHolder1:ddlOrder": "DESC",
    "_ctl0:ContentPlaceHolder1:bSubmit": "Submit",
}

response = requests.post(
    "https://web.sos.ky.gov/execjournal/(S(yequcphbywj4hpb53dswklaf))/jrnl.aspx",
    data=data,
).content


page = lxml.html.fromstring(response)
page.make_links_absolute(url)

# info from the same entry is split across 3 trs, then there's a spacer row
for row in page.xpath("//table/tr")[::4]:
    identifier = row.xpath("td[1]")[0].text_content()
    pubdate = row.xpath("following-sibling::tr[1]/td")[0].text_content().strip()

    pdf_url = row.xpath("following-sibling::tr[2]/td/a[1]/@href")[0]

    pubdate = pubdate.replace("Filed: ", "")

    pubdate = dateutil.parser.parse(pubdate)

    eo = executiveorder.executiveorder(
        abbr="ky",
        identifier=identifier,
        ocd_id="ocd-division/country:us/state:ky",
        pdf_url=pdf_url,
        published=pubdate,
        source_url=url,
    )
    logging.info(eo)
    eo.save()
