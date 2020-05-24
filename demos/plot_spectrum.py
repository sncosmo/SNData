"""Bokeh style demonstration of the Salt2 model in separate bandpasses"""

import numpy as np
import sncosmo
from bokeh import models
from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.plotting import figure

model = sncosmo.Model('salt2-extended')

###############################################################################
# Innit Bokeh Plotting Widgets
###############################################################################

z_slider = models.Slider(start=.001, end=.5, value=.001, step=.01)
phase_slider = models.Slider(start=-20, end=100, value=0, step=.01)

wavelengths = np.arange(4000, 12000)
zeros = np.zeros_like(wavelengths)
data_source = models.ColumnDataSource(data=dict(wavelength=wavelengths, flux=zeros))

figure = figure()
figure.line(x='wavelength', y='flux', source=data_source)


###############################################################################
# Define callbacks
###############################################################################


def update_plot(attr, old, new):
    model.set(z=z_slider.value)
    flux = model.flux(phase_slider.value, wavelengths)
    data_source.update(data=dict(wavelength=wavelengths, flux=flux))


z_slider.on_change('value', update_plot)
phase_slider.on_change('value', update_plot)

update_plot(None, None, None)

###############################################################################
# Layout the page
###############################################################################

doc_layout = layout(
    [[figure],
     [z_slider, phase_slider]],
    sizing_mode="scale_both")

curdoc().add_root(doc_layout)
curdoc().title = "SN Spectrum"
