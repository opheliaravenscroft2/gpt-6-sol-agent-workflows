import json,pathlib,unittest
class T(unittest.TestCase):
 def test_provider(self):
  d=json.loads((pathlib.Path(__file__).parents[1]/'.opencode/opencode.json').read_text());self.assertIn('argolink',d['provider']);self.assertNotIn('sk-',str(d))
if __name__=='__main__':unittest.main()
