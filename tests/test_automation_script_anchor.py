"""Keep the frozen source's Markdown emphasis from breaking approved note edits."""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE = '/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'


class ScriptAnchorTest(unittest.TestCase):
    def test_exact_bold_missing_and_duplicate_anchors(self):
        source = (ROOT / 'scripts/build_automation_identity.mjs').read_text()
        function = source.split('function replaceOnce(')[1].split('\nlet generated =')[0]
        js = 'function replaceOnce(' + function + '''
const assert = require('node:assert/strict');
assert.equal(replaceOnce('old', 'old', 'new'), 'new');
assert.equal(replaceOnce('The next step is **independent controlled validation**.',
  'The next step is independent controlled validation.', 'Approved new sentence.'),
  'Approved new sentence.');
assert.throws(()=>replaceOnce('missing', 'old', 'new'), /Ambiguous/);
assert.throws(()=>replaceOnce('old old', 'old', 'new'), /Ambiguous/);
'''
        result = subprocess.run([NODE, '-e', js], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
