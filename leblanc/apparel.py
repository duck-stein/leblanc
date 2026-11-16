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
        },
        'es_ES': {
            'Bottom Wear': 'Parte Inferior',
            'Top Wear': 'Parte Superior',
            'Footwear': 'Calzado',
            'Womenswear': 'Moda Mujer',
            'Accessories': 'Accesorios',
            'Slim Fit Jeans': 'Vaqueros Slim',
            'Basic Cotton T-Shirt': 'Camiseta Básica de Algodón',
            'Casual Running Shoes': 'Zapatillas Casuales de Correr',
            'Summer Midi Dress': 'Vestido Midi de Verano',
            'Dress Socks (Pair)': 'Calcetines de Vestir (Par)',
            'Black': 'Negro',
            'White': 'Blanco',
            'Navy Blue': 'Azul Marino',
            'Grey': 'Gris',
            'Red': 'Rojo'
        },
        'hi_IN': {
            'Bottom Wear': 'निचले वस्त्र',
            'Top Wear': 'ऊपरी वस्त्र',
            'Footwear': 'जूते',
            'Womenswear': 'महिला परिधान',
            'Accessories': 'एक्सेसरीज़',
            'Slim Fit Jeans': 'स्लिम फ़िट जींस',
            'Basic Cotton T-Shirt': 'बेसिक कॉटन टी-शर्ट',
            'Casual Running Shoes': 'कैज़ुअल रनिंग शूज़',
            'Summer Midi Dress': 'समर मिडी ड्रेस',
            'Dress Socks (Pair)': 'फ़ॉर्मल मोज़े (जोड़ी)',
            'Black': 'काला',
            'White': 'सफ़ेद',
            'Navy Blue': 'नेवी ब्लू',
            'Grey': 'स्लेटी',
            'Red': 'लाल'
        },
        'zh_CN': {
            'Bottom Wear': '下装',
            'Top Wear': '上装',
            'Footwear': '鞋类',
            'Womenswear': '女装',
            'Accessories': '配饰',
            'Slim Fit Jeans': '修身牛仔裤',
            'Basic Cotton T-Shirt': '基础款纯棉T恤',
            'Casual Running Shoes': '休闲跑鞋',
            'Summer Midi Dress': '夏季中长连衣裙',
            'Dress Socks (Pair)': '正装袜(双)',
            'Black': '黑色',
            'White': '白色',
            'Navy Blue': '藏青色',
            'Grey': '灰色',
            'Red': '红色'
        }
    }

    SEASONALITY = [0.9, 0.8, 0.9, 1.0, 1.1, 1.0, 1.0, 0.9, 1.0, 1.1, 1.5, 1.7]

    def get_metadata(self):
        return {"description": "Apparel and Fashion sales data"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        sales_data = []
        product_list = list(self.PRODUCTS_APPAREL.keys())
        translator = self._translator()
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
