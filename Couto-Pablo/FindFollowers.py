import tweepy
import json

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

# Acha seguidores do Pablo
seguidores=[]
try:
    for page in tweepy.Cursor(api.get_follower_ids, user_id=1243708484782370816).pages():
        seguidores.extend(page)
except tweepy.errors.TweepyException:
    print("erro seguidores")
# Acha seguidores do Pablo

seguidores_total=set(seguidores)

# Acha seguidores dos seguidores do Pablo
for userID in seguidores:
    try:
        for page in tweepy.Cursor(api.get_follower_ids, user_id=userID).pages():
            seguidores_total.update(page)
            break
    except tweepy.errors.TweepyException:
        print("erro seguidores de seguidores")
        continue
# Acha seguidores dos seguidores do Pablo

print(seguidores_total)

# Salva em arquivo
with open('./backup/seguidores.txt', 'w') as fp:
    for item in seguidores_total:
        fp.write("%s\n" % str(item))
    print('Done')
fp.close()
# Salva em arquivo