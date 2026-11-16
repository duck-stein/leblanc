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


class Logistics(Leblanc):

    SERVICES = {
        'Standard Ground': {'mode': 'Road', 'rate_per_kg': 2.5, 'days': 5},
        'Express Air': {'mode': 'Air', 'rate_per_kg': 9.0, 'days': 2},
        'Ocean Freight': {'mode': 'Sea', 'rate_per_kg': 0.8, 'days': 25},
        'Rail Cargo': {'mode': 'Rail', 'rate_per_kg': 1.4, 'days': 9},
        'Same Day Courier': {'mode': 'Road', 'rate_per_kg': 15.0, 'days': 1},
    }
    REGIONS = ['North', 'South', 'East', 'West', 'Central']
    STATUSES = ['Delivered', 'In Transit', 'Returned']

    SEASONALITY = [0.9, 0.8, 0.9, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.1, 1.5, 1.8]

    TRANSLATIONS = {
        'pt_BR': {
            'Standard Ground': 'Terrestre Padrão', 'Express Air': 'Aéreo Expresso', 'Ocean Freight': 'Frete Marítimo',
            'Rail Cargo': 'Carga Ferroviária', 'Same Day Courier': 'Entrega no Mesmo Dia',
            'Road': 'Rodoviário', 'Air': 'Aéreo', 'Sea': 'Marítimo', 'Rail': 'Ferroviário',
            'North': 'Norte', 'South': 'Sul', 'East': 'Leste', 'West': 'Oeste', 'Central': 'Centro',
            'Delivered': 'Entregue', 'In Transit': 'Em Trânsito', 'Returned': 'Devolvido'
        },
        'es_ES': {
            'Standard Ground': 'Terrestre Estándar', 'Express Air': 'Aéreo Exprés', 'Ocean Freight': 'Flete Marítimo',
            'Rail Cargo': 'Carga Ferroviaria', 'Same Day Courier': 'Mensajería el Mismo Día',
            'Road': 'Carretera', 'Air': 'Aéreo', 'Sea': 'Marítimo', 'Rail': 'Ferroviario',
            'North': 'Norte', 'South': 'Sur', 'East': 'Este', 'West': 'Oeste', 'Central': 'Centro',
            'Delivered': 'Entregado', 'In Transit': 'En Tránsito', 'Returned': 'Devuelto'
        },
        'hi_IN': {
            'Standard Ground': 'स्टैंडर्ड ज़मीनी', 'Express Air': 'एक्सप्रेस हवाई', 'Ocean Freight': 'समुद्री माल ढुलाई',
            'Rail Cargo': 'रेल कार्गो', 'Same Day Courier': 'उसी दिन कूरियर',
            'Road': 'सड़क', 'Air': 'हवाई', 'Sea': 'समुद्री', 'Rail': 'रेल',
            'North': 'उत्तर', 'South': 'दक्षिण', 'East': 'पूर्व', 'West': 'पश्चिम', 'Central': 'मध्य',
            'Delivered': 'डिलीवर हुआ', 'In Transit': 'पारगमन में', 'Returned': 'लौटाया गया'
        },
        'zh_CN': {
            'Standard Ground': '标准陆运', 'Express Air': '空运特快', 'Ocean Freight': '海运',
            'Rail Cargo': '铁路货运', 'Same Day Courier': '当日达快递',
            'Road': '公路', 'Air': '航空', 'Sea': '海上', 'Rail': '铁路',
            'North': '北部', 'South': '南部', 'East': '东部', 'West': '西部', 'Central': '中部',
            'Delivered': '已送达', 'In Transit': '运输中', 'Returned': '已退回'
        }
    }

    def get_metadata(self):
        return {"description": "Freight shipments, costs and delivery performance", "services": list(self.SERVICES.keys())}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        services = list(self.SERVICES.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 1, 1)))

        for i in range(self.num_records):
            raw_service = self.py_rng.choice(services)
            info = self.SERVICES[raw_service]
            origin = self.py_rng.choice(self.REGIONS)
            destination = self.py_rng.choice(self.REGIONS)
            weight = float(min(5000.0, max(0.5, self.rng.lognormal(3.0, 1.2))))
            distance = int(self.rng.integers(20, 300)) if origin == destination else int(self.rng.integers(300, 4500))
            freight = weight * info['rate_per_kg'] * (1 + distance / 1000)
            promised = info['days'] + int(distance // 1500)
            delivery_days = max(1, promised + int(self.rng.integers(-1, 4)))
            raw_status = self.py_rng.choices(self.STATUSES, weights=[0.88, 0.09, 0.03])[0]

            data.append({
                'shipment_id': 4000 + i,
                'ship_date': dates[i],
                'service': translator.get(raw_service, raw_service),
                'transport_mode': translator.get(info['mode'], info['mode']),
                'origin_region': translator.get(origin, origin),
                'destination_region': translator.get(destination, destination),
                'weight_kg': round(weight, 2),
                'distance_km': distance,
                'freight_cost': round(float(freight), 2),
                'promised_days': promised,
                'delivery_days': delivery_days,
                'delayed': delivery_days > promised,
                'status': translator.get(raw_status, raw_status),
                'customer_id': int(self.rng.integers(100, 9999))
            })

        return self._finalize(data, "Logistics", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
