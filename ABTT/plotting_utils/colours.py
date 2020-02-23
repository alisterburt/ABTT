import seaborn as sns


def generate_categorical_colourblind(n_colours=6):
    palette = sns.color_palette('colorblind', n_colors=n_colours)
    return palette


def generate_categorical_pastel(n_colours=6):
    palette = sns.color_palette('pastel', n_colors=n_colours)
    return palette


def generate_categorical(n_colours=6):
    palette = sns.color_palette(n_colors=n_colours)
    return palette
