# Copyright 2025 w.Sanice
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


LOCALE_ALIASES = {'en': 'en_US', 'pt': 'pt_BR', 'es': 'es_ES', 'hi': 'hi_IN', 'zh': 'zh_CN'}
LABEL_LANGUAGES = {'pt': 'pt_BR', 'es': 'es_ES', 'hi': 'hi_IN', 'zh_CN': 'zh_CN'}


class Leblanc(ABC):
    SEASONALITY = [1.0] * 12
    CUSTOMER_ID = 'customer_id'
    CUSTOMER_NAME = None

    def __init__(self, num_records, locale='en_US', seed=42, start_date=None, verbose=True,
                 seasonality=True, customers=None):
        if isinstance(num_records, bool) or not isinstance(num_records, (int, np.integer)) or num_records < 0:
            raise ValueError("num_records must be a non-negative integer")
        locale = LOCALE_ALIASES.get(locale, locale)
        if customers is not None:
            if not isinstance(customers, pd.DataFrame) or 'customer_id' not in customers.columns:
                raise ValueError("customers must be a DataFrame with a 'customer_id' column")
            if num_records > 0 and customers.empty:
                raise ValueError("customers must not be empty")
        self.num_records = int(num_records)
        self.locale = locale
        self.seed = seed
        self.verbose = verbose
        self.seasonality = seasonality
        self.customers = customers
        self.start_date = pd.Timestamp(start_date).to_pydatetime() if start_date is not None else None
        try:
            self.fake = Faker(locale)
        except AttributeError:
            raise ValueError(f"Unsupported locale '{locale}'")
        self._reset()

    def _label_key(self):
        language = self.locale.split('_')[0]
        return LABEL_LANGUAGES.get(language) or LABEL_LANGUAGES.get(self.locale)

    def _translator(self):
        return getattr(self, 'TRANSLATIONS', {}).get(self._label_key(), {})

    def _state(self):
        for name in ('state_abbr', 'state', 'administrative_unit'):
            method = getattr(self.fake, name, None)
            if method is not None:
                try:
                    return method()
                except AttributeError:
                    continue
        return ''

    def _season_factor(self, moment):
        if not self.seasonality:
            return 1.0
        return self.SEASONALITY[moment.month - 1] / (sum(self.SEASONALITY) / 12)

    def _reset(self):
        self.rng = np.random.default_rng(self.seed)
        self.py_rng = random.Random(self.seed)
        self.fake.seed_instance(self.seed)

    def _start(self, default):
        return self.start_date or default

    def _timeline(self, start, span_days=365):
        if self.seasonality and any(w != 1.0 for w in self.SEASONALITY):
            days = pd.date_range(start, periods=span_days, freq='D')
            weights = np.array([self.SEASONALITY[d.month - 1] for d in days], dtype=float)
            chosen = self.rng.choice(span_days, size=self.num_records, p=weights / weights.sum())
        else:
            chosen = self.rng.integers(0, span_days, self.num_records)
        hours = self.rng.integers(0, 24, self.num_records)
        offsets = np.sort(chosen * 24 + hours)
        return [start + timedelta(hours=int(h)) for h in offsets]

    def _apply_customers(self, df):
        if self.customers is None or df.empty:
            return df
        picks = self.rng.integers(0, len(self.customers), len(df))
        chosen = self.customers.iloc[picks].reset_index(drop=True)
        out = df.copy()
        out[self.CUSTOMER_ID] = chosen['customer_id'].to_numpy()
        if self.CUSTOMER_NAME and self.CUSTOMER_NAME in out.columns and 'customer_name' in chosen.columns:
            out[self.CUSTOMER_NAME] = chosen['customer_name'].to_numpy()
        for column in ('city', 'state'):
            if column in out.columns and column in chosen.columns:
                out[column] = chosen[column].to_numpy()
        return out

    @staticmethod
    def _as_list(columns):
        if columns is None:
            return []
        if isinstance(columns, str):
            return [columns]
        return list(columns)

    @staticmethod
    def _check_rate(rate, name):
        if not 0 <= rate <= 1:
            raise ValueError(f"{name} must be between 0 and 1")

    def _check_columns(self, df, columns):
        unknown = [c for c in columns if c not in df.columns]
        if unknown:
            raise ValueError(f"Unknown columns: {unknown}. Available: {list(df.columns)}")

    def inject_missing_values(self, df, columns, missing_rate=0.05):
        columns = self._as_list(columns)
        self._check_rate(missing_rate, "missing_rate")
        self._check_columns(df, columns)
        out = df.copy()
        for col in columns:
            mask = self.rng.random(len(out)) < missing_rate
            series = out[col]
            if pd.api.types.is_bool_dtype(series):
                series = series.astype('boolean')
            elif pd.api.types.is_integer_dtype(series):
                series = series.astype('float64')
            out[col] = series.mask(mask)
        return out

    def inject_outliers(self, df, columns, outlier_rate=0.01, factor=5.0):
        columns = self._as_list(columns)
        self._check_rate(outlier_rate, "outlier_rate")
        self._check_columns(df, columns)
        out = df.copy()
        for col in columns:
            if not pd.api.types.is_numeric_dtype(out[col]) or pd.api.types.is_bool_dtype(out[col]):
                raise ValueError(f"Column '{col}' is not numeric")
            mask = self.rng.random(len(out)) < outlier_rate
            values = out[col].astype('float64')
            values[mask] = values[mask] * factor
            out[col] = values
        return out

    def inject_duplicates(self, df, duplicate_rate=0.02):
        self._check_rate(duplicate_rate, "duplicate_rate")
        count = int(round(len(df) * duplicate_rate))
        if count == 0:
            return df.copy()
        picked = self.rng.choice(len(df), size=count, replace=False)
        order = np.sort(np.concatenate([np.arange(len(df)), picked]))
        return df.iloc[order].reset_index(drop=True)

    def export(self, df, path):
        target = Path(path)
        suffix = target.suffix.lower()
        if suffix == '.csv':
            df.to_csv(target, index=False)
        elif suffix == '.parquet':
            df.to_parquet(target, index=False)
        elif suffix == '.json':
            df.to_json(target, orient='records', date_format='iso')
        else:
            raise ValueError("Unsupported format. Use .csv, .parquet or .json")
        return target

    def _finalize(self, data, name, missing_data_cols, missing_rate, outlier_cols, duplicate_rate):
        df = pd.DataFrame(data)
        if not df.empty:
            df = self._apply_customers(df)
            if outlier_cols:
                df = self.inject_outliers(df, outlier_cols)
            if duplicate_rate:
                df = self.inject_duplicates(df, duplicate_rate)
            if missing_data_cols:
                df = self.inject_missing_values(df, missing_data_cols, missing_rate)
        if self.verbose:
            print(f"[Leblanc] {name} ({self.locale}): {len(df)} lines generated.")
        return df

    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        pass
