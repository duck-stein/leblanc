import json

import numpy as np
import pandas as pd
import pytest

import leblanc
from leblanc import (
    Agribusiness, Apparel, Financial, Food, Forestry, HealthBeauty, Tech,
    get_sector, list_sectors,
)
from leblanc.__main__ import main

ALL = [Agribusiness, Apparel, Financial, Food, Forestry, HealthBeauty, Tech]
ARGS = dict(verbose=False)


@pytest.mark.parametrize("cls", ALL)
def test_build_shape_and_no_nulls(cls):
    df = cls(200, **ARGS).build()
    assert len(df) == 200
    assert not df.isnull().any().any()


@pytest.mark.parametrize("cls", ALL)
def test_rebuild_and_new_instance_are_identical(cls):
    generator = cls(150, **ARGS)
    first = generator.build()
    assert first.equals(generator.build())
    assert first.equals(cls(150, **ARGS).build())


@pytest.mark.parametrize("cls", ALL)
def test_seed_changes_output(cls):
    assert not cls(100, seed=1, **ARGS).build().equals(cls(100, seed=2, **ARGS).build())


@pytest.mark.parametrize("cls", ALL)
def test_missing_values_every_column_dtype(cls):
    clean = cls(300, **ARGS).build()
    df = cls(300, **ARGS).build(missing_data_cols=list(clean.columns), missing_rate=0.2)
    for column in clean.columns:
        assert df[column].isnull().sum() > 0, column


def test_missing_rate_zero_and_one():
    assert Apparel(100, **ARGS).build(missing_data_cols=['return_flag'], missing_rate=0).return_flag.isnull().sum() == 0
    assert Apparel(100, **ARGS).build(missing_data_cols=['return_flag'], missing_rate=1).return_flag.isnull().all()


def test_unknown_column_and_bad_rate_raise():
    with pytest.raises(ValueError):
        Tech(10, **ARGS).build(missing_data_cols=['nope'])
    with pytest.raises(ValueError):
        Tech(10, **ARGS).build(missing_data_cols=['total_sale'], missing_rate=1.5)


@pytest.mark.parametrize("value", [-1, 1.5, "10", True])
def test_invalid_num_records(value):
    with pytest.raises(ValueError):
        Tech(value, **ARGS)


def test_zero_records_returns_empty_frame():
    assert Tech(0, **ARGS).build(missing_data_cols=['total_sale']).empty


def test_verbose_flag(capsys):
    Tech(5, verbose=False).build()
    assert capsys.readouterr().out == ""
    Tech(5).build()
    assert "[Leblanc]" in capsys.readouterr().out


def test_food_total_matches_unit_times_quantity():
    df = Food(1000, **ARGS).build()
    assert np.allclose(df.unit_price * df.quantity, df.total_sale, atol=0.011)


@pytest.mark.parametrize("cls,total", [(Tech, 'total_sale'), (Apparel, 'total_sale')])
def test_sales_totals_consistent(cls, total):
    df = cls(1000, **ARGS).build()
    assert np.allclose(df.unit_price * df.quantity, df[total], atol=0.011)


@pytest.mark.parametrize("cls,col", [(Tech, 'order_date'), (Apparel, 'transaction_date'), (Agribusiness, 'record_date')])
def test_dates_sorted_and_within_a_year(cls, col):
    df = cls(5000, **ARGS).build()
    assert df[col].is_monotonic_increasing
    assert (df[col].max() - df[col].min()).days <= 366


def test_start_date_is_respected():
    df = Tech(100, start_date="2030-05-01", **ARGS).build()
    assert df.order_date.min() >= pd.Timestamp("2030-05-01")
    assert df.order_date.max() < pd.Timestamp("2031-06-01")


def test_forestry_revenue_and_volume_are_coherent():
    df = Forestry(1000, **ARGS).build()
    prices = {'Eucalyptus Grandis': 80, 'Pinus Elliotti': 150, 'Native Hardwood': 400, 'Biomass Wood': 50}
    expected = df.product_name.map(prices)
    assert np.allclose(df.estimated_revenue / df.total_estimated_volume, expected, rtol=1e-3)
    per_hectare = df.total_estimated_volume / df.area_hectares
    assert per_hectare.max() < 1000


def test_financial_clients_repeat_and_checking_never_defaults():
    df = Financial(2000, **ARGS).build()
    assert df.client_id.nunique() > 100
    assert df.client_id.duplicated().any()
    assert not df[df.financial_product == 'Checking Account'].is_default.any()


def test_pt_br_translation():
    df = Tech(300, locale='pt_BR', **ARGS).build()
    assert 'Eletrônicos' in set(df.category)
    assert 'Fone de Ouvido 7.1' in set(df.product_name)
    forestry = Forestry(300, locale='pt_BR', **ARGS).build()
    assert set(forestry.volume_unit) <= {'m3', 'toneladas'}


def test_outliers_increase_maximum():
    base = Tech(2000, **ARGS).build()
    df = Tech(2000, **ARGS).build(outlier_cols=['total_sale'])
    assert df.total_sale.max() > base.total_sale.max()


def test_duplicates_added():
    df = Tech(500, **ARGS).build(duplicate_rate=0.1)
    assert len(df) == 550
    assert df.duplicated().sum() == 50


def test_outliers_reject_non_numeric():
    with pytest.raises(ValueError):
        Tech(10, **ARGS).build(outlier_cols=['city'])


def test_export_formats(tmp_path):
    generator = Tech(50, **ARGS)
    df = generator.build()
    generator.export(df, tmp_path / "a.csv")
    assert len(pd.read_csv(tmp_path / "a.csv")) == 50
    generator.export(df, tmp_path / "a.json")
    assert len(json.loads((tmp_path / "a.json").read_text())) == 50
    with pytest.raises(ValueError):
        generator.export(df, tmp_path / "a.txt")


def test_registry():
    assert "forestry" in list_sectors()
    assert get_sector("Health_Beauty") is HealthBeauty
    with pytest.raises(ValueError):
        get_sector("unknown")


def test_cli(tmp_path, capsys):
    out = tmp_path / "out.csv"
    main(["financial", "-n", "30", "-o", str(out), "--missing", "contracted_value", "--missing-rate", "0.5"])
    df = pd.read_csv(out)
    assert len(df) == 30
    assert df.contracted_value.isnull().any()
    assert "30 rows written" in capsys.readouterr().out


def test_version_matches_setup():
    import re
    from pathlib import Path
    setup_text = Path(__file__).resolve().parent.parent.joinpath("setup.py").read_text()
    assert "__version__" in setup_text
    assert re.fullmatch(r"\d+\.\d+\.\d+", leblanc.__version__)
