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


class Apparel(Leblanc):

    PRODUCTS_APPAREL = {
        'Slim Fit Jeans': {'category': 'Bottom Wear', 'price': 180.00},
        'Basic Cotton T-Shirt': {'category': 'Top Wear', 'price': 60.00},
        'Casual Running Shoes': {'category': 'Footwear', 'price': 320.00},
        'Summer Midi Dress': {'category': 'Womenswear', 'price': 150.00},
        'Dress Socks (Pair)': {'category': 'Accessories', 'price': 15.00},
    }
    SIZES = ['XS', 'S', 'M', 'L', 'XL']
    COLORS = ['Black', 'White', 'Navy Blue', 'Grey', 'Red']

    TRANSLATIONS = {
        'pt_BR': {
            'Bottom Wear': 'Calças/Inferior', 'Top Wear': 'Camisas/Superior', 'Footwear': 'Calçados',
            'Womenswear': 'Moda Feminina', 'Accessories': 'Acessórios',
            'Slim Fit Jeans': 'Calça Jeans Slim', 'Basic Cotton T-Shirt': 'Camiseta de Algodão',
            'Casual Running Shoes': 'Tênis de Corrida Casual', 'Summer Midi Dress': 'Vestido Midi de Verão',
            'Dress Socks (Pair)': 'Meias Sociais (Par)',
            'Black': 'Preto', 'White': 'Branco', 'Navy Blue': 'Azul Marinho', 'Grey': 'Cinza', 'Red': 'Vermelho'
        }
    }

    def get_metadata(self):
        return {"description": "Apparel and Fashion sales data"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        sales_data = []
        product_list = list(self.PRODUCTS_APPAREL.keys())
        translator = self.TRANSLATIONS.get(self.locale, {})
        dates = self._timeline(self._start(datetime(2025, 9, 1)))

        for i in range(self.num_records):
            raw_prod = self.py_rng.choice(product_list)
            raw_color = self.py_rng.choice(self.COLORS)
            info = self.PRODUCTS_APPAREL[raw_prod]
            order_date = dates[i]
            if order_date.month in [10, 11, 12]:
                quantity = int(self.rng.integers(1, 10))
            else:
                quantity = int(self.rng.integers(1, 5))
            unit_price = round(float(info['price'] * self.rng.uniform(0.9, 1.1)), 2)

            sales_data.append({
                'transaction_id': 3000 + i,
                'transaction_date': order_date,
                'product': translator.get(raw_prod, raw_prod),
                'category': translator.get(info['category'], info['category']),
                'unit_price': unit_price,
                'quantity': quantity,
                'total_sale': round(unit_price * quantity, 2),
                'size': self.py_rng.choice(self.SIZES),
                'color': translator.get(raw_color, raw_color),
                'customer_id': int(self.rng.integers(100, 9999)),
                'return_flag': bool(self.rng.random() < 0.15)
            })

        return self._finalize(sales_data, "Apparel & Fashion", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
