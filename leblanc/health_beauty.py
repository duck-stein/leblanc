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


class HealthBeauty(Leblanc):

    PRODUCTS_HEALTH = {
        'Hydrating Facial Cream': {'type': 'Product', 'category': 'Skincare', 'price': 85.00, 'recurrence': 60},
        'Whey Protein Isolate': {'type': 'Product', 'category': 'Supplements', 'price': 150.00, 'recurrence': 45},
        'Anti-Frizz Shampoo': {'type': 'Product', 'category': 'Haircare', 'price': 35.00, 'recurrence': 30},
        'Lip Filler Session': {'type': 'Service', 'category': 'Aesthetics', 'price': 1200.00, 'recurrence': 180},
        'Deep Tissue Massage': {'type': 'Service', 'category': 'Wellness', 'price': 150.00, 'recurrence': 90},
    }
    CHANNELS = ['Online Store', 'Physical Store', 'Subscription']

    TRANSLATIONS = {
        'pt_BR': {
            'Skincare': 'Cuidados com Pele', 'Supplements': 'Suplementos', 'Haircare': 'Cabelos',
            'Aesthetics': 'Estética', 'Wellness': 'Bem-estar',
            'Product': 'Produto', 'Service': 'Serviço',
            'Hydrating Facial Cream': 'Creme Facial Hidratante', 'Whey Protein Isolate': 'Whey Protein Isolado',
            'Anti-Frizz Shampoo': 'Shampoo Anti-Frizz', 'Lip Filler Session': 'Preenchimento Labial',
            'Deep Tissue Massage': 'Massagem Deep Tissue',
            'Online Store': 'Loja Online', 'Physical Store': 'Loja Física', 'Subscription': 'Assinatura'
        },
        'es_ES': {
            'Skincare': 'Cuidado de la Piel',
            'Supplements': 'Suplementos',
            'Haircare': 'Cuidado del Cabello',
            'Aesthetics': 'Estética',
            'Wellness': 'Bienestar',
            'Product': 'Producto',
            'Service': 'Servicio',
            'Hydrating Facial Cream': 'Crema Facial Hidratante',
            'Whey Protein Isolate': 'Proteína Whey Aislada',
            'Anti-Frizz Shampoo': 'Champú Anti-Frizz',
            'Lip Filler Session': 'Sesión de Relleno de Labios',
            'Deep Tissue Massage': 'Masaje de Tejido Profundo',
            'Online Store': 'Tienda en Línea',
            'Physical Store': 'Tienda Física',
            'Subscription': 'Suscripción'
        },
        'hi_IN': {
            'Skincare': 'त्वचा की देखभाल',
            'Supplements': 'सप्लीमेंट्स',
            'Haircare': 'बालों की देखभाल',
            'Aesthetics': 'सौंदर्य उपचार',
            'Wellness': 'वेलनेस',
            'Product': 'उत्पाद',
            'Service': 'सेवा',
            'Hydrating Facial Cream': 'हाइड्रेटिंग फ़ेशियल क्रीम',
            'Whey Protein Isolate': 'व्हे प्रोटीन आइसोलेट',
            'Anti-Frizz Shampoo': 'एंटी-फ़्रिज़ शैम्पू',
            'Lip Filler Session': 'लिप फ़िलर सेशन',
            'Deep Tissue Massage': 'डीप टिशू मसाज',
            'Online Store': 'ऑनलाइन स्टोर',
            'Physical Store': 'भौतिक स्टोर',
            'Subscription': 'सब्सक्रिप्शन'
        },
        'zh_CN': {
            'Skincare': '护肤',
            'Supplements': '营养补充剂',
            'Haircare': '护发',
            'Aesthetics': '医美',
            'Wellness': '健康养生',
            'Product': '产品',
            'Service': '服务',
            'Hydrating Facial Cream': '保湿面霜',
            'Whey Protein Isolate': '分离乳清蛋白',
            'Anti-Frizz Shampoo': '防毛躁洗发水',
            'Lip Filler Session': '唇部填充疗程',
            'Deep Tissue Massage': '深层组织按摩',
            'Online Store': '线上商店',
            'Physical Store': '实体店',
            'Subscription': '订阅'
        }
    }

    SEASONALITY = [1.2, 0.9, 1.0, 1.0, 1.3, 1.0, 1.0, 1.0, 1.0, 1.0, 1.2, 1.5]

    def get_metadata(self):
        return {"description": "Health, Beauty and Wellness services/products"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        prod_list = list(self.PRODUCTS_HEALTH.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 11, 1)), span_days=120)

        for i in range(self.num_records):
            raw_prod = self.py_rng.choice(prod_list)
            info = self.PRODUCTS_HEALTH[raw_prod]
            raw_channel = self.py_rng.choice(self.CHANNELS)
            unit_price = info['price']
            if raw_channel == 'Subscription':
                unit_price = round(unit_price * 0.90, 2)

            data.append({
                'transaction_id': 8000 + i,
                'transaction_date': dates[i],
                'item_name': translator.get(raw_prod, raw_prod),
                'type': translator.get(info['type'], info['type']),
                'category': translator.get(info['category'], info['category']),
                'unit_price': unit_price,
                'quantity': int(self.rng.integers(1, 4)) if info['type'] == 'Product' else 1,
                'sales_channel': translator.get(raw_channel, raw_channel),
                'days_until_next_purchase': info['recurrence'] + int(self.rng.integers(-15, 15)),
                'customer_id': int(self.rng.integers(1000, 9999))
            })

        return self._finalize(data, "Health & Beauty", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
