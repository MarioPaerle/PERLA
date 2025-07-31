"""Esempio di utilizzo della DeepSCM"""

import numpy as np
from models import SCM, DeepSCM
from random import choice


with open('../datas/parole_sillabate_2.txt', 'r') as f:
    datas = ' '.join(f.readlines())

datalist = [[c for c in datas.split()]]
datas2 = np.array(datalist)
data = np.array(datas2)

bm = DeepSCM(10)

bm.fit(data, hashable=True)

v_init = choice(data[0])
generated_sample = bm.sequential_predict(v_init, 3, 3)
print(''.join(generated_sample).replace('-', ' '))