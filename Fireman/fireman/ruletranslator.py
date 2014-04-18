from rte import iptables
import xmltodict, json

class RuleTranslator:
        def __init__(self, rules=""):
            self.rules = rules

        def execute(self, format):
            if format == "iptables":
                iptables.execute(self.rules)
            else:
                raise ValueError("Error: " + format + " is not yet supported")

        def translate(self, format):
            if format == "json":
                rules_dict = xmltodict.parse(self.rules)
                return json.dumps(rules_dict)
            elif format == "xml":
                return self.rules
            else:
                raise ValueError("Error: " + format + " is not yet supported")


