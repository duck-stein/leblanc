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


class Healthcare(Leblanc):

    PROCEDURES = {
        'General Consultation': {'department': 'Primary Care', 'price': 250.0, 'duration': 30},
        'Blood Test Panel': {'department': 'Laboratory', 'price': 120.0, 'duration': 15},
        'X-Ray': {'department': 'Radiology', 'price': 180.0, 'duration': 20},
        'MRI Scan': {'department': 'Radiology', 'price': 1200.0, 'duration': 45},
        'Physiotherapy Session': {'department': 'Rehabilitation', 'price': 150.0, 'duration': 50},
        'Minor Surgery': {'department': 'Surgery', 'price': 6500.0, 'duration': 90},
        'Dental Cleaning': {'department': 'Dentistry', 'price': 200.0, 'duration': 40},
    }
    COVERAGE = {'Private Insurance': 0.8, 'Public Health System': 0.95, 'Out of Pocket': 0.0}
    OUTCOMES = ['Resolved', 'Follow-up Needed', 'Referred']

    SEASONALITY = [1.1, 1.0, 1.0, 1.0, 1.1, 1.3, 1.3, 1.2, 1.0, 1.0, 1.0, 1.1]
    CUSTOMER_ID = 'patient_id'

    TRANSLATIONS = {
        'pt_BR': {
            'General Consultation': 'Consulta Geral', 'Blood Test Panel': 'Exames de Sangue', 'X-Ray': 'Raio-X',
            'MRI Scan': 'Ressonância Magnética', 'Physiotherapy Session': 'Sessão de Fisioterapia',
            'Minor Surgery': 'Cirurgia Menor', 'Dental Cleaning': 'Limpeza Dental',
            'Primary Care': 'Clínica Geral', 'Laboratory': 'Laboratório', 'Radiology': 'Radiologia',
            'Rehabilitation': 'Reabilitação', 'Surgery': 'Cirurgia', 'Dentistry': 'Odontologia',
            'Private Insurance': 'Plano de Saúde', 'Public Health System': 'Sistema Público', 'Out of Pocket': 'Particular',
            'Resolved': 'Resolvido', 'Follow-up Needed': 'Retorno Necessário', 'Referred': 'Encaminhado'
        },
        'es_ES': {
            'General Consultation': 'Consulta General', 'Blood Test Panel': 'Panel de Análisis de Sangre', 'X-Ray': 'Radiografía',
            'MRI Scan': 'Resonancia Magnética', 'Physiotherapy Session': 'Sesión de Fisioterapia',
            'Minor Surgery': 'Cirugía Menor', 'Dental Cleaning': 'Limpieza Dental',
            'Primary Care': 'Atención Primaria', 'Laboratory': 'Laboratorio', 'Radiology': 'Radiología',
            'Rehabilitation': 'Rehabilitación', 'Surgery': 'Cirugía', 'Dentistry': 'Odontología',
            'Private Insurance': 'Seguro Privado', 'Public Health System': 'Sistema Público de Salud', 'Out of Pocket': 'Pago Directo',
            'Resolved': 'Resuelto', 'Follow-up Needed': 'Requiere Seguimiento', 'Referred': 'Derivado'
        },
        'hi_IN': {
            'General Consultation': 'सामान्य परामर्श', 'Blood Test Panel': 'रक्त परीक्षण पैनल', 'X-Ray': 'एक्स-रे',
            'MRI Scan': 'एमआरआई स्कैन', 'Physiotherapy Session': 'फ़िज़ियोथेरेपी सत्र',
            'Minor Surgery': 'छोटी सर्जरी', 'Dental Cleaning': 'दंत सफ़ाई',
            'Primary Care': 'प्राथमिक देखभाल', 'Laboratory': 'प्रयोगशाला', 'Radiology': 'रेडियोलॉजी',
            'Rehabilitation': 'पुनर्वास', 'Surgery': 'सर्जरी', 'Dentistry': 'दंत चिकित्सा',
            'Private Insurance': 'निजी बीमा', 'Public Health System': 'सार्वजनिक स्वास्थ्य प्रणाली', 'Out of Pocket': 'स्वयं भुगतान',
            'Resolved': 'समाधान हुआ', 'Follow-up Needed': 'फ़ॉलो-अप आवश्यक', 'Referred': 'रेफ़र किया गया'
        },
        'zh_CN': {
            'General Consultation': '普通门诊', 'Blood Test Panel': '血液检查套餐', 'X-Ray': 'X光检查',
            'MRI Scan': '核磁共振检查', 'Physiotherapy Session': '理疗',
            'Minor Surgery': '小型手术', 'Dental Cleaning': '洁牙',
            'Primary Care': '全科', 'Laboratory': '检验科', 'Radiology': '放射科',
            'Rehabilitation': '康复科', 'Surgery': '外科', 'Dentistry': '口腔科',
            'Private Insurance': '商业保险', 'Public Health System': '公共医疗体系', 'Out of Pocket': '自费',
            'Resolved': '已解决', 'Follow-up Needed': '需要随访', 'Referred': '已转诊'
        }
    }

    def get_metadata(self):
        return {"description": "Healthcare visits, billing and outcomes", "procedures": list(self.PROCEDURES.keys())}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        procedures = list(self.PROCEDURES.keys())
        coverages = list(self.COVERAGE.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 1, 1)))

        for i in range(self.num_records):
            raw_proc = self.py_rng.choice(procedures)
            info = self.PROCEDURES[raw_proc]
            raw_cover = self.py_rng.choice(coverages)
            raw_outcome = self.py_rng.choices(self.OUTCOMES, weights=[0.7, 0.2, 0.1])[0]
            billed = round(float(info['price'] * self.rng.uniform(0.9, 1.15)), 2)
            covered = round(billed * self.COVERAGE[raw_cover], 2)
            duration = max(5, int(info['duration'] + self.rng.integers(-5, 16)))
            readmit_chance = 0.25 if raw_outcome == 'Follow-up Needed' else 0.05

            data.append({
                'visit_id': 2000 + i,
                'visit_date': dates[i],
                'procedure': translator.get(raw_proc, raw_proc),
                'department': translator.get(info['department'], info['department']),
                'patient_id': int(self.rng.integers(1000, 9999)),
                'patient_age': int(self.rng.integers(1, 95)),
                'insurance_type': translator.get(raw_cover, raw_cover),
                'duration_minutes': duration,
                'billed_amount': billed,
                'covered_amount': covered,
                'patient_amount': round(billed - covered, 2),
                'outcome': translator.get(raw_outcome, raw_outcome),
                'readmitted': bool(self.rng.random() < readmit_chance)
            })

        return self._finalize(data, "Healthcare", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
