# nactu knihovnu pandas
import pandas as pd

# ulozim adresu API
endpoint = "https://opendata.mfcr.cz/api/v1/faktury"

offset = 0  # od ktereho radku zacit
limit = 100  # kolik radku na stranku

# nactu si prazdny dataframe
df = pd.DataFrame()

# budu opakovat dokud nezavolam break
while True:

    # vytvorim adresu podle dokumentace - limit je kolik radku, offset od ktereho a `dodavatel_i%C4%8Do=eq.64949681` je filtr na dodavatele T-Mobile
    url = f"{endpoint}?limit={limit}&offset={offset}&dodavatel_i%C4%8Do=eq.64949681"
    print(url)

    # nactu data
    df_part = pd.read_json(url)

    # zapsat data do celkoveho df - sloucim stare a nove zaznamy a ulozim je do puvodni promenne df
    df = pd.concat([df, df_part])

    # pocet radku tenhle iterace
    count = len(df_part)

    print(f"Pocet radku: {count}")

    offset += count

    if count == 0:
        break

df.to_csv("./download.csv", index=False) # index=False zajistí, že se neuloží první sloupec s čísly řádků

