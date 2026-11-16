# Contributing to leblanc

First off, thank you for considering contributing to **leblanc**! It's people like you that make the open-source community such an amazing place to learn, inspire, and create.

## Setting Up the Development Environment

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YourFork/leblanc.git
   cd leblanc
   ```

3. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

4. **Install Dependencies & Install in Editable Mode**:
   ```bash
   pip install -e ".[dev]"
   ```
   *Note: The `-e .` flag allows you to edit the code and test it immediately without reinstalling.*

## Coding Guidelines

If you are adding a new sector or modifying an existing one, please follow these rules:

1. **Inheritance**: All generator classes must inherit from `Leblanc` (imported from `.base`).
2. **Structure**:
   * Define your data dictionaries (e.g., `PRODUCTS_X`) as class constants.
   * Define a `TRANSLATIONS` dictionary for `pt_BR` support.
3. **Methods**:
   * Implement `get_metadata(self)`: Returns a dict with description.
   * Implement `build(self, missing_data_cols=None, missing_rate=0.05, outlier_cols=None, duplicate_rate=0.0)`: The main logic. Call `self._reset()` first.
   * Use `self.rng` (NumPy), `self.py_rng` (random) and `self.fake` (Faker) instead of global random state or a new Faker.
   * Use `self._timeline(...)` and `self._start(default)` for dates.
   * Return `self._finalize(data, name, missing_data_cols, missing_rate, outlier_cols, duplicate_rate)`.
4. **Registry**: add the class to `SECTORS` in `leblanc/__init__.py`.

## Testing

Before submitting a Pull Request, make sure your code works and does not break existing modules.

```bash
python -m pytest -q
```

Add your new sector to the parametrized lists in `tests/test_leblanc.py` and verify that `pt_BR` translations work.

## Submitting a Pull Request (PR)

1. Create a branch for your feature:
   ```bash
   git checkout -b feature/amazing-sector
   ```
2. Commit your changes:
   ```bash
   git commit -m 'Add Amazing Sector generator'
   ```
3. Push to the branch:
   ```bash
   git push origin feature/amazing-sector
   ```
4. Open a Pull Request on GitHub.
