
# SoftCropper

**SoftCropper** is a Python tool that automatically resizes rectangular images into squares and adds soft, blurred borders — ideal for prepping images for print or display.

> _This package is part of the internal tools used at [CanvasMagnet](https://www.instagram.com/canvamagnet/) for order preparation and production automation._

---

![Overview](./tests/softcropper.png)

---

### 📸 Example Results

| Before | ➡️ | After |
|--------|----|-------|
| <sub>Baby.webp (600×900)</sub><br><img src="./tests/assets/baby.webp" width="150"/> |  | <sub>Output (900×900)</sub><br><img src="./tests/assets/output/baby.webp" width="150"/> |
| <sub>Kid.jpg (1100×733)</sub><br><img src="./tests/assets/kid.jpg" width="150"/> |  | <sub>Output (1100×1100)</sub><br><img src="./tests/assets/output/kid.jpg" width="150"/> |

---

## 🚀 Features

- Pads any image to a perfect square
- Fills padding using soft Gaussian blur from original image
- Automatically saves output in a separate folder

---

## 📦 Requirements

- Python `>= 3.7`
- `opencv-python`
- `numpy`
  

## 🔧 Installation

```bash
pip install softcropper
```

## ⚙️ Usage

```bash
softcropper ./path/input_photos ./path/output_ready
```
- input_photos: folder with png, jpg, jpeg, or webp files
- output_photos: optional (defaults to ./input_photos/output/)


## ✅ Testing

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/test_softcropper.py -v
```

## 🛠️ Makefile Commands

```
make venv         # create .venv
make install      # install in editable mode
make test         # run unit/integration tests
make build        # build for PyPI
make clean        # remove all build artifacts and caches
```

## 🤝 Contribution
Pull requests are welcome! If you'd like to suggest improvements or fix issues, feel free to fork and submit.


## Author

**Khaled Alam**

📧 [khaledalam.net@gmail.com](mailto:khaledalam.net@gmail.com)<br />
🌍 [Website](https://khaledalam.net/) | [LinkedIn](https://www.linkedin.com/in/khaledalam/) | [X(Twitter)](https://x.com/khaledalamxyz
)
