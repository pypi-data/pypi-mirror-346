# issnresolver

Fast, asynchronous resolution between ISSNs, EISSNs, and ISSN-L using the [ISSN Portal API](https://portal.issn.org).  
Supports both forward (ISSN → ISSN-L) and reverse (ISSN-L → all related ISSNs) lookup.

---

## 🔧 Features

- 🔁 ISSN or EISSN → ISSN-L (forward lookup)
- 🔁 ISSN-L → list of all related ISSNs and EISSNs (reverse lookup)
- ⚡ Async support with built-in rate limiting
- 🧠 Safe for Jupyter notebooks (via `nest_asyncio`)
- 📦 Pandas integration for batch filling missing ISSN-Ls in DataFrames

---

## 📦 Installation

```bash
pip install issnresolver
```

**For Jupyter notebook support:**

```bash
pip install "issnresolver[notebook]"
```

---

## 🚀 Usage

### ✅ Example 1: Clean an ISSN

```python
from issnresolver.utils import clean_issn

clean_issn("12345678")  # → '1234-5678'
```

---

### ✅ Example 2: Fill ISSN-L in a DataFrame

```python
import pandas as pd
from issnresolver.utils import fill_missing_issnl_fast

df = pd.DataFrame({
    "title": ["Journal A", "Journal B"],
    "issn": ["1234-5678", None],
    "eissn": [None, "1557-7317"],
    "issn_l": [None, None]
})

df = fill_missing_issnl_fast(df)
print(df)
```

---

### ✅ Example 3: Direct Async Lookups

```python
from issnresolver.core import async_lookup, async_lookup_reverse

# Forward: ISSN or EISSN → ISSN-L
async_lookup(["1234-5678", "1557-7317"])

# Reverse: ISSN-L → list of ISSNs
async_lookup_reverse(["1234-5678"])
```

---

## 🧠 Notebook Usage

If you're using `issnresolver` in a **Jupyter notebook**, you must apply `nest_asyncio` before calling lookup functions:

```python
import nest_asyncio
nest_asyncio.apply()
```

> This is required because Jupyter runs an active event loop.
> Without it, you may get:  
> `RuntimeError: asyncio.run() cannot be called from a running event loop`

To install notebook support:

```bash
pip install "issnresolver[notebook]"
```

---

## 📘 License

MIT © Ace Setiawan
