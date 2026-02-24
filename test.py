import xml.etree.ElementTree as ET


# -------- FILE PATHS --------
XML_FILE = "roles.xml"
TEXT_FILE = "uris.txt"


# -------- READ XML URIs --------
def extract_xml_uris(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    xml_uris = []

    # find permission-param nodes
    for elem in root.iter():
        if "name" in elem.attrib:
            uri = elem.attrib["name"].strip().lower()
            xml_uris.append(uri)

    return xml_uris


# -------- READ TEXT FILE --------
def read_text_uris(text_file):
    with open(text_file, "r", encoding="utf-8") as f:
        return [
            line.strip().lower()
            for line in f
            if line.strip()
        ]


# -------- PARTIAL MATCH CHECK --------
def compare_uris(xml_uris, text_uris):

    found = {}
    missing = []

    for text_uri in text_uris:
        matches = [x for x in xml_uris if text_uri in x]

        if matches:
            found[text_uri] = matches
        else:
            missing.append(text_uri)

    return found, missing


# -------- MAIN --------
if __name__ == "__main__":

    xml_uris = extract_xml_uris(XML_FILE)
    text_uris = read_text_uris(TEXT_FILE)

    found, missing = compare_uris(xml_uris, text_uris)

    print("\n=========== FOUND ===========")
    for k, v in found.items():
        print(f"\n{text_uri}")
        for m in v:
            print(f"   -> {m}")

    print("\n=========== MISSING ===========")
    for uri in missing:
        print(uri)
