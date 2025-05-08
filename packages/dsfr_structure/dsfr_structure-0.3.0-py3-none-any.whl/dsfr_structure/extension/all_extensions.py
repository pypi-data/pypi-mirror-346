from markdown.extensions import Extension

from dsfr_structure.extension import accordion
from dsfr_structure.extension import alert
from dsfr_structure.extension import blockquote
from dsfr_structure.extension import table
from dsfr_structure.extension import badge

class AllExtensions(Extension):
    def extendMarkdown(self, md):
        blockquote_ext = blockquote.DsfrBlockQuoteExtension()
        blockquote_ext.extendMarkdown(md)

        table_ext = table.DsfrTableExtension()
        table_ext.extendMarkdown(md)

        accordion_ext = accordion.DsfrAccordionExtension()
        accordion_ext.extendMarkdown(md)

        alert_ext = alert.DsfrAlertExtension()
        alert_ext.extendMarkdown(md)

        badge_ext = badge.DsfrBadgeExtension()
        badge_ext.extendMarkdown(md)


def makeExtension(**kwargs):
    return AllExtensions(**kwargs)
