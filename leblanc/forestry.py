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


class Forestry(Leblanc):

    PRODUCTS_FORESTRY = {
        'Eucalyptus Grandis': {'species': 'Eucalyptus', 'target_age': 7, 'unit': 'm3', 'yield_per_ha': 300, 'price': 80},
        'Pinus Elliotti': {'species': 'Pinus', 'target_age': 18, 'unit': 'm3', 'yield_per_ha': 400, 'price': 150},
        'Native Hardwood': {'species': 'Native', 'target_age': 30, 'unit': 'm3', 'yield_per_ha': 150, 'price': 400},
        'Biomass Wood': {'species': 'Eucalyptus', 'target_age': 5, 'unit': 'tons', 'yield_per_ha': 200, 'price': 50},
    }
    MANAGEMENT = ['Intensive', 'Sustainable', 'Reforestation']
    REGIONS = ['Northern', 'Southern', 'Coastal']

    TRANSLATIONS = {
        'pt_BR': {
            'Eucalyptus': 'Eucalipto', 'Pinus': 'Pinus', 'Native': 'Nativa',
            'Intensive': 'Intensivo', 'Sustainable': 'Sustentável', 'Reforestation': 'Reflorestamento',
            'Northern': 'Norte', 'Southern': 'Sul', 'Coastal': 'Litoral',
            'Eucalyptus Grandis': 'Eucalipto Grandis (Celulose)', 'Pinus Elliotti': 'Pinus (Serraria)',
            'Native Hardwood': 'Madeira de Lei (Manejo)', 'Biomass Wood': 'Madeira para Biomassa',
            'm3': 'm3', 'tons': 'toneladas'
        }
    }

    def get_metadata(self):
        return {"description": "Forestry inventory and harvest data"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        prod_list = list(self.PRODUCTS_FORESTRY.keys())
        translator = self.TRANSLATIONS.get(self.locale, {})
        dates = self._timeline(self._start(datetime(2025, 1, 1)))

        for i in range(self.num_records):
            raw_prod = self.py_rng.choice(prod_list)
            info = self.PRODUCTS_FORESTRY[raw_prod]
            raw_mgmt = self.py_rng.choice(self.MANAGEMENT)
            raw_reg = self.py_rng.choice(self.REGIONS)
            area = float(self.rng.uniform(100, 5000))
            age = int(self.rng.integers(1, info['target_age'] * 2))
            age_factor = min(age / info['target_age'], 1.5)
            mgmt_factor = {'Intensive': 1.1, 'Sustainable': 1.0, 'Reforestation': 0.9}[raw_mgmt]
            total_vol = info['yield_per_ha'] * age_factor * mgmt_factor * area * self.rng.uniform(0.9, 1.1)
            revenue = total_vol * info['price']

            data.append({
                'inventory_id': 6000 + i,
                'record_date': dates[i],
                'product_name': translator.get(raw_prod, raw_prod),
                'species': translator.get(info['species'], info['species']),
                'region': translator.get(raw_reg, raw_reg),
                'area_hectares': round(area, 2),
                'planting_age_years': age,
                'management_type': translator.get(raw_mgmt, raw_mgmt),
                'volume_unit': translator.get(info['unit'], info['unit']),
                'total_estimated_volume': round(float(total_vol), 2),
                'estimated_revenue': round(float(revenue), 2),
                'owner_name': self.fake.name()
            })

        return self._finalize(data, "Forestry & Timber", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
