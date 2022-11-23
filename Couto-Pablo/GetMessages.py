import tweepy
import json
import codecs

# Configuração API
credenciais = open('./Couto-Pablo/credenciais.json').read()
info = json.loads(credenciais)

consumer_key = info['API_ACCESS_PABLO']
consumer_secret = info['API_ACCESS_SECRET_PABLO']
access_key = info['ACCESS_TOKEN_PABLO']
access_secret = info['ACCESS_TOKEN_SECRET_PABLO']

autorizacao = tweepy.OAuthHandler(consumer_key, consumer_secret)
autorizacao.set_access_token(access_key, access_secret)

api = tweepy.API(autorizacao, wait_on_rate_limit=True)
# Configuração API

# Pega seguidores do arquivo
seguidores=[]
with open('./backup/seguidoresNaoRepet.txt', 'r') as filehandle:
    for line in filehandle:
        curr_place = line[:-1]
        seguidores.append(int(curr_place))
filehandle.close()
# Pega seguidores do arquivo

# !!!!!!!!!!! Teste   
seguidores = seguidores[0:300]
# !!!!!!!!!!! Teste  

mensagens=[]

# Pega mensagens de cada seguidor
count=1
for user in seguidores:
    try:
        for status in tweepy.Cursor(api.user_timeline, user_id=user, tweet_mode="extended").items(20):
            mensagens.append(status.full_text)
    except tweepy.errors.TweepyException:
        print("erro mensagens")
    print(count)
    count=count+1
# Pega mensagens de cada seguidor

# Salva em arquivo
file = codecs.open("./backup/tweets.txt", "w", "utf-8")
for item in mensagens:
    file.write(u'{item}')
print('Done')
file.close()
# Salva em arquivo