import json

import numpy as np
import pandas as pd
import pytest

import leblanc
from leblanc import (
    Agribusiness, Apparel, Education, Energy, Financial, Food, Forestry, Healthcare,
    HealthBeauty, Logistics, RealEstate, Tech, Warehouse, get_sector, list_sectors,
)
from leblanc.__main__ import main

ALL = [Agribusiness, Apparel, Education, Energy, Financial, Food, Forestry, Healthcare, HealthBeauty,
       Logistics, RealEstate, Tech]
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


LANGS = ['pt_BR', 'es_ES', 'hi_IN', 'zh_CN']
FREE_TEXT = {'city', 'state', 'customer_name', 'owner_name', 'farm_owner', 'email', 'delivery_zipcode',
             'production_unit', 'size'}


@pytest.mark.parametrize("cls", ALL)
@pytest.mark.parametrize("lang", LANGS)
def test_every_label_is_translated(cls, lang):
    df = cls(1500, **ARGS).build()
    labels = cls.TRANSLATIONS[lang]
    for column in df.columns:
        if column in FREE_TEXT or pd.api.types.is_numeric_dtype(df[column]) or pd.api.types.is_bool_dtype(df[column]):
            continue
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            continue
        for value in df[column].unique():
            assert value in labels or value == 'SSD 1TB', (cls.__name__, lang, column, value)


@pytest.mark.parametrize("locale", ['en_US', 'en_GB', 'en_IN', 'pt_BR', 'es_ES', 'es_MX', 'hi_IN', 'zh_CN', 'es', 'hi', 'zh', 'en', 'pt'])
@pytest.mark.parametrize("cls", ALL)
def test_all_locales_build(cls, locale):
    assert len(cls(60, locale=locale, **ARGS).build()) == 60


def test_translated_values_appear():
    assert set(Tech(400, locale='es_ES', **ARGS).build().category) <= {'Electrónica', 'Accesorios', 'Mobiliario', 'Hardware'}
    assert set(Financial(400, locale='hi_IN', **ARGS).build().client_risk_level) == {'कम', 'मध्यम', 'उच्च'}
    assert set(Healthcare(400, locale='zh_CN', **ARGS).build().department) >= {'全科', '放射科'}


def test_invalid_locale_raises():
    with pytest.raises(ValueError):
        Tech(10, locale='xx_YY', **ARGS)


def test_seasonality_concentrates_records():
    on = Tech(6000, **ARGS).build()
    off = Tech(6000, seasonality=False, **ARGS).build()
    share_on = on.order_date.dt.month.isin([11, 12]).mean()
    share_off = off.order_date.dt.month.isin([11, 12]).mean()
    assert share_on > share_off + 0.07


def test_energy_consumption_follows_season():
    df = Energy(6000, **ARGS).build()
    df = df[df.tariff_class == 'Residential']
    monthly = df.groupby(df.reading_date.dt.month).consumption_kwh.mean()
    assert monthly.loc[[1, 2]].mean() > monthly.loc[[6, 7]].mean()


def test_new_sector_rules():
    health = Healthcare(1000, **ARGS).build()
    assert np.allclose(health.billed_amount - health.covered_amount, health.patient_amount, atol=0.011)
    logistics = Logistics(1000, **ARGS).build()
    assert (logistics.delayed == (logistics.delivery_days > logistics.promised_days)).all()
    education = Education(1000, **ARGS).build()
    assert education.final_grade.between(0, 100).all()
    assert not education[education.completed].attendance_rate.lt(0.7).any()
    estate = RealEstate(1000, **ARGS).build()
    rents = estate[estate.transaction_type == 'Rent'].price_per_m2.mean()
    sales = estate[estate.transaction_type == 'Sale'].price_per_m2.mean()
    assert sales > rents * 50


def test_customers_pool_links_tables():
    customers = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'customer_name': ['A', 'B', 'C'],
        'city': ['X', 'Y', 'Z'],
        'state': ['S1', 'S2', 'S3'],
    })
    tech = Tech(100, customers=customers, **ARGS).build()
    assert set(tech.customer_id) <= {1, 2, 3}
    assert (tech.city == tech.customer_id.map({1: 'X', 2: 'Y', 3: 'Z'})).all()
    bank = Financial(100, customers=customers, **ARGS).build()
    assert set(bank.client_id) <= {1, 2, 3}
    food = Food(100, customers=customers, **ARGS).build()
    assert (food.customer_name == food.customer_id.map({1: 'A', 2: 'B', 3: 'C'})).all()
    with pytest.raises(ValueError):
        Tech(10, customers=pd.DataFrame({'id': [1]}), **ARGS)
    with pytest.raises(ValueError):
        Tech(10, customers=customers.iloc[0:0], **ARGS)


def test_warehouse_integrity_and_reproducibility(tmp_path):
    warehouse = Warehouse(80, locale='pt_BR', verbose=False)
    tables = warehouse.build(sectors=['tech', 'financial', 'healthcare', 'education'], records=200)
    assert set(tables) == {'customers', 'tech', 'financial', 'healthcare', 'education'}
    assert len(tables['customers']) == 80
    assert all(warehouse.check_integrity(tables).values())
    again = Warehouse(80, locale='pt_BR', verbose=False).build(sectors=['tech', 'financial', 'healthcare', 'education'], records=200)
    assert all(tables[k].equals(again[k]) for k in tables)
    paths = warehouse.export(tables, tmp_path / "out")
    assert len(paths) == 5
    with pytest.raises(ValueError):
        warehouse.export(tables, tmp_path, fmt="xml")


def test_warehouse_cli(tmp_path, capsys):
    main(["warehouse", "-n", "30", "-o", str(tmp_path / "wh")])
    assert len(list((tmp_path / "wh").glob("*.csv"))) == 13
    assert "13 tables written" in capsys.readouterr().out


def test_cli_new_sector_and_no_seasonality(tmp_path):
    out = tmp_path / "e.csv"
    main(["energy", "-n", "40", "-o", str(out), "--locale", "zh_CN", "--no-seasonality"])
    assert len(pd.read_csv(out)) == 40
