import re

def create_gdrive_download_link(url: str) -> str:
    if "drive.google.com" not in url.lower():
        return url

    google_id = re.findall(r"\/d\/(.*)\/view", url)
    if len(google_id) > 0:
        google_id = google_id[0]
    else:
        google_id = re.findall(r"\?id=(.*)", url)
        google_id = google_id[0]

    download_url = f"https://drive.google.com/uc?export=download&id={google_id}"
    return download_url
