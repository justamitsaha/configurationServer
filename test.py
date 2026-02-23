import xml.etree.ElementTree as ET


def check_name_presence(xml_file, search_value):
    """
    Parses XML and checks in which roles (principal/permission-group)
    a given name value is present or missing.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    roles_found = set()
    roles_missing = set()

    # iterate over principals (roles)
    for principal in root.iter("principal"):

        role_name = principal.attrib.get("name")

        if not role_name:
            continue

        found = False

        # search all nodes under this role having attribute name=""
        for node in principal.iter():
            name_attr = node.attrib.get("name")

            if name_attr and search_value in name_attr:
                found = True
                break

        if found:
            roles_found.add(role_name)
        else:
            roles_missing.add(role_name)

    print("\n===== RESULT =====")
    print(f"\nPresent in roles ({len(roles_found)}):")
    for r in sorted(roles_found):
        print(f"  ✅ {r}")

    print(f"\nMissing in roles ({len(roles_missing)}):")
    for r in sorted(roles_missing):
        print(f"  ❌ {r}")


# ----------------------
# Usage
# ----------------------
if __name__ == "__main__":
    xml_path = "policy.xml"   # your XML file
    search_string = input("Enter name value to search: ").strip()

    check_name_presence(xml_path, search_string)
