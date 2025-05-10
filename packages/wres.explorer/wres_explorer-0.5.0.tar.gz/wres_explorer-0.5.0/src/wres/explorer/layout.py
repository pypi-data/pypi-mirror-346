"""Layout widgets for the dashboard."""
from typing import Protocol
import pandas as pd
import panel as pn
from panel.template import BootstrapTemplate
from .widgets import Widgets

class TableBuilder(Protocol):
    """
    Build a metrics table from the given data.
    
    Parameters
    ----------
    data: pd.DataFrame
        Data to display in the metrics table.
    
    Returns
    -------
    pn.widgets.Tabulator
        A Tabulator widget displaying the metrics table.
    """
    @staticmethod
    def __call__(data: pd.DataFrame) -> pn.widgets.Tabulator:
        ...

class Layout:
    """
    Layout for the dashboard.
    
    Attributes
    ----------
    widgets: Widgets
        Instance of Widgets to create the layout.
    tabs: pn.Tabs
        Dashboard tabs.
    template: pn.template
        Servable dashboard with widgets laid out.
    """
    def __init__(self, title: str, widgets: Widgets):
        """
        Initialize the layout of the dashboard.
        
        Parameters
        ----------
        title: str
            Dashboard title.
        widgets: Widgets
            Instance of Widgets to create the layout.
        """
        self.widgets = widgets
        self.navigation_buttons = pn.Row(
            self.widgets.back_tab_button,
            self.widgets.next_tab_button,
            align="end"
        )
        self.image_display = pn.Card()
        self.image_viewer = pn.Column(
            self.image_display,
            self.widgets.image_player
        )
        self.tabs = pn.Tabs()
        self.add_tab(
            "CSV Selector",
            pn.Column(
                self.widgets.file_selector,
                self.widgets.load_data_button
                )
            )
        self.add_tab(
            "Feature Selector",
            pn.Row(
                pn.Column(
                    self.widgets.left_feature_selector,
                    self.widgets.right_feature_selector,
                    self.widgets.description_pane
                    ),
                self.widgets.map_selector
            )
        )
        self.add_tab(
            "Metrics Plots",
            pn.Row(
                pn.Column(
                    self.widgets.description_pane,
                    self.widgets.selected_metric
                ),
                self.widgets.metrics_pane
            )
        )
        self.add_tab(
            "Pairs Plot",
            self.widgets.pairs_pane
        )
        self.add_tab(
            "Metrics Table",
            self.widgets.build_table(
                pd.DataFrame({"message": ["no data loaded"]})
        ))
        self.add_tab(
            "Pairs Table",
            self.widgets.build_table(
                pd.DataFrame({"message": ["no data loaded"]})
        ))
        self.add_tab(
            "Image Selector",
            pn.Column(
                self.widgets.image_selector,
                self.widgets.load_images_button
                )
            )
        self.add_tab(
            "Image Viewer",
            self.image_viewer
            )
        self.template = BootstrapTemplate(title=title)
        self.template.main.append(pn.Column(
            self.tabs,
            self.navigation_buttons
        ))
    
    def add_tab(self, name: str, content: pn.pane) -> None:
        """
        Add a tab to the tabs panel.
        
        Parameters
        ----------
        name: str
            Name of the tab.
        content: pn.pane
            Content of the tab.
        """
        self.tabs.append((name, content))
    
    def servable(self) -> BootstrapTemplate:
        """
        Serve the layout.
        """
        return self.template.servable()

    def update_metrics_table(
            self,
            data: pd.DataFrame,
            table_builder: TableBuilder,
            left_feature_name: str | None = None
            ) -> None:
        """
        Update metrics table with new data.
        
        Parameters
        ----------
        data: pd.DataFrame
            Data to display in the metrics table.
        table_builder: TableBuilder
            Function to build the metrics table.
        left_feature_name: str | None
            Name of the left feature to filter the data by.
        """
        df = data.copy()
        if left_feature_name is not None:
            df = df[df["LEFT FEATURE NAME"] == left_feature_name]

        self.tabs[4] = (
            "Metrics Table",
            table_builder(df)
            )

    def update_pairs_table(
            self,
            data: pd.DataFrame,
            table_builder: TableBuilder,
            feature_name: str | None = None
            ) -> None:
        """
        Update pairs table with new data.
        
        Parameters
        ----------
        data: pd.DataFrame
            Data to display in the pairs table.
        table_builder: TableBuilder
            Function to build the pairs table.
        feature_name: str | None
            Name of the feature to filter the data by.
        """
        if feature_name is not None:
            df = data[data["FEATURE NAME"] == feature_name]
        else:
            df = data.copy()

        self.tabs[5] = (
            "Pairs Table",
            table_builder(df)
            )

    def update_images(self, filenames) -> None:
        filenames = list(filenames)
        if len(filenames) == 0:
            self.widgets.image_player.options = ["None"]
            self.widgets.image_player.value = "None"
            return
        self.widgets.image_player.options = filenames
        self.widgets.image_player.value = filenames[0]

    def update_image_card(self, image) -> None:
        self.image_display.objects = [pn.pane.Image(image)]
    
    def clear_image_card(self) -> None:
        self.image_display.clear()
