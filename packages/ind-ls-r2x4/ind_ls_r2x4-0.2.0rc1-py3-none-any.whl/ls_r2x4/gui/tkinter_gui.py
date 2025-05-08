"""Basic GUI for controlling the R2X4 light source from tkinter

The qt_widget looks nicer but the advantage of the tkinter gui is that it needs no extra dependencies.
"""

import tkinter as tk
from tkinter import ttk


class LightSourceWidget(tk.Frame):
    def __init__(self, master, light_source):
        super().__init__(master)
        self.light_source = light_source
        self.channel_widgets = {}

        name_label = tk.Label(self, text=f"{self.light_source.__class__.__name__} ({self.light_source.SOURCE_TYPE})")
        name_label.pack()

        if hasattr(self.light_source, "mux_sel"):
            hbox = tk.Frame(self)
            hbox.pack()

            left_label = tk.Label(hbox, text="Toggle channels: ")
            left_label.pack(side=tk.LEFT)

            # make a checkbutton to toggle the mux_sel, make it look like a button

            self.mux_sel = ttk.Checkbutton(hbox, text="A")
            self.mux_sel.pack(side=tk.LEFT)

            self.mux_sel_var = tk.BooleanVar()
            self.mux_sel.config(variable=self.mux_sel_var, command=self._set_mux_sel)

        for channel in self.light_source.CHANNELS:
            self._add_channel(getattr(self.light_source, channel.lower()))
        self._set_mux_sel()

    def _add_channel(self, channel_config):
        channel_widget = LightChannelWidget(self, channel_config, self.light_source.CHANNEL_DETAILS[channel_config.name])
        channel_widget.pack(fill=tk.X, expand=True)
        self.channel_widgets[channel_config.name] = channel_widget

    def _set_mux_sel(self):
        self.light_source.mux_sel.value = self.mux_sel_var.get()
        if self.mux_sel_var.get():
            channel_type = "b"
        else:
            channel_type = "a"
        self.mux_sel.config(text=channel_type)
        for channel_widget in self.channel_widgets.values():
            if channel_widget.channel_config.name.endswith(channel_type):
                channel_widget.show_active()
            else:
                channel_widget.show_inactive()


class LightChannelWidget(tk.Frame):
    def __init__(self, master, channel_config, channel_details):
        super().__init__(master)
        self.channel_config = channel_config

        self.name_label = tk.Label(self, text=channel_config.name, width=10)
        self.name_label.pack(side=tk.LEFT)

        wavelength_label = tk.Label(self, text=f"{channel_details['wavelength']: 5.1f}", width=10)
        wavelength_label.pack(side=tk.LEFT)

        self.power_edit = tk.Entry(self, width=10)
        self.power_edit.insert(0, f"{0:5.3f} {channel_config.unit}")
        self.power_edit.pack(side=tk.LEFT)
        self.power_edit.bind("<Return>", self.update_from_text_edit)

        style = ttk.Style()
        self._style_name = f"{self.channel_config.name}.Horizontal.TScale"
        style.configure(self._style_name, troughcolor="gray", background="gray")

        self.power_slider = ttk.Scale(self, from_=channel_config.min, to=channel_config.max, orient=tk.HORIZONTAL,
                                      style=self._style_name)
        self.power_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.power_slider.bind("<ButtonRelease-1>" , self._on_slider_change)

    def update_from_text_edit(self, event):
        try:
            value = float(self.power_edit.get().strip())
            if value < self.channel_config.min or value > self.channel_config.max:
                raise ValueError("Value out of range")
            self.channel_config.value = value
            self.power_slider.set(value)
        except ValueError:
            self.power_edit.delete(0, tk.END)
            self.power_edit.insert(0, "Error")

    def _on_slider_change(self, event):
        self.channel_config.value = self.power_slider.get()
        self.power_edit.delete(0, tk.END)
        self.power_edit.insert(0, f"{self.channel_config.value:5.3f} {self.channel_config.unit}")

    def show_active(self):
        """Update the background color so indicate it is active"""
        color = self.channel_config.name[:-2]
        style = ttk.Style()
        style.configure(self._style_name, troughcolor=color, background="gray")
        # change the name label background color
        self.name_label.config(bg=color)

    def show_inactive(self):
        """Update the background color so indicate it is inactive"""
        style = ttk.Style()
        style.configure(self._style_name, troughcolor="gray", background="gray")
        self.name_label.config(bg="light gray")

def main():
    import logging
    logging.basicConfig(level=logging.INFO)

    from ls_r2x4.r2x4 import LightSourceR2X4
    ls = LightSourceR2X4()

    root = tk.Tk()
    root.title("Light Source Control")
    light_source_widget = LightSourceWidget(root, light_source=ls)
    light_source_widget.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
