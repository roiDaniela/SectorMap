import matplotlib
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt
import PySimpleGUI as sg

fig=plt.figure()
ax=fig.add_subplot(111)

fov = Wedge((.2,.2), 0.6, 30, 60, color="r", alpha=0.5)

ax.add_artist(fov)

plt.show()

# draw the figure so the animations will work
# fig = plt.gcf()
# fig.show()
# fig.canvas.draw()
#
# while True:
#     # compute something
#     plt.plot([1], [2])  # plot something
#
#     # update canvas immediately
#     plt.xlim([0, 100])
#     plt.ylim([0, 100])
#     # plt.pause(0.01)  # I ain't needed!!!
#     fig.canvas.draw()