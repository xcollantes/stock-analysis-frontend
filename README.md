# Stock analysis frontend

## Start locally

1. Clone this repo

   ```shell
   git clone https://github.com/xcollantes/stock-analysis-frontend
   ```

1. Download dependencies:

   ```shell
   python3 -m venv env
   env/bin/pip install -r requirements.txt
   ```

1. Create `.streamlit/secrets.toml` file with API keys:

   - Get FinancialModelPrep.com API key:
     https://site.financialmodelingprep.com/register
   - Get FinnHub.io API key: https://finnhub.io

1. Start locally:

   ```shell
   env/bin/streamlit run Home.py
   ```

## Adding a new page

The Home page is `Home.py` which is accessed at `http://localhost`.

Subsequent pages can be nested under the `pages/` directory and accessed:

`pages/drops.py` -> `http://localhost/drops`

1. Add page as file in `pages/`.
1. Add page name and title to `deps/Home.py`.
