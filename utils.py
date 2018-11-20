import uuid,base64
import re

def protocol_from_url(url):
    """
    Given a url, extracts the protocol acronym
    """
    pattern = re.compile("^[^:]+(?=://)")
    match = pattern.search(url)
    if match:
        return match.group(0)


def filename_from_url(url):
    """
    Creates a unique filename based on the URL. There is a vanishingly small
    chance of filename collision, but I've left the function this way because
    I feel it's worth it to have shorter filenames. Collisions could be
    completely avoided by something like just base64 encoding the url
    """
    name = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
    short = base64.encodebytes(uuid.UUID(name).bytes).decode("ascii").rstrip('=\n').replace('/', '_')
    return short

