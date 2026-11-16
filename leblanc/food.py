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
from datetime import datetime, timedelta


class Food(Leblanc):

    PRODUCTS_FOOD = {
        'Whole Milk 1L': {'category': 'Dairy', 'price': 5.50, 'perishable': True},
        'Roasted Coffee 500g': {'category': 'Grocery', 'price': 18.00, 'perishable': False},
        'Beef Tenderloin (kg)': {'category': 'Meat', 'price': 65.00, 'perishable': True},
        'Craft Beer 6-pack': {'category': 'Beverages', 'price': 55.00, 'perishable': False},
        'Parboiled Rice 5kg': {'category': 'Grocery', 'price': 22.00, 'perishable': False},
    }

    TRANSLATIONS = {
        'pt_BR': {
            'Dairy': 'Laticínios', 'Grocery': 'Mercearia', 'Meat': 'Açougue', 'Beverages': 'Bebidas',
            'Whole Milk 1L': 'Leite Integral 1L', 'Roasted Coffee 500g': 'Café Torrado 500g',
            'Beef Tenderloin (kg)': 'Filé Mignon (kg)', 'Craft Beer 6-pack': 'Cerveja Artesanal 6-pack',
            'Parboiled Rice 5kg': 'Arroz Parboilizado 5kg'
        },
        'es_ES': {
            'Dairy': 'Lácteos',
            'Grocery': 'Abarrotes',
            'Meat': 'Carnes',
            'Beverages': 'Bebidas',
            'Whole Milk 1L': 'Leche Entera 1L',
            'Roasted Coffee 500g': 'Café Tostado 500g',
            'Beef Tenderloin (kg)': 'Solomillo de Res (kg)',
            'Craft Beer 6-pack': 'Cerveza Artesanal 6 unidades',
            'Parboiled Rice 5kg': 'Arroz Vaporizado 5kg'
        },
        'hi_IN': {
            'Dairy': 'डेयरी',
            'Grocery': 'किराना',
            'Meat': 'मांस',
            'Beverages': 'पेय पदार्थ',
            'Whole Milk 1L': 'पूर्ण क्रीम दूध 1L',
            'Roasted Coffee 500g': 'भुनी हुई कॉफ़ी 500g',
            'Beef Tenderloin (kg)': 'बीफ़ टेंडरलॉइन (किग्रा)',
            'Craft Beer 6-pack': 'क्राफ़्ट बीयर 6 का पैक',
            'Parboiled Rice 5kg': 'पारबॉइल्ड चावल 5किग्रा'
        },
        'zh_CN': {
            'Dairy': '乳制品',
            'Grocery': '杂货',
            'Meat': '肉类',
            'Beverages': '饮料',
            'Whole Milk 1L': '全脂牛奶1升',
            'Roasted Coffee 500g': '烘焙咖啡500克',
            'Beef Tenderloin (kg)': '牛里脊(公斤)',
            'Craft Beer 6-pack': '精酿啤酒6瓶装',
            'Parboiled Rice 5kg': '蒸谷米5公斤'
        }
    }

    SEASONALITY = [1.0, 0.9, 0.9, 1.0, 1.0, 1.0, 1.1, 1.0, 1.0, 1.0, 1.1, 1.6]
    CUSTOMER_NAME = 'customer_name'

    def get_metadata(self):
        return {"description": "Food and Beverages retail sales", "products": list(self.PRODUCTS_FOOD.keys())}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        sales_data = []
        product_list = list(self.PRODUCTS_FOOD.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 10, 1)), span_days=150)

        for i in range(self.num_records):
            raw_prod = self.py_rng.choice(product_list)
            info = self.PRODUCTS_FOOD[raw_prod]
            order_date = dates[i]
            base_price = info['price']
            if info['perishable'] and self.rng.random() < 0.15:
                unit_price = base_price * 0.80
            else:
                unit_price = base_price * self.rng.uniform(0.95, 1.05)
            unit_price = round(float(unit_price), 2)
            quantity = int(self.rng.integers(1, 20))

            validity_days = int(self.rng.integers(3, 30 if info['perishable'] else 365))

            sales_data.append({
                'transaction_id': 5000 + i,
                'order_date': order_date,
                'product': translator.get(raw_prod, raw_prod),
                'category': translator.get(info['category'], info['category']),
                'unit_price': unit_price,
                'quantity': quantity,
                'total_sale': round(unit_price * quantity, 2),
                'expiration_date': order_date + timedelta(days=validity_days),
                'customer_id': int(self.rng.integers(100, 9999)),
                'customer_name': self.fake.name(),
                'delivery_zipcode': self.fake.postcode()
            })

        return self._finalize(sales_data, "Food and Beverages", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
