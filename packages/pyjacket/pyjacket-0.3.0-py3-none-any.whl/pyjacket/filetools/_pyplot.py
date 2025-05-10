import matplotlib.pyplot as plt

DEFAULT_DPI = 300

PyplotHandle = tuple[plt.Figure, plt.Axes]

def current_handle():
    return plt.gcf(), plt.gca()

def savefig(filepath: str, handle: PyplotHandle=None, close: bool=True, **kwargs):
    fig, ax = handle or current_handle()
    kwargs.setdefault("dpi", DEFAULT_DPI)

    fig.savefig(filepath, **kwargs)

    if close:
        plt.close(fig)
