# Ultrasound Processing Package

**Ultrasound image processing Python toolkit** intended for the purpose of segmenting and processing raw or preprocessed ultrasound video frames or datasets.

This package provides basic tools for cleaning, masking, transforming and converting ultrasound scan images (e.g., polar-to-cartesian), either from single images or from full recordings. Custom pipelines can be built by composing the different functions and classes.

---

## 📦 Modules

- `mask`
- `interp`
- `transform`

---

## 🧠 Description

1. **We offer tools for preprocessing the image under localization into a "flat" format.**
   We first remove noise using contour- and intensity-aware morphological processing. Then we apply thresholding or external segmentation to mask the relevant regions. Cropping is also applied to reduce the image size. This prepares the image for geometric transformation or machine learning input.

2. **An intuitive user flow for geometric inference using band-to-plane image depth shifts.**
   The ultrasound sector geometry is known from acquisition metadata. We provide tools to resample this sector image into a Cartesian image. This is especially useful for matching with real-world coordinates or fusing multiple images spatially.

3. **A modular structure that allows integration into processing pipelines or training workflows.**
   The functions are pure (stateless), and each submodule can be used independently. The codebase is lightweight and free of unnecessary dependencies.

---

## 🔧 Usage

### Installation

```bash
pip install ultrasound-processing-package
```

---

## 📚 Requirements

- Python 3.7 or higher
- numpy
- matplotlib
- opencv-python
- Pillow
- scipy

---

## 🧪 Example

```python
from ultrasound_processing import mask, interp

img = load_image("input.png")
cleaned = mask.apply(img)
cartesian = interp.polar_to_cartesian(cleaned)
```

---

## 🔗 More info

Project home: [GitHub Repository](https://github.com/Mart-SciecPyt/ultrasound-processing)

Documentation: [Read the Docs](https://ultrasound-processing-minimal.readthedocs.io/en/latest/)
