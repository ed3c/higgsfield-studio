"""UI must not rely on inline style attributes blocked by its own CSP (style-src 'self')."""
import unittest
from pathlib import Path

SITE=Path(__file__).resolve().parents[1]/'review_site'


class ReviewUiCspTests(unittest.TestCase):
    def test_no_inline_style_attributes(self):
        for name in ('index.html','app.js'):
            self.assertNotIn('style="',(SITE/name).read_text(encoding='utf-8'),name)


if __name__=='__main__':unittest.main()
