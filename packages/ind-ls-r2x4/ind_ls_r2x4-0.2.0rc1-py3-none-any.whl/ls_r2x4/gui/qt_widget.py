"""Control a light source's power levels from inside a Qt widget.

It can be used in any pyside or pyqt application like for example Gamma desk.
As demo this file itself can be run as a standalone application. For this to work you need qtpy and for example pyside2,
pyside6 or pyqt5 installed in your python environment.
"""
from qtpy import QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSlider,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
)

from ls_r2x4._utils import ConfigValue


class LightSourceR2X4Widget(QWidget):
    """Show the channels of a light source."""

    # pylint: disable=too-few-public-methods

    UNIT_SHORTHAND = {
        "LSB8": "LSB8",
        "%": "%",
        "lm/m^2": "lm",
        "uW/cm^2": "uW",
    }

    update_power_levels = QtCore.Signal()
    write_power_levels = QtCore.Signal()

    def __init__(self, light_source, parent=None):
        """
        Initialize the LightSourceWidget object.

        :param light_source: LightSource instance.
        :param parent: Qt parent object.
        """
        super().__init__(parent=parent)
        self._light_source = light_source
        self._channel_widgets = {}
        self._channel_state = {}

        self.vertical = QVBoxLayout(self)
        self.vertical.setSpacing(0)
        self.vertical.setAlignment(Qt.AlignTop)

        self.label_horizontal = QHBoxLayout(self)

        self.name_label = QLabel(
            text=(
                f"{self._light_source.__class__.__name__}"
                f" ({self._light_source.SOURCE_TYPE})"
            ),
            parent=self,
        )
        self.label_horizontal.addWidget(self.name_label)

        self.vertical.addLayout(self.label_horizontal)

        self.setLayout(self.vertical)

        if hasattr(self._light_source, "mux_sel"):
            h_layout = QHBoxLayout()
            # Create a spacer and add it to the left of the layout
            left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            h_layout.addItem(left_spacer)

            self.left_label = QLabel("A", self)
            h_layout.addWidget(self.left_label)

            h_layout.addSpacing(10)

            self.mux_sel = QCheckBox(self)
            h_layout.addWidget(self.mux_sel)

            h_layout.addSpacing(10)

            self.right_label = QLabel("B", self)
            h_layout.addWidget(self.right_label)

            # Create a spacer and add it to the right of the layout
            right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            h_layout.addItem(right_spacer)

            self.mux_sel.setStyleSheet("""
                QCheckBox {
                    background-color: #bbb;
                    border-radius: 10px;
                    width: 20px;
                    height: 20px;
                }
                QCheckBox::indicator {
                    background-color: white;
                    border-radius: 10px;
                    width: 30px;
                    height: 20px;
                }
                QCheckBox::indicator:checked {
                    margin-left: 25px;
                    margin-right: 0px;
                }
            """)

            self.mux_sel.stateChanged.connect(self._set_mux_sel)

            # add checkbox to switch between two levels mode and 'simple' on/off mode
            self.two_levels_mode = QCheckBox("Two levels mode", self)
            self.two_levels_mode.setChecked(True)
            h_layout.addWidget(self.two_levels_mode)
            self.two_levels_mode.stateChanged.connect(self._two_levels_mode)

            self.vertical.addLayout(h_layout)
            self._light_source.mux_sel.set_value_event += self._update_mux_sel

        for channel in self._light_source.CHANNELS:
            self._add_channel(getattr(self._light_source, channel.lower()))

    def _add_channel(self, channel_config: ConfigValue):
        channel_widget = LightChannelWidget(channel_config, self._light_source.CHANNEL_DETAILS[channel_config.name],
                                            parent=self)
        self.vertical.addWidget(channel_widget)
        self._channel_widgets[channel_config.name] = channel_widget

    def _process_channel_updates(self, channel_state):
        # Remember the channel state.
        self._channel_state = channel_state

        # Fire the signal to update the sliders.
        self.update_power_levels.emit()

    def _update_mux_sel(self, config_value: ConfigValue):
        self.mux_sel.setChecked(config_value.value)
        # Change the border of the slider to indicate the mux selection.
        for channel_widget in self._channel_widgets.values():
            style = channel_widget._SLIDER_STYLE.replace("[color]", channel_widget.color)
            if config_value.value:
                if '_a' in channel_widget.channel_config.name:
                    style = style.replace("[color_left]", "none")
                    style = style.replace("[color_right]", "none")
                else:
                    style = style.replace("[color_left]", channel_widget.color)
                    style = style.replace("[color_right]", "white")
            else:
                if '_b' in channel_widget.channel_config.name:
                    style = style.replace("[color_left]", "none")
                    style = style.replace("[color_right]", "none")
                else:
                    style = style.replace("[color_left]", channel_widget.color)
                    style = style.replace("[color_right]", "white")
            channel_widget.power_slider.setStyleSheet(style)

    def _set_mux_sel(self, state):
        self._light_source.mux_sel.value = bool(state)

    def _two_levels_mode(self, state):
        if state:
            self.left_label.setText("A")
            self.right_label.setText("B")
            # makes sure all channels are visible
            for channel_widget in self._channel_widgets.values():
                channel_widget.setVisible(True)
        else:
            self.left_label.setText("On")
            self.right_label.setText("Off")
            # hide the _b channels and set the value to 0
            for channel_widget in self._channel_widgets.values():
                if '_b' in channel_widget.channel_config.name:
                    channel_widget.power_slider.setValue(0)
                    channel_widget.setVisible(False)


class LightChannelWidget(QWidget):
    """Show wavelength and power of a single light channel in a light source."""

    # pylint: disable=too-many-instance-attributes

    _SLIDER_STYLE = (
        """
        QSlider::groove:horizontal {
        border: 1px solid #bbb;
        background: none;
        height: 10px;
        border-radius: 1px;
        }

        QSlider::sub-page:horizontal {
        background: [color_left];
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::add-page:horizontal {
        background: [color_right];
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::handle:horizontal {
        background: [color];
        border: 1px solid #777;
        width: 13px;
        margin-top: -2px;
        margin-bottom: -2px;
        border-radius: 4px;
        }
        """
    )
    _EDIT_STYLE = "border: 1px solid #bbb; background: #FAFAFA;"
    _EDIT_STYLE_ERROR = "background: #FF5555;"
    _WAVELENGTH_STYLE = "font-size: 6pt; color: #aaa;"
    _COLOR = {"red_a": 'red', "red_b": 'red',
              "green_a": "green", "green_b": "green",
              "blue_a": "blue", "blue_b": "blue",
              "white_a": "white", "white_b": "white"}

    def __init__(self, channel_config: ConfigValue, channel_details: dict, parent=None):
        """
        Initialize the LightChannelWidget object.

        :param channel_config: ConfigValue instance for the channel.
        :param channel_details: Dictionary with channel details, for the moment this is only the wavelength.
        :param parent: Qt parent object.
        """
        # pylint: disable=too-many-arguments
        super().__init__(parent=parent)
        self.channel_config = channel_config
        self.light_source_widget = parent
        self._unit_shorthand = LightSourceR2X4Widget.UNIT_SHORTHAND[channel_config.unit]

        layout = QGridLayout()

        self.channel_name_label = QLabel(channel_config.name, parent=self)
        self.channel_name_label.setMinimumWidth(100)
        self.channel_name_label.setMinimumHeight(20)

        self.wavelength_label = QLabel(
            f"{channel_details['wavelength']: 5.1f}", parent=self
        )
        self.wavelength_label.setMinimumWidth(35)
        self.wavelength_label.setMinimumHeight(20)
        self.wavelength_label.setStyleSheet(self._WAVELENGTH_STYLE)

        self.power_edit = QLineEdit(f"{0:5.3f} {self._unit_shorthand}", parent=self)
        self.power_edit.setStyleSheet(self._EDIT_STYLE)
        self.power_edit.setMinimumWidth(75)
        self.power_edit.setMinimumHeight(20)
        self.power_edit.setMaximumWidth(75)
        self.power_edit.setMaximumHeight(20)
        self.power_edit.editingFinished.connect(self.update_from_text_edit)

        self.color = self._COLOR.get(channel_config.name, channel_config.name)
        style = self._SLIDER_STYLE.replace("[color]", self.color)
        if '_a' in channel_config.name:  # only set the color for the left side of the slider for active channels
            style = style.replace("[color_left]", self.color)
            style = style.replace("[color_right]", "white")
        else:
            style = style.replace("[color_left]", "none")
            style = style.replace("[color_right]", "none")
        self.power_slider = QSlider(orientation=Qt.Horizontal, parent=self)
        self.power_slider.setStyleSheet(style)
        self.power_slider.setMinimumWidth(170)

        # A tick for every 10%. Although the last one is not drawn...
        self.power_slider.setTickInterval(channel_config.max / 9.7)
        self.power_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.power_slider.setMinimumHeight(20)

        self.power_slider.setMinimum(channel_config.min)
        self.power_slider.setMaximum(channel_config.max)

        self.channel_config.set_value_event += self._display_power_value
        self.channel_config.set_value_event += self._update_slider_position
        self.power_slider.valueChanged.connect(channel_config.set_value)

        layout.addWidget(self.channel_name_label, 0, 0)
        layout.addWidget(self.wavelength_label, 0, 1)
        layout.addWidget(self.power_edit, 0, 2)
        layout.addWidget(self.power_slider, 0, 3, Qt.AlignRight)

        layout.setRowMinimumHeight(0, 2)
        layout.setColumnStretch(0, 5)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setColumnStretch(3, 30)
        self.setLayout(layout)

    def update_from_text_edit(self):
        """Move the power based on the value present in the edit box."""
        edit_text = self.power_edit.text().strip().lower()

        if not edit_text:
            return

        is_bit = False
        if self._unit_shorthand.lower() in edit_text:
            edit_text = edit_text.replace(self._unit_shorthand.lower(), "")
        elif "bit" in edit_text:
            is_bit = True
            edit_text = edit_text.replace("bit", "")

        edit_text = edit_text.strip()

        try:
            if is_bit:
                # Value is expressed in 'LSB' bits.
                value_bit = int(edit_text)
                if value_bit < 0:
                    raise ValueError(f"Bit value is lower than 0: {value_bit}.")
                if value_bit > self.channel_config.max:
                    raise ValueError(
                        f"Bit value is higher than maximum: {value_bit} vs {self.channel_config.max}."
                    )
                # Value is relative not to 100% but to max_power.
                value = value_bit / self.channel_config.max
            else:
                # Value is given in current unit.
                value = float(edit_text)
                if value < 0:
                    raise ValueError(f"Value is lower than 0: {value}.")
                if value > self.channel_config.max:
                    raise ValueError(
                        f"Percent value is higher than maximum: {value} vs {self.channel_config.max}."
                    )

        except ValueError:
            # Could not parse...
            self.power_edit.setStyleSheet(self._EDIT_STYLE + self._EDIT_STYLE_ERROR)
            return

        # Parsing successful.
        self.power_edit.setStyleSheet(self._EDIT_STYLE)

        if self.channel_config.TYPE == int:
            value = int(value)
        self.channel_config.value = value

    def _display_power_value(self, config_value: ConfigValue):
        """
        Update the text of the power level edit ox.

        :param config_value: ConfigValue instance, can be ConfigInt or ConfigFloat
        """
        self.power_edit.setText(f"{config_value.value:5.3f} {self._unit_shorthand}")
        # drop the error style (if any).
        self.power_edit.setStyleSheet(self._EDIT_STYLE)

    def _update_slider_position(self, config_value: ConfigValue):
        """
        Move the power slider based on the value of the Config Value (int or float)
        But do not trigger another callback to the ConfigValue.

        :param config_value: ConfigValue instance, can be ConfigInt or ConfigFloat
        """
        self.power_slider.blockSignals(True)
        self.power_slider.setSliderPosition(config_value.value)
        self.power_slider.blockSignals(False)

    @property
    def power_level(self):
        """
        Return the power level of the slider.

        :returns: Power level in the current unit.
        """
        return self.power_slider.sliderPosition()

    @property
    def power_level_percent(self):
        """
        Return the power level of the slider.

        :returns: Power level in percent.
        """
        return 100 * self.power_level / self.channel_config.max


def main():
    import sys
    import logging
    from qtpy.QtWidgets import QApplication
    from ls_r2x4.r2x4 import LightSourceR2X4
    logging.basicConfig(level=logging.INFO)

    ls = LightSourceR2X4()
    app = QApplication(sys.argv)
    light_source_widget = LightSourceR2X4Widget(light_source=ls)
    light_source_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
