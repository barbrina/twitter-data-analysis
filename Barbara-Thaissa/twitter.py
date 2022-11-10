# Import the necessary package to process data in JSON format
import json
# Import the tweepy library
import tweepy
import pandas as pd
from IPython.display import display
import numpy as np
import networkx as nx
import time


# Aqui utilizamos a função open para abrir nosso arquivo e a
# biblioteca json para carregar nosso arquivo para uma variável chamada info.
credenciais = open('../credenciais.json').read()
info = json.loads(credenciais)

consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']

# Setup tweepy to authenticate with Twitter credentials:
autorizacao = tweepy.OAuthHandler(consumer_key, consumer_secret)
autorizacao.set_access_token(access_key, access_secret)

# Agora temos nossa variável chamada api onde guardamos uma instância do tweepy e
# com ela que iremos trabalhar a partir de agora.
api = tweepy.API(autorizacao)

# Pega 1000 tweets em português
tweets = tweepy.Cursor(api.search_tweets, q="*",
                       lang="pt", tweet_mode="extended")

resultado = []
for tweet in tweets.items(10):  # Remove the limit to 1000
    try:
        resultado.append(tweet.full_text)
    except:
        resultado.append(tweet.retweeted_status.full_text)
    resultado.append(tweet.retweet_count)
    try:
        resultado.append(tweet.retweeted_status.favorite_count)
    except:
        resultado.append(tweet.favorite_count)
    # resultado.append(tweet.created_at)
    resultado.append(tweet.user.screen_name)
    resultado.append(tweet.user.followers_count)
    resultado.append(tweet.user.friends_count)

matriz_np = np.array(resultado)
matriz_ajustada = np.reshape(matriz_np, (10, 6))

df = pd.DataFrame()

colunas = [
    'Tweet',
    'RTs',
    'Curtidas',
    # 'Data',
    'Nome do usuário',
    'Nº de seguidores',
    'Nº de amigos'
]

# displaying the DataFrame
df = pd.DataFrame(matriz_ajustada, columns=colunas)
display(df)

arquivo_tweets = 'tweets.csv'
df.to_csv(arquivo_tweets, encoding='utf-8', index=False, quotechar='|')