"""JupyterLab widget for the R2X4 class

Checkout the demo_notebook.ipynb for an example of how to use this widget.
"""
import ipywidgets as widgets


class LightSourceWidget(widgets.VBox):
    def __init__(self, light_source):
        super().__init__()
        self.light_source = light_source
        self.channel_widgets = {}

        name_label = widgets.Label(value=f"{self.light_source.__class__.__name__} ({self.light_source.SOURCE_TYPE})")
        self.children = [name_label]

        if hasattr(self.light_source, "mux_sel"):
            hbox = widgets.HBox()
            label = widgets.Label(value="Toggle channels: ")
            self.mux_sel = widgets.ToggleButton(value=False, description='A')
            hbox.children = [label, self.mux_sel]
            self.children += (hbox,)
            self.mux_sel.observe(self._set_mux_sel, names='value')

        for channel in self.light_source.CHANNELS:
            self._add_channel(getattr(self.light_source, channel.lower()))

        # trigger the mux_sel observer to set the initial state
        self._set_mux_sel({'new': self.light_source.mux_sel.value})

    def _add_channel(self, channel_config):
        channel_widget = LightChannelWidget(channel_config, self.light_source.CHANNEL_DETAILS[channel_config.name])
        self.children += (channel_widget,)
        self.channel_widgets[channel_config.name] = channel_widget

    def _set_mux_sel(self, change):
        if not change['new']:
            description = 'A'
        else:
            description = 'B'
        for channel_widget in self.channel_widgets.values():
            if channel_widget.channel_config.name[-1:] == description.lower():
                channel_widget.color_on()
            else:
                channel_widget.color_off()
        self.mux_sel.description = description
        self.light_source.mux_sel.value = change['new']


class LightChannelWidget(widgets.HBox):
    def __init__(self, channel_config, channel_details):
        super().__init__()
        self.channel_config = channel_config

        self.name_label = widgets.Label(value=channel_config.name, layout=widgets.Layout(width='100px'))
        wavelength_label = widgets.Label(value=f"{channel_details['wavelength']: 5.1f}", layout=widgets.Layout(width='100px'))
        self.power_edit = widgets.Text(value=f"{0:5.3f} {channel_config.unit}", layout=widgets.Layout(width='100px'))
        self.power_edit.on_submit(self.update_from_text_edit)
        self.power_slider = widgets.FloatSlider(min=channel_config.min, max=channel_config.max, layout=widgets.Layout(flex='1'))
        self.power_slider.observe(self._on_slider_change, names='value')

        self.children = [self.name_label, wavelength_label, self.power_edit, self.power_slider]

    def update_from_text_edit(self, change):
        try:
            value = float(self.power_edit.value.strip())
            if value < self.channel_config.min or value > self.channel_config.max:
                raise ValueError("Value out of range")
            self.channel_config.value = value
            self.power_slider.value = value
        except ValueError:
            self.power_edit.value = "Error"

    def _on_slider_change(self, change):
        self.channel_config.value = change['new']
        self.power_edit.value = f"{self.channel_config.value:5.3f} {self.channel_config.unit}"

    def color_on(self):
        """Indicate that the channel is selected

        Color it and put the text in bold
        """
        self.name_label.style = {'description_width': 'initial', 'background': self.channel_config.name[:-2]}

    def color_off(self):
        """Indicate that the channel is not selected

        Make the background ligth gray so we can see the difference with white
        """
        self.name_label.style = {'description_width': 'initial', 'background': 'lightgray'}
