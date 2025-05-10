# Ultrasound Processing Package (Minimal)

Python csomag ultrahangos képek feldolgozásához – minimal verzió.  
A célja, hogy hatékony és jól dokumentált funkciókat biztosítson orvosi és ipari képfeldolgozási célokra.

## ✨ Fő jellemzők

- Maszkolás és zajszűrés (`mask` modul)
- Interpoláció és leképezés (`interp` modul)
- Íves → sík képtranszformáció (`transform` modul)
- Egyszerű, moduláris kódfelépítés
- Kompatibilis NumPy, OpenCV és SciPy eszközökkel

## 🔧 Telepítés

A csomag telepítése a PyPI-ről:

```bash
pip install ultrasound-processing-package-minimal
```

## 💡 Használati példa

```python
from ultrasound_processing_package_minimal import mask

# Feltételezzük, hogy 'image' egy NumPy tömb (pl. OpenCV-ből beolvasva)
cleaned = mask.apply_noise_filter(image)
```

## 📚 Dokumentáció

A teljes dokumentáció elérhető a Read the Docs oldalon:

[https://ultrasound-processing-minimal.readthedocs.io/en/latest/](https://ultrasound-processing-minimal.readthedocs.io/en/latest/)

## ⚙️ Követelmények

- Python 3.8+
- numpy
- matplotlib
- opencv-python
- Pillow
- scipy

## ⚖️ Licenc

MIT License – Szabadon felhasználható, módosítható és terjeszthető.

## 👨‍💻 Szerző

Készült MSc kutatási projekt keretében.  
GitHub: [https://github.com/Mart-SciecPyt/ultrasound-processing-minimal](https://github.com/Mart-SciecPyt/ultrasound-processing-minimal)
