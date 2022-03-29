# nactu knihovnu pandas
import pandas as pd

# ulozim adresu API
endpoint = 'https://opendata.mfcr.cz/api/v1/faktury'

offset = 0 # od ktereho radku zacit
limit = 1000 # kolik radku na cyklus

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

  # zapsat data do celkoveho df - sloucim stare a nove zaznamy a ulozim je do puvodni promenne df
  df = pd.concat([df, df_part])

  # pocet radku tenhle iterace
  count = len(df_part)
  print(f"Pocet radku: {count}") # vypisu pocet radku na obrazovku

  # zvysim offset o pocet radku abychom pristi cyklus zacinali od dalsiho radku
  offset += count

  # pokud se v tomto cyklu nestahly zadne radky, koncim cyklus prikazem `break`
  if count == 0:
    break

df.to_csv("./download.csv", index=False) # index=False zajistí, že se neuloží první sloupec s čísly řádků

