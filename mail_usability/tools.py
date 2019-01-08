# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools.mail import _Cleaner
import os
import logging
_logger = logging.getLogger(__name__)

_Cleaner._style_whitelist += [
    'word-wrap',
    'display'
    'border-top',
    'border-bottom',
    'border-left',
    'border-right',
    'text-transform',
    ]


if os.getenv('LOG_STYLE_SANITIZE'):
    # Monkey patch the parse style method to debug
    # the missing style
    def parse_style(self, el):
        attributes = el.attrib
        styling = attributes.get('style')
        if styling:
            valid_styles = {}
            styles = self._style_re.findall(styling)
            for style in styles:
                if style[0].lower() in self._style_whitelist:
                    valid_styles[style[0].lower()] = style[1]
                # START HACK
                else:
                    _logger.warning('Remove style %s %s', *style)
                # END HACK
            if valid_styles:
                el.attrib['style'] = '; '.join(
			'%s:%s' % (key, val)
			for (key, val) in valid_styles.iteritems())
            else:
                del el.attrib['style']
    import pdb; pdb.set_trace()
    _Cleaner.parse_style = parse_style
