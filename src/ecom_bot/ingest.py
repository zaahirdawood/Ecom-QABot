import pandas as pd
import minsearch


def load_index(data_path=''):

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