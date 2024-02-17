import numpy as np
import matplotlib.pyplot as plt

# تعريف المتغيرات الضبابية والدوال الانتماء
# ...

# تعريف المدخلات المستخدمة للمحاكاة
inputs = {
    'temperature': np.arange(00, 101, 1),
    'humidity': np.arange(0, 101, 1),
    'people': np.arange(0, 11, 1)
}

# إنشاء شبكة قيم للمدخلات
meshgrid = np.meshgrid(*inputs.values())

# تحويل الشبكة إلى قائمة
combinations = np.vstack([x.flatten() for x in meshgrid]).T

# تهيئة رسم البيانات
fig, ax = plt.subplots()

# حساب النتائج لكل مجموعة من القيم
results = []
for combo in combinations:
    for i, key in enumerate(inputs.keys()):
     simulator.input[key] = combo[i]
     simulator.compute()
    results.append(simulator.output['output'])

# عرض النتائج على شكل رسم بياني
ax.scatter(combinations[:, 0], combinations[:, 1], c=results, cmap='viridis')
ax.set_xlabel('Temperature')
ax.set_ylabel('Humidity')
ax.set_title('Fuzzy Logic Simulation Results')

# عرض الرسم البياني
plt.show()