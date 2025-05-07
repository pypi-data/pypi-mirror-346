from markdown.extensions import Extension

from dsfr_structure.extension import accordion

# Importer les autres extensions ici
from .blockquote import DsfrBlockQuoteExtension
from .table import DsfrTableExtension


class AllExtensions(Extension):
    def extendMarkdown(self, md):
        # Enregistrer chaque extension

        blockquote_ext = DsfrBlockQuoteExtension()
        blockquote_ext.extendMarkdown(md)

        table_ext = DsfrTableExtension()
        table_ext.extendMarkdown(md)

        accordion_ext = accordion.DsfrAccordionExtension()
        accordion_ext.extendMarkdown(md)

        # Enregistrer d'autres extensions ici


def makeExtension(**kwargs):
    return AllExtensions(**kwargs)
