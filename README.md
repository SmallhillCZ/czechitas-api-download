# Ukázka stažení dat z API pro DA jaro 2022

## Keboola

#### 1) Najdu si extractor `Generic` a vytvořím si k němu konfiguraci

#### 2) Do pole `Configuration Parameters` v nastavení extraktoru vložím ukázkové nastavení:

```json
{
  "parameters": {
    "api": {
      "baseUrl": "https://opendata.mfcr.cz/api/v1/",
      "pagination": {
        "method": "offset",
        "offsetParam": "offset",
        "limitParam": "limit",
        "limit": 100
      }
    },
    "config": {
      "outputBucket": "api-test",
      "jobs": [
        {
          "endpoint": "faktury",
          "params": {
            "dodavatel_ičo": "eq.64949681"
          }
        }
      ]
    }
  }
}
```

#### 3) Spustím extraktor a data se mi načtou do Storage do bucketu `api-test` do tabulky `faktury`

## Python

Okomentovaný ukázkový kód je v souboru [download.py](download.py), v notebooku [download.ipynb](download.ipynb) a níže:

```python
# ulozim adresu API
endpoint = 'https://opendata.mfcr.cz/api/v1/faktury'

offset = 0 # od ktereho radku zacit
limit = 1000 # kolik radku na stranku

# nactu si prazdny dataframe
df = pd.DataFrame()

# budu opakovat dokud nezavolam break
while True:

  # vytvorim adresu podle dokumentace - limit je kolik radku, offset od ktereho a `dodavatel_i%C4%8Do=eq.64949681` je filtr na dodavatele T-Mobile
  # pismenko f pred uvozovkami mi dovoli vyplnovat do textu hodnoty promennych jako `{nazev_promenne}`
  # treba pro prvni cyklus bude vysledek takovy: https://opendata.mfcr.cz/api/v1/faktury?limit=1000&offset=0&dodavatel_i%C4%8Do=eq.64949681
  url = f"{endpoint}?limit={limit}&offset={offset}&dodavatel_i%C4%8Do=eq.64949681"
  
  print(url) # vypisu url na obrazovku

  # nactu data
  df_part = pd.read_json(url)

  # zapsat data do celkoveho df - sloucim stare (df) a nove (df_part) zaznamy a sloucene je ulozim do puvodni promenne df
  df = pd.concat([df, df_part])

  # pocet radku tenhle iterace
  count = len(df_part)
  print(f"Pocet radku: {count}") # vypisu pocet radku na obrazovku

  offset += count

  if count == 0:
    break

# ulozim data do csv
df.to_csv("./download.csv", index=False)
```
