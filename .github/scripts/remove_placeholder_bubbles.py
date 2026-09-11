from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old = r'''/* PLACEHOLDER_CHIPS_V1 */
.slot-chip{display:inline-flex;align-items:center;justify-content:center;min-width:1.55em;height:1.55em;padding:0 .38em;border-radius:999px;font-weight:850;font-size:.78em;line-height:1;vertical-align:.12em;border:1px solid transparent;box-shadow:inset 0 0 0 1px rgba(255,255,255,.35)}
.slot-a{background:#e8f1ff;border-color:#bfd0ec;color:#3e5f8c}
.slot-b{background:#f3eafb;border-color:#d5c1e8;color:#76548f}
.vocab-item .slot-chip{font-size:.72em;margin:0 .05em}
.flash-front .slot-chip{font-size:.58em;vertical-align:.18em}
.flash-back-title .slot-chip{font-size:.68em}
.related-chip .slot-chip{font-size:.72em}
.meaning-row .slot-chip{font-size:.76em}
'''
new = r'''/* PLACEHOLDER_CHIPS_V1 */
.slot-chip{display:inline;padding:0;margin:0;border:0;border-radius:0;background:transparent;box-shadow:none;font-weight:850;font-size:inherit;line-height:inherit;vertical-align:baseline}
.slot-a{color:#4f76a8}
.slot-b{color:#8a63a4}
'''
if old not in s:
    raise RuntimeError('Could not find placeholder style block')
s = s.replace(old, new, 1)
path.write_text(s, encoding='utf-8')
print('Removed placeholder bubbles; kept distinct A/B colors.')
