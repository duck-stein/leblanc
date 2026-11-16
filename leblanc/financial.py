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


class Financial(Leblanc):

    PRODUCTS_FINANCIAL = {
        'Personal Loan': {'type': 'Loan', 'min_value': 5000, 'max_value': 50000, 'base_interest': 0.015},
        'Credit Card': {'type': 'Service', 'min_value': 1000, 'max_value': 20000, 'base_interest': 0.05},
        'Checking Account': {'type': 'Service', 'min_value': 0, 'max_value': 0, 'base_interest': 0.0},
        'Mortgage': {'type': 'Loan', 'min_value': 100000, 'max_value': 500000, 'base_interest': 0.007},
    }
    RISK_LEVELS = ['Low', 'Medium', 'High']

    TRANSLATIONS = {
        'pt_BR': {
            'Personal Loan': 'Empréstimo Pessoal', 'Credit Card': 'Cartão de Crédito',
            'Checking Account': 'Conta Corrente', 'Mortgage': 'Financiamento Imobiliário',
            'Loan': 'Empréstimo', 'Service': 'Serviço',
            'Low': 'Baixo', 'Medium': 'Médio', 'High': 'Alto'
        },
        'es_ES': {
            'Personal Loan': 'Préstamo Personal',
            'Credit Card': 'Tarjeta de Crédito',
            'Checking Account': 'Cuenta Corriente',
            'Mortgage': 'Hipoteca',
            'Loan': 'Préstamo',
            'Service': 'Servicio',
            'Low': 'Bajo',
            'Medium': 'Medio',
            'High': 'Alto'
        },
        'hi_IN': {
            'Personal Loan': 'व्यक्तिगत ऋण',
            'Credit Card': 'क्रेडिट कार्ड',
            'Checking Account': 'चालू खाता',
            'Mortgage': 'गृह ऋण',
            'Loan': 'ऋण',
            'Service': 'सेवा',
            'Low': 'कम',
            'Medium': 'मध्यम',
            'High': 'उच्च'
        },
        'zh_CN': {
            'Personal Loan': '个人贷款',
            'Credit Card': '信用卡',
            'Checking Account': '活期账户',
            'Mortgage': '住房抵押贷款',
            'Loan': '贷款',
            'Service': '服务',
            'Low': '低',
            'Medium': '中',
            'High': '高'
        }
    }

    SEASONALITY = [1.4, 1.1, 1.0, 1.0, 1.0, 0.9, 0.9, 0.9, 0.9, 1.0, 1.1, 1.4]
    CUSTOMER_ID = 'client_id'

    def get_metadata(self):
        return {"description": "Banking transactions and risk profiles"}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        prod_list = list(self.PRODUCTS_FINANCIAL.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 7, 1)), span_days=150)
        client_pool = max(100, self.num_records // 5)

        for i in range(self.num_records):
            raw_prod = self.py_rng.choice(prod_list)
            info = self.PRODUCTS_FINANCIAL[raw_prod]
            raw_risk = self.py_rng.choice(self.RISK_LEVELS)
            value_base = info['min_value'] + self.rng.random() * (info['max_value'] - info['min_value'])
            risk_factor = {'Low': 0.9, 'Medium': 1.0, 'High': 1.2}[raw_risk]
            final_interest = info['base_interest'] * risk_factor * self.rng.uniform(0.95, 1.05)
            high_risk_default = raw_risk == 'High' and self.rng.random() < 0.2
            card_default = raw_prod == 'Credit Card' and self.rng.random() < 0.1
            is_default = bool((high_risk_default or card_default) and raw_prod != 'Checking Account')

            data.append({
                'client_id': 7000 + int(self.rng.integers(1, client_pool + 1)),
                'transaction_date': dates[i],
                'financial_product': translator.get(raw_prod, raw_prod),
                'type': translator.get(info['type'], info['type']),
                'contracted_value': round(float(value_base), 2),
                'monthly_interest_rate': round(float(final_interest), 4),
                'client_risk_level': translator.get(raw_risk, raw_risk),
                'is_default': is_default
            })

        return self._finalize(data, "Financial Services", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
