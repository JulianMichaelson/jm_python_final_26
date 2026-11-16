# Julians Pizza

A simple Streamlit point-of-sale app for building pizza orders, calculating order totals, and keeping a local order log.

## Run locally

From the project folder in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run Final_Project.py
```

The app reads menu choices from `menu_config.txt`. Prices are configured in `Final_Project.py`; if you add menu choices, add their prices there too. Employee registrations are saved in `employees.txt`, and completed orders are appended to `orders.txt`.

Employee IDs are used for staff attribution only; this local demo does not use passwords or provide secure authentication. Prices are example prices, and sales tax is not included.
