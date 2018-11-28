#!/usr/bin/env python
import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

from matplotlib.patches import Wedge
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import tkinter as Tk

"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Basic steps are:
 * Create a Canvas Element
 * Layout form
 * Display form (NON BLOCKING)
 * Draw plots onto convas
 * Display form (BLOCKING)
"""


#------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import NullFormatter  # useful for `logit` scale

# Fixing random state for reproducibility
np.random.seed(19680801)

# make up some data in the interval ]0, 1[
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

# plot with various axes scales
plt.figure(1)

# linear
# plt.subplot(221)
# plt.plot(x, y)
# plt.yscale('linear')
# plt.title('linear')
# plt.grid(True)
#
#
# # log
# plt.subplot(222)
# plt.plot(x, y)
# plt.yscale('log')
# plt.title('log')
# plt.grid(True)
#
#
# # symmetric log
# plt.subplot(223)
# plt.plot(x, y - y.mean())
# plt.yscale('symlog', linthreshy=0.01)
# plt.title('symlog')
# plt.grid(True)

# logit
# plt.subplot(224)
# plt.plot(x, y)
# plt.yscale('logit')
# plt.title('logit')
# plt.grid(True)

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)
fig = plt.gcf()      # if using Pyplot then get the figure from the plot
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

#------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

#------------------------------- Beginning of Matplotlib helper code -----------------------


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.

    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
    return photo

def update_plot(gx, gy):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fov = Wedge((.2, .2), 0.6, 30, 60, color="r", alpha=0.5)
    ax.add_artist(fov)

    # plt.gca().yaxis.set_minor_formatter(NullFormatter())
    axes = plt.gca()
    axes.set_xlim(0, gx)
    axes.set_ylim(-1*gy, gy)

#------------------------------- Beginning of GUI CODE -------------------------------

column1 = [[sg.Text('local point detail', background_color='lightblue', justification='center', size=(10, 1))],
           [sg.Text('x          '), sg.Spin(values=np.arange(-999999, 999999), initial_value=1)],
           [sg.Text('y          '), sg.Spin(values=np.arange(-999999, 999999), initial_value=1)],
           [sg.Text('teta      '), sg.Spin(values=np.arange(-999999, 999999), initial_value=1)],
           [sg.Text('azimuth'), sg.Spin(values=np.arange(-999999, 999999), initial_value=1)]]

# define the window layout
layout = [[sg.Text('Plot test', font='Any 18')],
          [sg.Column(column1, background_color='lightblue')],
          [sg.ReadButton('add', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True)],
          [sg.Canvas(size=(figure_w, figure_h), key='canvas')],
          [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', force_toplevel=True).Layout(layout).Finalize()

# add the plot to the window
fig_photo = draw_figure(window.FindElement('canvas').TKCanvas, fig)

while True:
    (event, value) = window.Read()
    if event is 'add':
        # EXECUTE YOUR COMMAND HERE
        #fig = plt.figure()
        # ax = fig.add_subplot(111)

        # plt.gca().yaxis.set_minor_formatter(NullFormatter())
        axes = plt.gca()
        axes.set_xlim(0, 100)
        axes.set_ylim(-50, +50)
        fov = Wedge((12, 12), 16, 30, 60, color="b", alpha=0.5)
        axes.add_artist(fov)
        fig_photo = draw_figure(window.FindElement('canvas').TKCanvas, fig)
    elif event is None or event == 'EXIT':            # quit if exit button or X
        break
sys.exit(69)
