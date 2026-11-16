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


class RealEstate(Leblanc):

    PROPERTIES = {
        'Apartment': {'price_m2': 7500.0, 'area': (40, 140), 'bedrooms': (1, 4)},
        'House': {'price_m2': 6000.0, 'area': (90, 400), 'bedrooms': (2, 6)},
        'Commercial Room': {'price_m2': 9000.0, 'area': (30, 200), 'bedrooms': (0, 1)},
        'Land': {'price_m2': 1500.0, 'area': (250, 2000), 'bedrooms': (0, 1)},
        'Studio': {'price_m2': 9500.0, 'area': (20, 45), 'bedrooms': (0, 1)},
    }
    ZONES = {'Downtown': 1.2, 'Suburb': 0.9, 'Waterfront': 1.5, 'Rural': 0.6}
    TRANSACTIONS = ['Sale', 'Rent']
    RENT_YIELD = 0.005

    SEASONALITY = [0.9, 0.9, 1.1, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0, 1.0, 0.9, 0.7]

    TRANSLATIONS = {
        'pt_BR': {
            'Apartment': 'Apartamento', 'House': 'Casa', 'Commercial Room': 'Sala Comercial', 'Land': 'Terreno', 'Studio': 'Studio',
            'Sale': 'Venda', 'Rent': 'Aluguel',
            'Downtown': 'Centro', 'Suburb': 'Subúrbio', 'Waterfront': 'Beira-mar', 'Rural': 'Zona Rural'
        },
        'es_ES': {
            'Apartment': 'Apartamento', 'House': 'Casa', 'Commercial Room': 'Local Comercial', 'Land': 'Terreno', 'Studio': 'Estudio',
            'Sale': 'Venta', 'Rent': 'Alquiler',
            'Downtown': 'Centro', 'Suburb': 'Periferia', 'Waterfront': 'Frente al Mar', 'Rural': 'Zona Rural'
        },
        'hi_IN': {
            'Apartment': 'अपार्टमेंट', 'House': 'मकान', 'Commercial Room': 'वाणिज्यिक कार्यालय', 'Land': 'भूखंड', 'Studio': 'स्टूडियो',
            'Sale': 'बिक्री', 'Rent': 'किराया',
            'Downtown': 'शहर का केंद्र', 'Suburb': 'उपनगर', 'Waterfront': 'समुद्र किनारा', 'Rural': 'ग्रामीण क्षेत्र'
        },
        'zh_CN': {
            'Apartment': '公寓', 'House': '独栋住宅', 'Commercial Room': '商用房', 'Land': '土地', 'Studio': '单间公寓',
            'Sale': '出售', 'Rent': '出租',
            'Downtown': '市中心', 'Suburb': '郊区', 'Waterfront': '滨海', 'Rural': '乡村'
        }
    }

    def get_metadata(self):
        return {"description": "Property listings for sale and rent", "property_types": list(self.PROPERTIES.keys())}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        properties = list(self.PROPERTIES.keys())
        zones = list(self.ZONES.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 1, 1)))

        for i in range(self.num_records):
            raw_type = self.py_rng.choice(properties)
            info = self.PROPERTIES[raw_type]
            raw_zone = self.py_rng.choice(zones)
            raw_transaction = self.py_rng.choices(self.TRANSACTIONS, weights=[0.55, 0.45])[0]
            area = float(self.rng.uniform(*info['area']))
            value = info['price_m2'] * area * self.ZONES[raw_zone] * float(self.rng.uniform(0.85, 1.15))
            if raw_transaction == 'Rent':
                value *= self.RENT_YIELD
            days_on_market = int(self.rng.exponential(60 if raw_transaction == 'Sale' else 25)) + 1
            low, high = info['bedrooms']

            data.append({
                'listing_id': 13000 + i,
                'listing_date': dates[i],
                'property_type': translator.get(raw_type, raw_type),
                'transaction_type': translator.get(raw_transaction, raw_transaction),
                'zone': translator.get(raw_zone, raw_zone),
                'area_m2': round(area, 1),
                'bedrooms': int(self.rng.integers(low, high + 1)),
                'price': round(float(value), 2),
                'price_per_m2': round(float(value / area), 2),
                'days_on_market': days_on_market,
                'closed': bool(days_on_market < 120),
                'customer_id': int(self.rng.integers(100, 9999))
            })

        return self._finalize(data, "Real Estate", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
