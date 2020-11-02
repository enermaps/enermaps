"""xml helpers
"""
from lxml import etree


def etree_fromstring(string):
    """This is a safer implementation of the default fromstring that disable:
    * network interaction.
    * entity resolution.

    This can lead to information leakage and memory hogging.
    see https://github.com/PyCQA/bandit/issues/435
    """
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    root = etree.fromstring(string, parser)
    return root
