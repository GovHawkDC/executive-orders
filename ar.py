import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder


def scrape_listing_page(base_url: str, page_num: int):
    if page_num > 1:
        url = f"{base_url}/{page_num}"
    else:
        url = f"{base_url}/1"

    logging.info(f"Fetch page {page_num}")

    page_plain = requests.get(url).text
    page = lxml.html.fromstring(page_plain)
    page.make_links_absolute(url)

    for row in page.xpath(
        "//div[contains(@class,'dce-posts-container')]//a[contains(@class,'elementor-element')]"
    ):
        html_url = row.xpath("@href")[0]
        title = row.xpath("div[@data-widget_type='theme-post-title.default']")[
            0
        ].text_content()

        pubdate = row.xpath("div[@data-widget_type='dyncontel-date.default']")[
            0
        ].text_content()
        pubdate = dateutil.parser.parse(pubdate)

        eo_page = requests.get(html_url).content
        eo_page = lxml.html.fromstring(eo_page)
        eo_page.make_links_absolute(html_url)

        pdf_url = eo_page.xpath(
            "//div[contains(@class,'e-con-inner')]//a[contains(@href,'.pdf')]/@href"
        )[0]

        eo = executiveorder.executiveorder(
            abbr="ar",
            html_url=html_url,
            ocd_id="ocd-division/country:us/state:ar",
            pdf_url=pdf_url,
            published=pubdate,
            source_url=base_url,
            title=title,
        )
        logging.info(eo)
        eo.save()

    if "No results found." not in page_plain:
        scrape_listing_page(base_url, page_num + 1)


url = "https://governor.arkansas.gov/our-office/executive-orders/"

scrape_listing_page(url, 1)
