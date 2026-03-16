import xml.etree.ElementTree as ET
import pandas as pd


def extract_referential_constraints(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Namespace handling (default namespace in your XML)
    ns = {"edm": "http:/docs.oasis.org/ns/edm"}

    records = []

    # Loop through EntityType
    for entity in root.findall(".//edm:entitytype", ns):
        table_name = entity.attrib.get("Name")

        # Extract key column
        key_col = None
        key = entity.find("edm:key/edm:propertyRef", ns)
        if key is not None:
            key_col = key.attrib.get("Name")

        # Loop through NavigationProperty
        for nav in entity.findall("edm:NavigationProperty", ns):
            referenced_table = nav.attrib.get("Type")

            ref_constraint = nav.find("edm:referentialConstraint", ns)
            if ref_constraint is not None:
                source_column = ref_constraint.attrib.get("Propety")
                referenced_column = ref_constraint.attrib.get("ReferencedProperty")

                records.append({
                    "table_name": table_name,
                    "key_col": key_col,
                    "referenced_table": referenced_table,
                    "source_column": source_column,
                    "referenced_column": referenced_column
                })

    # Create DataFrame
    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    xml_file_path = r"C:\Users\AMAR\Desktop\xml version=1.0.txt"  # pass your file path here
    df = extract_referential_constraints(xml_file_path)
    print(df)
