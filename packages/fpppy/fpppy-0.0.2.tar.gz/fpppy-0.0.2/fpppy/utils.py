import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from utilsforecast.plotting import plot_series as _plot_series


def plot_series(*args, **kwargs):
    title = kwargs.pop("title", None)
    xlabel = kwargs.pop("xlabel", None)
    ylabel = kwargs.pop("ylabel", None)
    rm_legend = kwargs.pop("rm_legend", True)
    ax = kwargs.get("ax", None)

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(15, 6))
        kwargs["ax"] = ax

    fig = _plot_series(*args, **kwargs)
    for ax in fig.axes:
        if isinstance(title, str):
            ax.set_title(title, fontsize=25)
        else:
            ax.title.set_fontsize(25)
        if isinstance(xlabel, str):
            ax.set_xlabel(xlabel, fontsize=20)
        else:
            ax.xaxis.label.set_fontsize(20)
        if isinstance(ylabel, str):
            ax.set_ylabel(ylabel, fontsize=20)
        else:
            ax.yaxis.label.set_fontsize(20)
        ax.tick_params(axis="both", labelsize=15)
        for label in ax.get_xticklabels():
            label.set_rotation(0)
    fig.legends = []
    if not rm_legend:
        handles, labels = fig.axes[0].get_legend_handles_labels()
        fig.legend(
            handles, labels, loc="upper right", bbox_to_anchor=(1, 1), frameon=False
        )
    fig.show()
    return fig


def plot_series_stacked(*args, **kwargs):
    fig = _plot_series(*args, **kwargs)
    for ax in fig.axes:
        ax.title.set_fontsize(25)
        ax.xaxis.label.set_fontsize(20)
        ax.yaxis.label.set_fontsize(20)
        ax.tick_params(axis="both", labelsize=15)
        for label in ax.get_xticklabels():
            label.set_rotation(0)
    fig.show()
    return fig


def plot_diagnostics(data):
    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(2, 2, (1, 2))
    ax1.plot(data["ds"], data["resid"])
    ax1.set_title("Innovation Residuals")

    ax2 = fig.add_subplot(2, 2, 3)
    plot_acf(data["resid"].dropna(), ax=ax2, zero=False, bartlett_confint=False)
    ax2.set_title("ACF Plot")
    ax2.set_xlabel("lag[1]")

    ax3 = fig.add_subplot(2, 2, 4)
    ax3.hist(data["resid"], bins=20)
    ax3.set_title("Histogram")
    ax3.set_xlabel(".resid")
    ax3.set_ylabel("Count")

    plt.tight_layout()
    plt.show()
