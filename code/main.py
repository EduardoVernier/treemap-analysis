import matplotlib.pyplot as plt
import numpy as np


def styleBoxplot(bp, ax, n_revisions):
    def get_ax_size(ax):
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        width *= fig.dpi
        height *= fig.dpi
        return width, height

    for box in bp['boxes']:
        # change outline color
        box.set(color='#1b9e77', linewidth=0)
        # change fill color
        box.set(facecolor='#1b9e77')
        box.set_zorder(10)
    for i, median in enumerate(bp['medians']):
        median.set(color='#1445FF', linewidth=2, ms=(get_ax_size(ax)[0]) / (n_revisions))
        median.set_zorder(11)
        median.set_xdata([i + 1 - 0.3, i + 1 + 0.3])
    for whisker in bp['whiskers']:
        # Butt remove excess lenght of linewidth
        whisker.set(color='#CCCCCC', linestyle='-', solid_capstyle="butt", markeredgecolor=None,
                    linewidth=(get_ax_size(ax)[0]*1.1) / n_revisions, ms=0)
    for cap in bp['caps']:
        cap.set(color='#FFFFFF', linewidth=0)

    # print(plt.getp(bp['whiskers'][0]))

    # ax.set_ylim([0, 1])

    # Set only 3 ticks on x
    ax.set_xticks([1, n_revisions / 2, n_revisions], minor=False)
    ax.set_xticklabels([1, int(n_revisions / 2), n_revisions], fontdict=None, minor=False)

    # Remove extra spines and ticks
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_zorder(20)
    ax.spines['bottom'].set_zorder(20)
    ax.tick_params(axis='x', which='both', top='off', direction='out')
    ax.tick_params(axis='y', which='both', right='off', direction='out')

np.random.seed(937)
data = np.random.lognormal(size=(37, 4), mean=1.5, sigma=1.75)

fig, axs = plt.subplots(1,1, sharex=True, sharey=True, figsize=(10, 22))

# bp = plt.boxplot(data)
bp = fig.axes[0].boxplot(data, whis=[5, 95], showfliers=False, patch_artist=True, widths=1);

styleBoxplot(bp, fig.axes[0], 4)
a= 1
plt.show()
