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
        },
        'es_ES': {
            'Eucalyptus': 'Eucalipto',
            'Pinus': 'Pino',
            'Native': 'Nativa',
            'Intensive': 'Intensivo',
            'Sustainable': 'Sostenible',
            'Reforestation': 'Reforestación',
            'Northern': 'Norte',
            'Southern': 'Sur',
            'Coastal': 'Costa',
            'Eucalyptus Grandis': 'Eucalipto Grandis (Celulosa)',
            'Pinus Elliotti': 'Pino Elliottii (Aserradero)',
            'Native Hardwood': 'Madera Dura Nativa (Manejo)',
            'Biomass Wood': 'Madera para Biomasa',
            'm3': 'm3',
            'tons': 'toneladas'
        },
        'hi_IN': {
            'Eucalyptus': 'यूकेलिप्टस',
            'Pinus': 'चीड़',
            'Native': 'देशी',
            'Intensive': 'गहन',
            'Sustainable': 'टिकाऊ',
            'Reforestation': 'पुनर्वनीकरण',
            'Northern': 'उत्तरी',
            'Southern': 'दक्षिणी',
            'Coastal': 'तटीय',
            'Eucalyptus Grandis': 'यूकेलिप्टस ग्रैंडिस (लुगदी)',
            'Pinus Elliotti': 'पाइनस एलियोटी (आरा मिल)',
            'Native Hardwood': 'देशी कठोर लकड़ी (प्रबंधित)',
            'Biomass Wood': 'बायोमास लकड़ी',
            'm3': 'm3',
            'tons': 'टन'
        },
        'zh_CN': {
            'Eucalyptus': '桉树',
            'Pinus': '松树',
            'Native': '本地树种',
            'Intensive': '集约经营',
            'Sustainable': '可持续经营',
            'Reforestation': '再造林',
            'Northern': '北部',
            'Southern': '南部',
            'Coastal': '沿海',
            'Eucalyptus Grandis': '巨桉(纸浆)',
            'Pinus Elliotti': '湿地松(锯材)',
            'Native Hardwood': '本地硬木(经营)',
            'Biomass Wood': '生物质木材',
            'm3': '立方米',
            'tons': '吨'
        }
    }

    SEASONALITY = [0.7, 0.7, 0.8, 1.0, 1.1, 1.4, 1.6, 1.6, 1.4, 1.0, 0.8, 0.7]
    CUSTOMER_NAME = 'owner_name'

    def get_metadata(self):
        return {"description": "Forestry inventory and harvest data"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        prod_list = list(self.PRODUCTS_FORESTRY.keys())
        translator = self._translator()
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
                'customer_id': int(self.rng.integers(100, 9999)),
                'owner_name': self.fake.name()
            })

        return self._finalize(data, "Forestry & Timber", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
