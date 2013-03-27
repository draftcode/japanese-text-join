# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

import docutils.nodes
import docutils.transforms
import unicodedata

class JapaneseTextJoin(docutils.transforms.Transform):
    default_priority = 800

    def apply(self):
        for text in self.document.traverse(docutils.nodes.Text):
            if (not isinstance(text.parent, docutils.nodes.literal_block) and
                not isinstance(text.parent, docutils.nodes.raw)):
                lines = []
                prev_category = ''
                for line in text.astext().splitlines():
                    line = line.strip()
                    if len(lines) > 0 and len(line) > 0:
                        if prev_category == 'Lo' or unicodedata.category(line[0]) == 'Lo':
                            lines[-1] += line
                        else:
                            lines.append(line)
                        prev_category = unicodedata.category(line[-1])
                    else:
                        lines.append(line)
                joined_text = '\n'.join(lines)
                text.parent.replace(text, docutils.nodes.Text(joined_text, text.rawsource))

def setup(app):
    app.add_transform(JapaneseTextJoin)

