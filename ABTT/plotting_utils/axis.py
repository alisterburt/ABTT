import logging


def hide_spines(ax, spines=('top', 'right')):
    """
    Hide the spines of a matplotlib axis object
    :param ax: matplotlib.axis
    :param spines: list of spines to hide, default is ['top', 'right']
    :return: None
    """
    logging.info('hiding spines in matplotlib axis')
    for spine in spines:
        ax.spines[spine].set_visible(False)

    return None


def show_spines(ax, spines=('top', 'right')):
    """
    Hide the spines of a matplotlib axis object
    :param ax: matplotlib.axis
    :param spines: list of spines to hide, default is ['top', 'right']
    :return: None
    """
    logging.info('hiding spines in matplotlib axis')
    for spine in spines:
        ax.spines[spine].set_visible(True)

    return None


def title_size(ax, fontsize):
    """
    change axis title size
    :param ax: matplotlib.axis
    :param fontsize: new title size
    :return: None
    """
    title = ax.get_title()
    ax.set_title(title, fontsize=fontsize)
    return None


def axis_label_size(ax, fontsize, axes=('x', 'y')):
    """
    Change axis label sizes for matplotlib axis
    :param ax: matplotlib.axis
    :param fontsize: new fontsize
    :param axes: list of axes to modify label size, default is ['x','y']
    :return: None
    """
    logging.info('changing axis label sizes in matplotlib axis')
    for axis in axes:
        if axis == 'x':
            ax.xaxis.label.set_fontsize(fontsize)

        elif axis == 'y':
            ax.yaxis.label.set_fontsize(fontsize)

        elif axis == 'z':
            ax.zaxis.label.set_fontsize(fontsize)

    return None


def ticklabel_size(ax, fontsize, axes=('x', 'y')):
    """
    Change ticklabel size for matplotlib axis on given axes.
    :param ax: matplotlib.axis
    :param fontsize: new fontsize
    :param axes: list of axes to modify ticklabel size, default is ['x','y']
    :return: None
    """
    logging.info('changing axis ticklabel sizes in matplotlib axis')
    for axis in axes:
        if axis == 'x':
            for item in ax.get_xticklabels():
                item.set_fontsize(fontsize)

        elif axis == 'y':
            for item in ax.get_yticklabels():
                item.set_fontsize(fontsize)

    return None


def axis_thickness(ax, new_thickness):
    """
    change x and y axis and ticklabel thickness for a matplotlib axis object
    :param ax: matplotlib.axis
    :param new_thickness: desired axis thickness
    :return: None
    """
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(new_thickness)
    ax.xaxis.set_tick_params(width=new_thickness * 0.75, length=6)
    ax.yaxis.set_tick_params(width=new_thickness * 0.75, length=6)

    return None


def raise_spines(ax):
    """
    raises spines above everything else in plot
    :param ax: matplotlib.axis
    :return: None
    """
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].zorder = 999999


def hide_ticklabels(ax, axes=('x', 'y')):
    """
    hide axes of a matplotlib axis object
    :param ax: matplotlib.axis
    :param axes: ('x','y') or ('x') or ('y')
    :return: None
    """
    for axis in axes:
        if axis == 'x':
            ax.set_xticklabels([])

        elif axis == 'y':
            ax.set_yticklabels([])

    return None


def hide_ticks(ax, axes=('x', 'y')):
    """
    hide ticks of a matplotlib axis object
    :param ax: matplotlib.axis
    :param axes: ('x','y') or ('x') or ('y')
    :return: None
    """
    for axis in axes:
        if axis == 'x':
            ax.set_xticks([])

        elif axis == 'y':
            ax.set_yticks([])

    return None


def hide_ticks_and_ticklabels(ax, axes=('x', 'y')):
    """
    hide ticks and ticklabels of a matplotlib axis object
    :param ax: matplotlib.axis
    :param axes: ('x','y') or ('x') or ('y')
    :return: None
    """
    hide_ticks(ax, axes)
    hide_ticklabels(ax, axes)

    return None
