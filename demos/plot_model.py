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

# User input widgets
z_slider = models.Slider(start=.001, end=.5, value=.001, step=.01)
x0_slider = models.Slider(start=.1, end=1, value=1, step=.01)
t0_slider = models.Slider(start=-10, end=10, value=0, step=.01)
x1_slider = models.Slider(start=-5, end=5, value=0, step=.01)
c_slider = models.Slider(start=-5, end=5, value=0, step=.01)
input_widgets = [z_slider, x1_slider, x0_slider, t0_slider, x1_slider, c_slider]

# Instantiate plotting objects for each photometric bandpass (ugrizy)
time_arr = np.arange(-100, 100)
zeros = np.zeros_like(time_arr)
u_source = models.ColumnDataSource(data=dict(time=time_arr, flux=zeros))
g_source = models.ColumnDataSource(data=dict(time=time_arr, flux=zeros))
r_source = models.ColumnDataSource(data=dict(time=time_arr, flux=zeros))
i_source = models.ColumnDataSource(data=dict(time=time_arr, flux=zeros))
z_source = models.ColumnDataSource(data=dict(time=time_arr, flux=zeros))
y_source = models.ColumnDataSource(data=dict(time=time_arr, flux=zeros))
data_sources = [u_source, g_source, r_source, i_source, z_source, y_source]

u_fig = figure()
g_fig = figure()
r_fig = figure()
i_fig = figure()
z_fig = figure()
y_fig = figure()
figures = [u_fig, g_fig, r_fig, i_fig, z_fig, y_fig]

for _fig, _data_source in zip(figures, data_sources):
    _fig.line(x='time', y='flux', source=_data_source)


###############################################################################
# Define callbacks
###############################################################################


def update_plot(attr, old, new):
    model.set(
        z=z_slider.value,
        x0=x0_slider.value,
        t0=t0_slider.value,
        x1=x1_slider.value,
        c=c_slider.value
    )

    for band, data_source in zip('ugrizy', data_sources):
        flux = model.bandflux(f'LSST{band}', time_arr)
        data_source.update(data=dict(time=time_arr, flux=flux))


for _widget in input_widgets:
    _widget.on_change('value', update_plot)

update_plot(None, None, None)

###############################################################################
# Layout the page
###############################################################################

user_inputs = column(*input_widgets, width=320, height=1000)
doc_layout = layout(
    [[u_fig, g_fig, r_fig],
     [i_fig, z_fig, user_inputs]],
    sizing_mode="scale_both")

curdoc().add_root(doc_layout)
curdoc().title = "SN Light-Curves"
