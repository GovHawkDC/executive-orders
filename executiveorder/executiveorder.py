import datetime
import hashlib
import json
import logging
import os

from dataclasses import asdict, dataclass, field


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class executiveorder:
    ocd_id: str
    abbr: str
    source_url: str
    published: datetime.date = field()
    # if the state gives a unique ID
    identifier: str = ""
    title: str = ""
    pdf_url: str = ""
    html_url: str = ""
    executive: str = ""
    classification: str = "executive-order"
    rescinded: bool = False
    superceded: bool = False
    replaced: bool = False
    amended: bool = False

    def __post_init__(self):
        self.abbr = self.abbr.upper()

        if self.title == "" and self.identifier == "":
            raise ValueError("Order must have either an Identifier, a Title, or both")

        if not os.path.exists("./cache"):
            os.makedirs("./cache")

        if not os.path.exists("./json"):
            os.makedirs("./json")

        if not os.path.exists(f"./json/{self.abbr}"):
            os.makedirs(f"./json/{self.abbr}")

    def dict(self):
        # TODO: better datetime handling here
        return {k: str(v).strip() for k, v in asdict(self).items()}

    def __repr__(self):
        return f"{self.abbr} - {self.identifier} {self.title.strip()}"

    def save(self, filename: str = ""):
        if filename == "":
            unique = f"{self.identifier}{self.title}{self.pdf_url}{self.html_url}{self.source_url}"
            url_hash = hashlib.md5(unique.encode()).hexdigest()
            filename = f"./json/{self.abbr}/{url_hash}.json"

        logging.info(f"Saving to {filename}")

        with open(filename, "w") as f:
            f.write(json.dumps(self.dict()))
