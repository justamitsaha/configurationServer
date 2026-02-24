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



1. Parse Login API Response

-   Converts API response string → JSON object.
    
-   Extracts **customer ID (BP_CUSTOMER_ID)** from response.
    
-   Stores it into `BaseProfile` (session/user context).
    

**Goal:** attach login response data to the current user session.

----------

2. Initialize Digipass Flags

Several flags are initialized (mostly `"N"` initially):

-   `dpActiveReg` → whether Digipass registration exists
    
-   `dpDeviceIdMatch` → device ID match status
    
-   `dpUniqueIdMatch` → unique device hash match
    
-   `dpIsDeviceFresh` → whether device is new/fresh
    

These flags control downstream authentication behavior.

----------

 3. Check Digipass Registration

-   Reads token from profile/DB.
    
-   If token exists → user has active Digipass registration.
    

tokenFromDB != empty → dpActiveReg = Y  
else → dpActiveReg = N

----------

 4. Fetch Device Information

The code retrieves:

-   `deviceId` from profile
    
-   `uniqueIDHashFromDevice` (device fingerprint/hash)
    
-   `uniqueIdFromDB` (stored server value)
    

Purpose: compare **current device vs registered device**.

----------

5. Read Stored Device List (JSON Parsing)

-   Fetches device details JSON (`DP_DEVICE_DETAILS`).
    
-   Deserializes JSON into:
    

DeviceList  
 → List<DeviceDetail>

Then loops through devices:

if deviceId == storedDeviceId  
 dpDeviceIdMatch = Y

**Goal:** confirm login device exists in known devices.

----------

6. Generate & Compare Unique Device Hash

-   Generates DB-side unique hash:
    
    dbUniqueIdHash = generateUniqueId(uniqueIdFromDB)
    
-   Compares with device hash sent during login.
    

if hashes match → dpUniqueIdMatch = Y  
else → N

This acts as **device fingerprint validation**.

----------

7. Fresh Device Detection

If device hash is missing/invalid:

dpIsDeviceFresh = Y

Meaning login is from a new or unknown device.

----------

8. Feature Toggle Logic

If configuration flag is enabled:

isDigipassManageRemovalEnabled

AND all conditions match:

-   device fresh = Y
    
-   active registration = Y
    
-   deviceIdMatch = Y
    
-   uniqueIdMatch = Y
    

Then flags are reset (forcing removal/reset flow).
