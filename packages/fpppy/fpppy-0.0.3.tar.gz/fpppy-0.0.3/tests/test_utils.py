import pandas as pd


def test_import_plot_series():
    from fpppy.utils import plot_series

    aus_production = pd.read_csv("../data/aus_production.csv", parse_dates=["ds"])
    ausbeer2 = aus_production.query('ds >= "2000-01-01"')[["ds", "Beer"]]
    ausbeer2.insert(0, "unique_id", "Beer")
    ausbeer2.rename(columns={"Beer": "y"}, inplace=True)
    plot_series(ausbeer2)
