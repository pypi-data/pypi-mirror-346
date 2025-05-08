from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import Block, type_string_in
import xml.etree.ElementTree as etree


class DsfrAlert(Block):
    NAME = "alert"
    ARGUMENT = None
    OPTIONS = {
        "type": ("info", type_string_in(["success", "error", "info", "warning", "new"])),
    }

    def on_create(self, parent):
        # <div class="fr-alert fr-alert--success">
        #     <h3 class="fr-alert__title">Succès de l'envoi</h3>
        #     <p>Description</p>
        # </div>

        alert_div = etree.SubElement(parent, "div")

        if self.argument:
            alert_div.set("class", f"fr-alert fr-alert--{self.options['type']}")
            h3 = etree.SubElement(alert_div, "h3")
            h3.set("class", "fr-alert__title")
            h3.text = self.argument
        else:
            alert_div.set("class", f"fr-alert fr-alert--{self.options['type']} fr-alert--small")

        # Add the content of the block
        content = etree.SubElement(alert_div, "p")

        return content


class DsfrAlertExtension(BlocksExtension):

    def extendMarkdownBlocks(self, md, block_mgr):

        block_mgr.register(DsfrAlert, self.getConfigs())


def makeExtension(*args, **kwargs):
    """Return extension."""

    return DsfrAlertExtension(*args, **kwargs)
