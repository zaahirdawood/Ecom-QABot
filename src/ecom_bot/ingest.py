import pandas as pd
import minsearch
import os

dp= os.environ['DATA_PATH']

def load_index(data_path=dp): 

    dat_df = pd.read_csv(data_path)

    documents = dat_df.to_dict(orient='records')


    index= minsearch.Index(
        text_fields = ['question', 
                       'answer', 
                       'topic'
                       ],
        
        keyword_fields = ['id']
    )

    index.fit(documents)
    return index 