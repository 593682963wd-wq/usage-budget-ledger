import unittest,tempfile,json
from pathlib import Path
from core import run

class Tests(unittest.TestCase):
 def test_cost(self):
  r=run(json.loads(Path('example.json').read_text()));self.assertEqual(r['priced_cost'],'0.00014');self.assertEqual(r['budget_remaining'],880)
 def test_empty(self):self.assertEqual(run({})['total_tokens'],0)
 def test_duplicate(self):
  with self.assertRaises(ValueError):run({'records':[{'id':'a','model':'m'},{'id':'a','model':'m'}]})
 def test_missing_price(self):self.assertEqual(run({'records':[{'id':'a','model':'m'}]})['unpriced_events'],['a'])

if __name__=="__main__":unittest.main()
