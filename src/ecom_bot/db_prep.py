# import os
# import requests
# import pandas as pd
# from tqdm.auto import tqdm
# from dotenv import load_dotenv

from db import init_db

# load_dotenv()

def main():
    print("Initializing database...")
    init_db()

    print("Indexing process completed successfully!")


if __name__ == "__main__":
    main()