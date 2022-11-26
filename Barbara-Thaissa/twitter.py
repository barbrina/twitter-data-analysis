# -*- coding: utf-8 -*-
from community import community_louvain
from IPython.display import display
import scipy as sp
import matplotlib.pyplot as plt
import networkx as nx
import tweepy
import json
import pandas as pd

# Aqui utilizamos a funcaoo open para abrir nosso arquivo e a
# biblioteca json para carregar nosso arquivo para uma variavel chamada info.
credenciais = open('credenciais.json').read()
info = json.loads(credenciais)

consumer_key = info['API_ACCESS']
consumer_secret = info['API_ACCESS_SECRET']
access_key = info['ACCESS_TOKEN']
access_secret = info['ACCESS_TOKEN_SECRET']

# Configure tweepy para autenticar com as credenciais do Twitter:
autorizacao = tweepy.OAuthHandler(consumer_key, consumer_secret)
autorizacao.set_access_token(access_key, access_secret)

# Agora temos nossa variÃ¡vel chamada api onde guardamos uma instÃ¢ncia do tweepy e
# com ela que iremos trabalhar a partir de agora.
api = tweepy.API(autorizacao, wait_on_rate_limit=True)

me = api.get_user(screen_name="Barbrinass")
print(me.id)

user_list = [me.id]
follower_list = []
for user in user_list:
    followers = []
    try:
        for page in tweepy.Cursor(api.get_follower_ids, user_id=user).pages():
            followers.extend(page)
            print(len(followers))
    except tweepy.errors.TweepyException:
        print("error")
        continue
    follower_list.append(followers)

df = pd.DataFrame(columns=['source', 'target'])  # DataFrame vazio
# Defina a lista de seguidores como a coluna de destino
df['target'] = follower_list[0]
df['source'] = me.id  # Define meu ID de usuário como source

display(df)

G = nx.from_pandas_edgelist(df, 'source', 'target')  # Transforma df em gráfico
pos = nx.spring_layout(G)  # especifica layout

f, ax = plt.subplots(figsize=(10, 10))
plt.style.use('ggplot')
nodes = nx.draw_networkx_nodes(G, pos, alpha=0.8)
nodes.set_edgecolor('k')

nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.2)
nx.draw(G)
plt.savefig("BarbrinassFollowers.png")


# Use a lista de seguidores que extraímos no código acima
user_list = list(df['target'])
for userID in user_list:
    print(userID)
    followers = []
    follower_list = []

    # busca o usuário
    user = api.get_user(user_id=userID)

    # buscan a contagem de seguidores
    followers_count = user.followers_count

    try:
        for page in tweepy.Cursor(api.get_follower_ids, user_id=userID).pages():
            followers.extend(page)
            print(len(followers))
            if followers_count >= 5000:  # Pega apenas os primeiros 5.000 seguidores
                break
    except tweepy.errors.TweepyException:
        print("error")
        continue
    follower_list.append(followers)
    temp = pd.DataFrame(columns=['source', 'target'])
    temp['target'] = follower_list[0]
    temp['source'] = userID
    df = df.append(temp)
    df.to_csv("networkOfFollowers.csv")


df = pd.read_csv("networkOfFollowers.csv")  # Lê em um df
display(df)

G = nx.from_pandas_edgelist(df, 'source', 'target')

G.number_of_nodes()  # Encontra o número total de nós neste gráfico

G_sorted = pd.DataFrame(sorted(G.degree, key=lambda x: x[1], reverse=True))
G_sorted.columns = ['nconst', 'degree']
G_sorted.head()

u = api.get_user(user_id=1034409277551796224)
u.screen_name

G_tmp = nx.k_core(G, 4)  # Exclui nós com grau menor que 4

partition = community_louvain.best_partition(
    G_tmp)  # Transforma partição em dataframe
partition1 = pd.DataFrame([partition]).T
partition1 = partition1.reset_index()
partition1.columns = ['names', 'group']

display(partition1)

G_sorted = pd.DataFrame(sorted(G_tmp.degree, key=lambda x: x[1], reverse=True))
G_sorted.columns = ['names', 'degree']
G_sorted.head()
dc = G_sorted

display(dc)

combined = pd.merge(dc, partition1, how='left',
                    left_on='names', right_on='names')

display(combined)

pos = nx.spring_layout(G_tmp)
f, ax = plt.subplots(figsize=(10, 10))
plt.style.use('ggplot')  # cc = nx.betweenness_centrality(G2)
nodes = nx.draw_networkx_nodes(G_tmp, pos,
                               cmap=plt.cm.Set1,
                               node_color=combined['group'],
                               alpha=0.8)
nodes.set_edgecolor('k')
nx.draw_networkx_labels(G_tmp, pos, font_size=4)
nx.draw_networkx_edges(G_tmp, pos, width=1.0, alpha=0.2)
plt.savefig('twitterFollowers.png')

combined = combined.rename(columns={"names": "Id"})
edges = nx.to_pandas_edgelist(G_tmp)
nodes = combined['Id']
edges.to_csv("edges.csv", index=False)
combined.to_csv("nodes.csv", index=False)
