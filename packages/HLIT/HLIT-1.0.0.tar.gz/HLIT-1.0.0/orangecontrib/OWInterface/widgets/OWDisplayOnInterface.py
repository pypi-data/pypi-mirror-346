from Orange.widgets.utils.widgetpreview import WidgetPreview
import os
from Orange.data.table import Table
from pathlib import Path
from AnyQt import uic

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.HLIT.download.BaseDisplayOnInterface import BaseDisplayOnInterface
    from Orange.widgets.orangecontrib.HLIT.download.type_utils import build_domain_info, compare_domains
else:
    from orangecontrib.HLIT.download.BaseDisplayOnInterface import BaseDisplayOnInterface
    from orangecontrib.HLIT.download.type_utils import build_domain_info, compare_domains


class OWDisplayOnInterface(BaseDisplayOnInterface): # type: ignore
    name = "Display on Local Interface"
    description = "Push data to a local interface (deprecated -> use hlit-dev instead)"
    
    # Assign specific icons depending on environment
    icon = "icons/local_interf_push.svg"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/local_interf_push.svg"

    priority = 1220
    category = "Advanced Artificial Intelligence Tools"
    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    # Path to the UI file
    gui_path = Path(__file__).parent / "designer" / "display_on_interface.ui"

    def __init__(self):
        super().__init__()
        self._setup_ui()  # Call the subclass's _setup_ui implementation

    def _setup_ui(self):
        """Set up the user interface using the Qt Designer UI file."""
        # Load the UI file
        Form, _ = uic.loadUiType(self.gui_path)
        self.ui = Form()
        self.ui.setupUi(self)

        # Connect signals
        self.ui.le_fileId.editingFinished.connect(self.update_fileId)
        self.ui.le_csv_delimiter.editingFinished.connect(self.update_csv_delimiter)
        self.ui.reset_delimiter_button.clicked.connect(self.reset_csv_delimiter)

        # Set initial values
        self.ui.le_fileId.setText(self.output_fileId)
        self.ui.le_csv_delimiter.setText(self.CSVDelimiter)

        # Store references to UI elements
        self.info_label = self.ui.info_label
        self.le_fileId = self.ui.le_fileId
        self.le_csv_delimiter = self.ui.le_csv_delimiter

        # Adjust size to fit content
        self.adjustSize()


# Main block to preview the widget, specific to the subclass
if __name__ == "__main__": 
    WidgetPreview(OWDisplayOnInterface).run(Table("iris"))

