# Test file

from defusedxml.ElementTree import fromstring


def parse_xml(xml_string: str):
    root = fromstring(xml_string)
    for project in root.iter("project"):
        for formData in project.iter("formData"):
            for country in formData.iter("country"):
                print(country.text)
            for canton in formData.iter("canton"):
                print(canton.text)


if __name__ == "__main__":
    with open(
        file=r"default-response.xml"
    ) as file:
        xml = file.read()
        parse_xml(xml_string=xml)
        print(xml)
