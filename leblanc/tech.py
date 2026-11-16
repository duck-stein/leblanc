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


class Tech(Leblanc):
    PRODUCTS_TECH = {
        'Gaming Laptop': {'category': 'Electronics', 'price': 7500.00},
        'Vertical Mouse': {'category': 'Accessories', 'price': 250.00},
        'Mechanical Keyboard': {'category': 'Accessories', 'price': 550.00},
        'Ultrawide Monitor': {'category': 'Electronics', 'price': 2800.00},
        'Gaming Chair': {'category': 'Furniture', 'price': 1200.00},
        'Headset 7.1': {'category': 'Accessories', 'price': 800.00},
        'Video Card': {'category': 'Hardware', 'price': 4500.00},
        'SSD 1TB': {'category': 'Hardware', 'price': 600.00}
    }

    TRANSLATIONS = {
        'pt_BR': {
            'Electronics': 'Eletrônicos', 'Accessories': 'Acessórios',
            'Furniture': 'Mobiliário', 'Hardware': 'Hardware',
            'Gaming Laptop': 'Notebook Gamer', 'Vertical Mouse': 'Mouse Vertical',
            'Mechanical Keyboard': 'Teclado Mecânico', 'Ultrawide Monitor': 'Monitor Ultrawide',
            'Gaming Chair': 'Cadeira Gamer', 'Headset 7.1': 'Fone de Ouvido 7.1',
            'Video Card': 'Placa de Vídeo'
        }
    }

    def get_metadata(self):
        return {
            "description": "Technology retail sales data",
            "products_count": len(self.PRODUCTS_TECH)
        }

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        sales_data = []
        product_list = list(self.PRODUCTS_TECH.keys())
        translator = self.TRANSLATIONS.get(self.locale, {})
        dates = self._timeline(self._start(datetime(2026, 1, 1)))

        for i in range(self.num_records):
            raw_product_name = self.py_rng.choice(product_list)
            product_info = self.PRODUCTS_TECH[raw_product_name]
            quantity = int(self.rng.integers(1, 8))

            if raw_product_name in ['Vertical Mouse', 'Mechanical Keyboard']:
                unit_price = round(float(product_info['price'] * self.rng.uniform(0.9, 1.0)), 2)
            else:
                unit_price = product_info['price']

            sales_data.append({
                'order_id': 1000 + i,
                'order_date': dates[i],
                'product_name': translator.get(raw_product_name, raw_product_name),
                'category': translator.get(product_info['category'], product_info['category']),
                'unit_price': unit_price,
                'quantity': quantity,
                'total_sale': round(unit_price * quantity, 2),
                'customer_id': int(self.rng.integers(100, 9999)),
                'city': self.fake.city(),
                'state': self.fake.state_abbr()
            })

        return self._finalize(sales_data, "Technology Sales", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
