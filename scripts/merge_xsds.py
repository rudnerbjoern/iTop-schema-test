from lxml import etree
import os

XSD_NS = "http://www.w3.org/2001/XMLSchema"
NSMAP = {"xs": XSD_NS}
INCLUDE_TAG = f"{{{XSD_NS}}}include"

included_files = set()

def resolve_includes(tree, base_path):
    root = tree.getroot()
    includes = root.findall(INCLUDE_TAG)
    for include in includes:
        href = include.attrib.get("schemaLocation")
        if not href:
            continue
        included_path = os.path.normpath(os.path.join(base_path, href))
        if included_path in included_files:
            root.remove(include)
            continue
        print(f"Including: {included_path}")
        included_tree = etree.parse(included_path, etree.XMLParser(remove_blank_text=True))
        resolve_includes(included_tree, os.path.dirname(included_path))
        included_root = included_tree.getroot()
        for child in included_root:
            root.append(child)
        root.remove(include)
        included_files.add(included_path)

MASTER_FILE = "schemas/itop_design.master.xsd"
OUTPUT_FILE = "dist/itop_design_combined.xsd"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

master_tree = etree.parse(MASTER_FILE, etree.XMLParser(remove_blank_text=True))
resolve_includes(master_tree, os.path.dirname(MASTER_FILE))

# Pretty-print output
pretty_xml = etree.tostring(master_tree.getroot(), pretty_print=True, xml_declaration=True, encoding="UTF-8")
formatted_root = etree.fromstring(pretty_xml)

etree.ElementTree(formatted_root).write(
    OUTPUT_FILE,
    pretty_print=True,
    xml_declaration=True,
    encoding="UTF-8"
)

print(f"✅ Combined schema written to: {OUTPUT_FILE}")
