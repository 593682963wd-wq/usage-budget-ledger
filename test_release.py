"""作者：Wangyuan；日期：2026-11-08。职责：通过合成输入复验已确认缺陷。"""
import subprocess,sys,tempfile,unittest
from pathlib import Path
class ReleaseTests(unittest.TestCase):
 def test_invalid_decimal_cli(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.json';p.write_text('{"records":[{"id":"a","model":"sample"}],"prices":{"sample":{"input":"bad","cached_input":"0","output":"0"}}}')
   r=subprocess.run([sys.executable,'-B','cli.py',str(p)],capture_output=True,text=True)
   self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
