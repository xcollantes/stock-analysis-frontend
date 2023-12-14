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
   env/bin/streamlit run 1_🏠_Getting_started.py
   ```

   Default is `Home.py` but to make path and sidebar named with emoji, this is
   the best way.

## Adding a new page

The Home page is `Home.py` which is accessed at `http://localhost`.

Subsequent pages can be nested under the `pages/` directory and accessed:

`pages/drops.py` -> `http://localhost/drops`

1. Add page as file in `pages/`.
1. Add page name and title to `deps/Home.py`.

## Naming pages

File name will tell Streamlit:

- Order
- Emoji
- Sidebar title
- Url path

Example: `pages/1_📈_Plotting_Demo.py`

- Order: first in sidebar
- Emoji: chart emoji
- Sidebar title: Plotting Demo
- Url path: https://mystreamlit.streamlit.app/Plotting_Demo

[Streamlit docs](https://docs.streamlit.io/library/get-started/multipage-apps/create-a-multipage-app#convert-an-existing-app-into-a-multipage-app)

## Common debugging issues

**Yahoo Finance.**

yfinance API is the weakest part of this project because it is a free resource
which scrapes Yahoo Finance data. Check functions that make contact with Yahoo
Finance first.

https://github.com/xcollantes/stock-analysis-frontend/issues/35

**TypeError: 'DataFrame' object is not callable.**

Error message is often misleading and usually is actually the failure of the
yfinance API. Either update the library or wait 24 hours for any limits to
replenish.

After checking the Yahoo Finance, check other keys for the other data sources.

**Enter password showing up in the middle of the page.**

The rest of the page could not load because the feature fell back on the
password box.
