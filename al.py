import dateutil.parser
import requests
import logging
import lxml.html
from executiveorder import executiveorder


class alscraper:
    page_num = 0

    def scrape_listing_page(self, url):
        self.page_num += 1
        logging.info(f"Fetch page {self.page_num}")

        page = requests.get(url).content
        page = lxml.html.fromstring(page)
        page.make_links_absolute(url)

        for row in page.xpath("//div[contains(@class,'story-summary')]"):
            page_link = row.xpath("h2[contains(@class,'story-title')]/a")[0]
            html_url = page_link.xpath("@href")[0]
            identifier = page_link.text_content()
            title = row.xpath("p[contains(@class,'excerpt')]")[0].text_content()

            pubdate = row.xpath("time/@datetime")[0]
            pubdate = dateutil.parser.parse(pubdate)

            eo_page = requests.get(html_url).content
            eo_page = lxml.html.fromstring(eo_page)
            eo_page.make_links_absolute(html_url)

            pdf_url = eo_page.xpath("//a[contains(@class, 'pdfemb-viewer')]/@href")[0]

            eo = executiveorder.executiveorder(
                abbr="al",
                html_url=html_url,
                identifier=identifier,
                ocd_id="ocd-division/country:us/state:al",
                pdf_url=pdf_url,
                published=pubdate,
                source_url=url,
                title=title,
            )
            logging.info(eo)
            eo.save()

        if page.xpath("//a[contains(@class,'nextpostslink')]/@href"):
            next_url = page.xpath("//a[contains(@class,'nextpostslink')]/@href")[0]
            self.scrape_listing_page(next_url)


url = "https://governor.alabama.gov/newsroom/category/executive-orders/"

als = alscraper()
als.scrape_listing_page(url)
