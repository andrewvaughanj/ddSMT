import progressbar
import sys

__BAR = None


def start(max):
    """Initialize a new progress bar for at most ``max`` steps."""
    global __BAR
    if not sys.stdout.isatty():
        return
    widgets = [progressbar.Bar(), ' ', progressbar.Counter(), ' / ', str(max)]
    __BAR = progressbar.ProgressBar(maxval=max, widgets=widgets)
    __BAR.start()
    __BAR.update_interval = 1


def update(newval=None):
    """Update the current progress bar.

    The value is incremented by one, or set to newval if newval is not
    ``None``.
    """
    global __BAR
    if __BAR:
        if newval is not None:
            __BAR.update(min(newval, __BAR.maxval))
        else:
            __BAR.update(__BAR.currval + 1)


def finish():
    """Stop the current progress bar.

    Delete the object and write a newline.
    """
    global __BAR
    if __BAR:
        __BAR = None
        sys.stdout.write('\n')
