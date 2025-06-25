from lxml import etree
import glob, os

INPUT_DIR = "schemas/parts"
OUTPUT_FILE = "dist/itop_design_combined.xsd"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Basis-Schema erzeugen
base_schema = etree.Element("xs:schema", nsmap={"xs": "http://www.w3.org/2001/XMLSchema"})

# Alle Teile einfügen
for xsd_file in sorted(glob.glob(f"{INPUT_DIR}/*.xsd")):
    print(f"Including: {xsd_file}")
    tree = etree.parse(xsd_file)
    for child in tree.getroot():
        base_schema.append(child)

# Zusammengeführte Datei schreiben
etree.ElementTree(base_schema).write(
    OUTPUT_FILE,
    pretty_print=True,
    xml_declaration=True,
    encoding="UTF-8"
)
print(f"Written combined schema to: {OUTPUT_FILE}")
