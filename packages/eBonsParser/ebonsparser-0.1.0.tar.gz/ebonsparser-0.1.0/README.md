# 🧾 eBonsParser

**eBonsParser** is a modular Python library for parsing digital receipt PDFs (eBons) used in Germany.  
It extracts structured data such as store details, purchase date, payment method, and a full itemized list.

🛒 Currently supports **REWE** receipts — built to extend to other German retailers (e.g., Lidl, Edeka, Aldi).

---
## 🚀 Features
- 📄 Parse eBon PDFs directly (from path or memory)
- 🛒 Extract store, date, total, payment type, and itemized product data
- 💶 Handle price, weight, unit, and tax class
- 🧱 Structured output using Pydantic models (easy to convert to JSON)

## 📦 Installation

Clone the repo and install in editable mode:

```bash
git clone https://github.com/YOUR_USERNAME/eBonsParser.git
cd eBonsParser
pip install -e .
```

## 🧠 Usage
```python
from eBonsParser import Rewe

pdf_file_path = "path/to/your/rewe.pdf"
rewe = Rewe()
receipt = rewe.parse_ebon(pdf_file_path)
print(receipt.model_dump_json(indent=4))
```
This will return a structured *Receipt* object like:
```json
{
    "ebonNr": 1617,
    "store": {
        "name": "REWE Markt GmbH",
        "type": "supermarket",
        "UID": "DE812706034",
        "address": {
            "street": "Pontdriesch 10-12",
            "city": "Aachen",
            "zip": 52062
        },
        "phone": "0241 1684258"
    },
    "date": "2025-05-06",
    "total": 6.85,
    "payment_method": {
        "method": "card",
        "card": null
    },
    "items": [
        {
            "name": "TARTETEIG",
            "price": 1.89,
            "tax_class": 0.07
        },
        ...
    ]
}
```

---

## 🙌 Contributing

Want to help improve **eBonsParser**?

Whether it's fixing bugs, adding support for more retailers, or improving documentation — your contributions are welcome!

Please read our [CONTRIBUTING.md](CONTRIBUTING.md)

## 📜 License
This project is licensed under the MIT License. For details see [LICENSE](LICENSE).
