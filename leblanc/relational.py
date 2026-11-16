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

from datetime import datetime, timedelta
from pathlib import Path

from .base import Leblanc


class Customers(Leblanc):

    def get_metadata(self):
        return {"description": "Customer dimension shared by related sector tables"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        reference = self._start(datetime(2025, 1, 1))
        data = []
        for i in range(self.num_records):
            data.append({
                'customer_id': 10000 + i,
                'customer_name': self.fake.name(),
                'email': self.fake.email(),
                'city': self.fake.city(),
                'state': self._state(),
                'signup_date': reference - timedelta(days=int(self.rng.integers(1, 731)))
            })
        return self._finalize(data, "Customers", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)


class Warehouse:
    def __init__(self, num_customers=1000, locale='en_US', seed=42, start_date=None, verbose=True, seasonality=True):
        self.num_customers = num_customers
        self.locale = locale
        self.seed = seed
        self.start_date = start_date
        self.verbose = verbose
        self.seasonality = seasonality
        self.customers = None

    def build(self, sectors=None, records=None):
        from . import SECTORS, get_sector

        chosen = [get_sector(s) for s in sectors] if sectors else [SECTORS[k] for k in sorted(SECTORS)]
        customers = Customers(
            self.num_customers, locale=self.locale, seed=self.seed,
            start_date=self.start_date, verbose=self.verbose,
        ).build()
        self.customers = customers
        tables = {'customers': customers}
        for index, sector in enumerate(chosen, start=1):
            if isinstance(records, dict):
                count = records.get(sector.__name__.lower(), self.num_customers * 3)
            elif records is None:
                count = self.num_customers * 3
            else:
                count = records
            tables[sector.__name__.lower()] = sector(
                count, locale=self.locale, seed=self.seed + index, start_date=self.start_date,
                verbose=self.verbose, seasonality=self.seasonality, customers=customers,
            ).build()
        return tables

    def check_integrity(self, tables):
        valid = set(tables['customers']['customer_id'])
        report = {}
        for name, df in tables.items():
            if name == 'customers':
                continue
            key = next(k for k in ('customer_id', 'client_id', 'patient_id', 'student_id') if k in df.columns)
            report[name] = bool(df[key].isin(valid).all())
        return report

    def export(self, tables, directory, fmt='csv'):
        if fmt not in ('csv', 'parquet', 'json'):
            raise ValueError("Unsupported format. Use csv, parquet or json")
        target = Path(directory)
        target.mkdir(parents=True, exist_ok=True)
        paths = []
        for name, df in tables.items():
            path = target / f"{name}.{fmt}"
            if fmt == 'csv':
                df.to_csv(path, index=False)
            elif fmt == 'parquet':
                df.to_parquet(path, index=False)
            else:
                df.to_json(path, orient='records', date_format='iso')
            paths.append(path)
        return paths
