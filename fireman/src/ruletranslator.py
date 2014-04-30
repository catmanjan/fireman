from rte import iptables
import dicttoxml, json

def execute(self, rules, format):
    """ Execute the set of rules using the specified program
        (Rule, str) -> None
    """
    if format == "iptables":
        # convert to xml for iptables to translate
        iptables.execute(translate("xml"))
    else:
        raise ValueError("Error: " + format + " is not yet supported")

def translate(self, rules format):
    """ Translate the set of rules into a specified format
        (Rule, str) -> None
    """
    if format == "json":
        return json.dumps(rules.__dict__)
    elif format == "xml":
        return dicttoxml.parse(rules.__dict__)
    else:
        raise ValueError("Error: " + format + " is not yet supported")


