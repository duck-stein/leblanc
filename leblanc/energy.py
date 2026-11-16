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

from .base import Leblanc
from datetime import datetime


class Energy(Leblanc):

    TARIFFS = {
        'Residential': {'avg_kwh': 250, 'price_kwh': 0.85},
        'Commercial': {'avg_kwh': 1800, 'price_kwh': 0.95},
        'Industrial': {'avg_kwh': 25000, 'price_kwh': 0.55},
        'Rural': {'avg_kwh': 400, 'price_kwh': 0.70},
    }
    SOURCES = ['Hydro', 'Solar', 'Wind', 'Thermal']
    REGIONS = ['North', 'South', 'East', 'West', 'Central']

    SEASONALITY = [1.2, 1.2, 1.1, 1.0, 0.9, 0.9, 0.9, 0.9, 1.0, 1.0, 1.1, 1.2]

    TRANSLATIONS = {
        'pt_BR': {
            'Residential': 'Residencial', 'Commercial': 'Comercial', 'Industrial': 'Industrial', 'Rural': 'Rural',
            'Hydro': 'Hídrica', 'Solar': 'Solar', 'Wind': 'Eólica', 'Thermal': 'Térmica',
            'North': 'Norte', 'South': 'Sul', 'East': 'Leste', 'West': 'Oeste', 'Central': 'Centro'
        },
        'es_ES': {
            'Residential': 'Residencial', 'Commercial': 'Comercial', 'Industrial': 'Industrial', 'Rural': 'Rural',
            'Hydro': 'Hidráulica', 'Solar': 'Solar', 'Wind': 'Eólica', 'Thermal': 'Térmica',
            'North': 'Norte', 'South': 'Sur', 'East': 'Este', 'West': 'Oeste', 'Central': 'Centro'
        },
        'hi_IN': {
            'Residential': 'आवासीय', 'Commercial': 'वाणिज्यिक', 'Industrial': 'औद्योगिक', 'Rural': 'ग्रामीण',
            'Hydro': 'जलविद्युत', 'Solar': 'सौर', 'Wind': 'पवन', 'Thermal': 'ताप',
            'North': 'उत्तर', 'South': 'दक्षिण', 'East': 'पूर्व', 'West': 'पश्चिम', 'Central': 'मध्य'
        },
        'zh_CN': {
            'Residential': '居民用电', 'Commercial': '商业用电', 'Industrial': '工业用电', 'Rural': '农村用电',
            'Hydro': '水电', 'Solar': '太阳能', 'Wind': '风电', 'Thermal': '火电',
            'North': '北部', 'South': '南部', 'East': '东部', 'West': '西部', 'Central': '中部'
        }
    }

    def get_metadata(self):
        return {"description": "Electricity consumption and billing readings", "tariffs": list(self.TARIFFS.keys())}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        tariffs = list(self.TARIFFS.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 1, 1)))

        for i in range(self.num_records):
            raw_tariff = self.py_rng.choice(tariffs)
            info = self.TARIFFS[raw_tariff]
            raw_source = self.py_rng.choice(self.SOURCES)
            raw_region = self.py_rng.choice(self.REGIONS)
            consumption = float(info['avg_kwh'] * self._season_factor(dates[i]) * self.rng.lognormal(0, 0.3))
            price = round(float(info['price_kwh'] * self.rng.uniform(0.95, 1.05)), 4)
            amount = round(consumption * price, 2)
            peak = float(consumption / 720 * self.rng.uniform(1.5, 3.0))

            data.append({
                'reading_id': 11000 + i,
                'reading_date': dates[i],
                'customer_id': int(self.rng.integers(100, 9999)),
                'tariff_class': translator.get(raw_tariff, raw_tariff),
                'region': translator.get(raw_region, raw_region),
                'energy_source': translator.get(raw_source, raw_source),
                'consumption_kwh': round(consumption, 2),
                'price_per_kwh': price,
                'amount_due': amount,
                'peak_demand_kw': round(peak, 2),
                'outage_minutes': int(self.rng.poisson(12 if raw_tariff == 'Rural' else 4)),
                'late_payment': bool(self.rng.random() < 0.08)
            })

        return self._finalize(data, "Energy", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
