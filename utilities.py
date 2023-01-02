import pandas as pd
import numpy as np


def read_data(filepath: str):
    data = pd.read_excel(filepath)
    
    data['onculler'] = data['onculler'].apply(lambda x: [] if pd.isnull(x) else x)
    data['onculler'] = data['onculler'].apply(lambda x: x.split(',') if type(x) == str else x)
    
    return data