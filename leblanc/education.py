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


class Education(Leblanc):

    COURSES = {
        'Data Science Bootcamp': {'level': 'Professional', 'price': 4500.0, 'hours': 240},
        'Intro to Python': {'level': 'Beginner', 'price': 600.0, 'hours': 40},
        'MBA Finance': {'level': 'Postgraduate', 'price': 18000.0, 'hours': 480},
        'English B2': {'level': 'Language', 'price': 1200.0, 'hours': 90},
        'Digital Marketing': {'level': 'Professional', 'price': 2200.0, 'hours': 120},
        'High School Prep': {'level': 'Secondary', 'price': 900.0, 'hours': 200},
    }
    MODALITIES = {'Online': 0.8, 'In Person': 1.0, 'Hybrid': 0.9}
    DISCOUNTS = [0, 5, 10, 20]

    SEASONALITY = [1.8, 1.6, 1.1, 0.8, 0.8, 0.9, 1.4, 1.5, 1.1, 0.8, 0.7, 0.6]
    CUSTOMER_ID = 'student_id'

    TRANSLATIONS = {
        'pt_BR': {
            'Data Science Bootcamp': 'Bootcamp de Ciência de Dados', 'Intro to Python': 'Introdução ao Python',
            'MBA Finance': 'MBA em Finanças', 'English B2': 'Inglês B2', 'Digital Marketing': 'Marketing Digital',
            'High School Prep': 'Preparatório Ensino Médio',
            'Professional': 'Profissional', 'Beginner': 'Iniciante', 'Postgraduate': 'Pós-graduação',
            'Language': 'Idiomas', 'Secondary': 'Ensino Médio',
            'Online': 'Online', 'In Person': 'Presencial', 'Hybrid': 'Híbrido'
        },
        'es_ES': {
            'Data Science Bootcamp': 'Bootcamp de Ciencia de Datos', 'Intro to Python': 'Introducción a Python',
            'MBA Finance': 'MBA en Finanzas', 'English B2': 'Inglés B2', 'Digital Marketing': 'Marketing Digital',
            'High School Prep': 'Preparación de Bachillerato',
            'Professional': 'Profesional', 'Beginner': 'Principiante', 'Postgraduate': 'Posgrado',
            'Language': 'Idiomas', 'Secondary': 'Secundaria',
            'Online': 'En Línea', 'In Person': 'Presencial', 'Hybrid': 'Híbrido'
        },
        'hi_IN': {
            'Data Science Bootcamp': 'डेटा साइंस बूटकैंप', 'Intro to Python': 'पायथन का परिचय',
            'MBA Finance': 'फ़ाइनेंस में एमबीए', 'English B2': 'अंग्रेज़ी B2', 'Digital Marketing': 'डिजिटल मार्केटिंग',
            'High School Prep': 'हाई स्कूल तैयारी',
            'Professional': 'पेशेवर', 'Beginner': 'शुरुआती', 'Postgraduate': 'स्नातकोत्तर',
            'Language': 'भाषा', 'Secondary': 'माध्यमिक',
            'Online': 'ऑनलाइन', 'In Person': 'कक्षा में', 'Hybrid': 'हाइब्रिड'
        },
        'zh_CN': {
            'Data Science Bootcamp': '数据科学训练营', 'Intro to Python': 'Python入门',
            'MBA Finance': '金融MBA', 'English B2': '英语B2', 'Digital Marketing': '数字营销',
            'High School Prep': '高中备考',
            'Professional': '职业技能', 'Beginner': '入门', 'Postgraduate': '研究生',
            'Language': '语言', 'Secondary': '中学',
            'Online': '线上', 'In Person': '线下', 'Hybrid': '混合式'
        }
    }

    def get_metadata(self):
        return {"description": "Course enrollments, tuition and academic results", "courses": list(self.COURSES.keys())}

    def build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0):
        self._reset()
        data = []
        courses = list(self.COURSES.keys())
        modalities = list(self.MODALITIES.keys())
        translator = self._translator()
        dates = self._timeline(self._start(datetime(2025, 1, 1)))

        for i in range(self.num_records):
            raw_course = self.py_rng.choice(courses)
            info = self.COURSES[raw_course]
            raw_modality = self.py_rng.choice(modalities)
            discount = self.py_rng.choice(self.DISCOUNTS)
            tuition = round(float(info['price'] * self.MODALITIES[raw_modality] * (1 - discount / 100)), 2)
            attendance = float(min(1.0, max(0.2, self.rng.beta(8, 2))))
            grade = float(min(100.0, max(0.0, self.rng.normal(70 + (attendance - 0.8) * 40, 10))))

            data.append({
                'enrollment_id': 1500 + i,
                'enrollment_date': dates[i],
                'course': translator.get(raw_course, raw_course),
                'level': translator.get(info['level'], info['level']),
                'modality': translator.get(raw_modality, raw_modality),
                'student_id': int(self.rng.integers(1000, 9999)),
                'student_age': int(self.rng.integers(15, 60)),
                'course_hours': info['hours'],
                'tuition': tuition,
                'discount_pct': discount,
                'scholarship': bool(self.rng.random() < 0.1),
                'attendance_rate': round(attendance, 3),
                'final_grade': round(grade, 1),
                'completed': bool(grade >= 60 and attendance >= 0.7)
            })

        return self._finalize(data, "Education", missing_data_cols, missing_rate, outlier_cols, duplicate_rate)
