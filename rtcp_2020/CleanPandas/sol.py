import pickle
import base64
import pandas as pd
from clean_pandas import CleanPandas

with open("pandas.pkl","rb") as f:
    df = pickle.load(f)

with open("soap.pkl","rb") as f:
    soap = pickle.load(f)

for k in soap:
    try:
        print("".join(df.clean_pandas.decrypt('unknown flag 394052487124', k)['unknown flag 394052487124']))
    except:
        pass




