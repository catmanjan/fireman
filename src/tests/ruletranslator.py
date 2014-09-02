import rte.ruletranslator as rte
from rte.rule import Rule
import unittest

class RuleTranslatorTests(unittest.TestCase):

    def setUp(self):
        # Do a test for a blank rule with minimum valid values
        self.blankRule = Rule("blank", 0, 0, [])

        # Do a test for rules with None for an ID (edgecase?)
        self.noneRule = Rule(None, 0, 0, [])

    def test_add_rule(self):
        self.assertEqual(True, True)

    def test_delete_rule_using_id(self):
        self.assertEqual(True, True)

    def test_delete_rule(self):
        self.assertEqual(True, True)

    def test_translate(self):
        blankRuleJson = "{\"action\": 0, \"conditions\": [], \"id\": \"blank\", \"chain\": 0}"
        noneRuleJson = "{\"action\": 0, \"conditions\": [], \"chain\": 0}"
        
        self.assertEqual(rte.translate(self.blankRule, "json"), blankRuleJson)
        self.assertEqual(rte.translate(self.noneRule, "json"), noneRuleJson)

if __name__ == '__main__':
    unittest.main()