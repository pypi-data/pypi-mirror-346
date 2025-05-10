# Ultrasound Processing Package (Minimal)

Python csomag ultrahangos képek feldolgozásához – minimal változat.  
Ez a csomag az alapvető feldolgozási funkciókat tartalmazza, mint a maszkolás, leképezés és képtranszformáció.

## 🔧 Telepítés

```
pip install ultrasound-processing-package-minimal
```

## 📦 Modulok

- `mask` – maszkolás és zajszűrés
- `interp` – térbeli leképezés és interpoláció
- `transform` – íves → sík képtranszformáció

## 📘 Dokumentáció

Részletes példa- és API-leírás:  
👉 [https://ultrasound-processing-minimal.readthedocs.io](https://ultrasound-processing-minimal.readthedocs.io)

## 💡 Példa használatra

```python
from ultrasound_processing_package_minimal import mask

# Példa futtatás
cleaned_img = mask.apply_noise_filter(image)
```

## ⚖️ Licenc

MIT License – Szabadon használható, módosítható, publikálható.
