import requests
import re
import pandas as pd
from watson_developer_cloud import AlchemyLanguageV1
from bs4 import BeautifulSoup
from pandas.io.json import json_normalize

alchemy_language = AlchemyLanguageV1(api_key='e2ed5f68ab6c179d4a40e51a91ab1c0a0992ecc3')

url = 'https://developer.ibm.com/watson/blog/2015/11/03/price-reduction-for' \
      '-watson-personality-insights/'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
copy = soup.find(class_='pn-copy').get_text()
copy = re.split("or leave a comment below", copy)[0]  # remove the share this section
keywords = alchemy_language.combined(text=copy, extract=['keyword'])
keywords_df = json_normalize(keywords['keywords'])
keywords_df.columns = ['manual_relevance', 'manual_text']

keywords_api = alchemy_language.combined(url=url, extract=['keyword'])
keywords_api_df = json_normalize(keywords_api['keywords'])
keywords_api_df.columns = ['api_relevance', 'api_text']

if __name__ == "__main__":
        print(pd.concat([keywords_df, keywords_api_df], axis=1).head(10))