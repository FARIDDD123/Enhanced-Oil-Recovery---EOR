import numpy as np
import pandas as pd

# تعداد داده‌ها
n_samples = 1_000_000

# ساخت ویژگی‌ها
np.random.seed(42)
pressure = np.random.uniform(1500, 5000, n_samples)
temperature = np.random.uniform(50, 130, n_samples)
viscosity = np.random.uniform(1, 500, n_samples)
porosity = np.random.uniform(5, 35, n_samples)
permeability = np.random.uniform(0.1, 1000, n_samples)
saturation = np.random.uniform(20, 70, n_samples)
inj_rate = np.random.uniform(100, 10000, n_samples)
salinity = np.random.uniform(1000, 200000, n_samples)
depth = np.random.uniform(3000, 12000, n_samples)

# انتخاب تصادفی نوع تزریق
inj_type = np.random.choice(['Gas', 'Polymer', 'Steam'], n_samples)

# شبیه‌سازی خروجی‌ها بر اساس یک مدل فرضی
recovery = 20 + (porosity/10) + (permeability/300) - (viscosity/100) + (np.where(inj_type == 'Steam', 5, 0))
recovery = np.clip(recovery + np.random.normal(0, 2, n_samples), 10, 70)

cumulative_oil = recovery * 100  # فرض بر 100 بشکه در هر درصد
efficiency = (recovery / 70) * 100

# ساخت دیتافریم
df = pd.DataFrame({
    'Pressure': pressure,
    'Temperature': temperature,
    'Viscosity': viscosity,
    'Porosity': porosity,
    'Permeability': permeability,
    'Water_Saturation': saturation,
    'Injection_Rate': inj_rate,
    'Injection_Type': inj_type,
    'Salinity': salinity,
    'Depth': depth,
    'Oil_Recovery': recovery,
    'Cumulative_Oil': cumulative_oil,
    'Efficiency': efficiency
})

# ذخیره فایل
df.to_csv('synthetic_EOR_dataset.csv', index=False)
