from PyQt6.QtWidgets import QTabWidget

from .ControlsTab import ControlsTab
from .MetricsTab import MetricsTab
from .EvaluationTab import EvaluationTab


class Tabs(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.controls_tab = ControlsTab()
        self.metrics_tab = MetricsTab()
        self.evaluation_tab = EvaluationTab()
        self.addTab(self.controls_tab, "NMF")
        self.addTab(self.metrics_tab, "Metrics")
        self.addTab(self.evaluation_tab, "Evaluation")

        self.setMaximumWidth(200)
