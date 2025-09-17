import bz2
import xml.etree.ElementTree as ET
from config import WIKIPEDIA_FILE


def parse_wikipedia_dump():
    # Wikipedia XML uses namespaces, so we need to handle them
    namespace = "{http://www.mediawiki.org/xml/export-0.11/}"
    with bz2.open(WIKIPEDIA_FILE, "rt", encoding="utf-8") as file:
        context = ET.iterparse(file, events=("end",))
        count = 0
        for event, elem in context:
            if elem.tag == namespace + "page":
                title_elem = elem.find(namespace + "title")
                revision_elem = elem.find(namespace + "revision")
                text_elem = (
                    revision_elem.find(namespace + "text")
                    if revision_elem is not None
                    else None
                )
                title = title_elem.text if title_elem is not None else None
                text = text_elem.text if text_elem is not None else None
                yield title, text
                count += 1
                elem.clear()
                # if limit and count >= limit:
                #     break
