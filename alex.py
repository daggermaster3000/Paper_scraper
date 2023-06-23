from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
import pandas as pd

pyalex.config.email = "favey.quillan@gmail.com"
df = pd.read_json(Works().search("fierce creatures").get()[0])
print(df)