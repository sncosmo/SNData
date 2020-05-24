"""Bokeh style demonstration for fitting supernova light-curves"""

from pathlib import Path

import numpy as np
import sncosmo
from bokeh import models
from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure

import sndata

model = sncosmo.Model('salt2-extended')

###############################################################################
# Prepare the Data
###############################################################################

# We define photometric the data access objects and the names to display
# {<Astronomical Survey Name>: {<Data Release Name>: <Access Object>, ...}, ...}
data_release_options = {
    'CSP': {
        'DR3': sndata.csp.DR3()
    },
    'DES': {
        'SN3YR': sndata.des.SN3YR()
    }
}

# We make sure the sncosmo fitting package is aware the filters
# for of each data release
for _data_release_dict in data_release_options.values():
    for _data_release in _data_release_dict.values():
        _data_release.register_filters(force=True)

###############################################################################
# Innit Bokeh Plotting Widgets
###############################################################################

# Descriptive text for the top of the page
header_path = Path(__file__).parent / "header.html"
with header_path.open() as infile:
    header_div = models.Div(text=infile.read(), sizing_mode="stretch_width")

# User input widgets for data selection
survey_select = models.Select(title="Survey:", value='CSP', options=list(data_release_options))
release_select = models.Select(title="Data Release:", options=['DR1'])
target_select = models.MultiSelect(title="Supernova Name:", options=[], height=200)
plot_button = models.Button(label="Plot Object", button_type="success")
fit_button = models.Button(label="Fit Light-Curve Params", button_type="success")
data_select_widgets = [survey_select, release_select, target_select, plot_button, fit_button]

# User input widgets for tweaking the model
x0_slider = models.Slider(start=.1, end=1, value=1, step=.01)
t0_slider = models.Slider(start=-10, end=10, value=0, step=.01)
x1_slider = models.Slider(start=-5, end=5, value=0, step=.01)
c_slider = models.Slider(start=-5, end=5, value=0, step=.01)
model_slider_widgets = [x1_slider, x0_slider, t0_slider, x1_slider, c_slider]

fit_results_div = models.Div(text="")

# The figure to plot on
fig = figure(plot_height=400, plot_width=700, sizing_mode="scale_both")
fig.legend.location = "top_left"
fig.legend.click_policy = "hide"


###############################################################################
# Define callbacks
###############################################################################

def enable_sliders(enabled):
    """Enable or disable the slider widgets

    Args:
        enabled (bool): Enable or disable the widgets
    """

    for widget in model_slider_widgets:
        widget.disabled = not enabled


def format_fit_results_txt(results):
    """Format a fit result object as pretty text

    Args:
        results (Result): Result object from an ``sncosmo`` fit

    Returns:
        Fit results as an HTML string
    """

    keys = 'message', 'ncall', 'chisq', 'ndof', 'param_names', 'parameters'
    return '<br>'.join(f'{k}: {results[k]}' for k in keys)


class Callbacks:
    """Defines interactive behavior by providing methods for callbacks"""

    release = None
    object_data = None
    plotted_fits = []
    plotted_data = []

    def clear_fitted_lines(self):
        """Remove model fits from the plot"""

        fit_results_div.update(text='')
        while self.plotted_fits:
            fig.renderers.remove(self.plotted_fits.pop())

    def clear_plotted_object_data(self):
        """Remove object data from the plot"""

        while self.plotted_data:
            fig.renderers.remove(self.plotted_data.pop())

    def update_data_select_widgets(self, attr, old, new):
        """Repopulate options in the input widgets"""

        # Figure out what data releases are available for the survey
        releases = data_release_options[survey_select.value]

        # Update release options
        release_options = list(releases)
        default_release = release_options[0]
        release_select.update(options=release_options, value=default_release)

        # Update object Ids
        self.release = releases[default_release]
        obj_ids = self.release.get_available_ids()
        target_select.update(options=obj_ids, value=obj_ids[0:1])

    def plot_supernova_data(self, event=None):
        """Plot data for the currently selected object Id"""

        self.clear_fitted_lines()
        self.clear_plotted_object_data()

        # Load the new object data
        obj_id = target_select.value[0]
        object_data = self.release.get_data_for_id(obj_id)
        self.object_data = object_data.group_by('band')

        # Update the plot with the data
        for band_data, color in zip(self.object_data.groups, palette):
            line = fig.circle(
                x=band_data['time'],
                y=band_data['flux'],
                color=color,
                # legend_label=band_data['band'][0]
            )

            self.plotted_data.append(line)

        # Update the plot title to match the supernova name
        title = models.annotations.Title()
        title.text = obj_id
        fig.title = title

    def plot_object_fit(self, event=None):
        """Fit the currently plotted data and plot the light-curve"""

        # Fit the light-curve
        model.set(z=self.object_data.meta['z'])
        result, fitted_model = sncosmo.fit_lc(
            self.object_data, model, vparam_names=['t0', 'x0', 'x1', 'c'])

        self._plot_model(fitted_model)

        # Update the sliders to the model values
        enable_sliders(True)
        x0_slider.update(value=fitted_model['x0'])
        t0_slider.update(value=fitted_model['t0'])
        x1_slider.update(value=fitted_model['x1'])
        c_slider.update(value=fitted_model['c'])

        fit_results_div.update(text=format_fit_results_txt(result))

    def _plot_model(self, fitted_model):

        self.clear_fitted_lines()

        # Plot the fitted model
        time_vals = self.object_data['time']
        x = np.arange(min(time_vals) - 10, max(time_vals) + 10)
        bands = sorted(set(self.object_data['band']))
        for band, color in zip(bands, palette):
            line = fig.line(
                x=x,
                y=fitted_model.bandflux(band, x),
                color=color,
                # legend_label=band
            )

            self.plotted_fits.append(line)

    def update_model_with_sliders(self, attr, old, new):

        model.set(
            x0=x0_slider.value,
            x1=x1_slider.value,
            c=c_slider.value
        )

        self._plot_model(model)


callbacks = Callbacks()

survey_select.on_change('value', callbacks.update_data_select_widgets)
plot_button.on_click(callbacks.plot_supernova_data)
fit_button.on_click(callbacks.plot_object_fit)

callbacks.update_data_select_widgets(None, None, None)
callbacks.plot_supernova_data()

###############################################################################
# Layout the page
###############################################################################

left_column = column(
    *data_select_widgets,
    *model_slider_widgets,
    width=320,
    height=1000,
    sizing_mode="fixed")

right_column = column(fig, fit_results_div, height=1000, sizing_mode="scale_width")

doc_layout = layout([[header_div], [left_column, right_column]], sizing_mode="scale_both")

curdoc().add_root(doc_layout)
curdoc().title = "SN Light-Curves"
