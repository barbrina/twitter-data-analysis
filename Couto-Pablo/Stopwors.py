import nltk
import matplotlib.pyplot as plt
import networkx as nx
import regex as re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class GraphVisualization:
   
    def __init__(self):
        self.visual = []
          
    def addEdge(self, a, b, peso=1):
        temp = (a, b,peso)
        self.visual.append(temp)
        print(peso)
          
    def visualize(self):
        G = nx.Graph()
        G.add_weighted_edges_from(self.visual)
        pos = nx.spring_layout(G, seed=7)
        nx.draw_networkx_nodes(G, pos, node_size=400)
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, "weight"))
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
        
        
G = GraphVisualization()

with open('../backup/backupTweetTeste.txt', mode='r',encoding='utf-8') as file:
    texto= file.read()
file.close()    

texto = texto.lower() #converte todas as palavras para letras minusculas
texto = re.sub(r'rt', '', texto) # remove todo rt
texto = re.sub(r'@\w+', '', texto) # remove tudo que começar com @
texto = re.sub(r'https://t.co/\w+', '', texto) # remove todos links do twitter
texto = re.sub(r'https', '', texto) # remove todos links do twitter
texto = re.sub(r'\n\s\n', '', texto) # remove toda linha vazia
texto = re.sub(r'\s\s', ' ', texto) # remove todo duplo espaco
texto = re.sub(r'[^\P{P};]+', '', texto) # remove toda pontuação exceto ;

text_tokens=word_tokenize(texto)
tokens_without_swpt=[word for word in text_tokens if not word in (stopwords.words('portuguese'))]
tokens_without_swpten=[word for word in tokens_without_swpt if not word in (stopwords.words('english'))]
texto=' '.join(tokens_without_swpten)

nos=set()
arestas=[]

data_set=texto.split("; ; ;")
print(data_set)

for tweet in range(len(data_set)):
    for palavraChave in data_set[tweet].split():
        nos.add(palavraChave)
        for palavra in data_set[tweet].replace(palavraChave,'').split():
            arestas.append({palavraChave, palavra})
            
print(arestas)
print(nos)

# for tweet in range(len(data_set)):
#     for palavra in data_set[tweet].split():
#         dicionario.setdefault(palavra,set(data_set[tweet].replace(palavra,'').split())).update(data_set[tweet].replace(palavra,'').split())

# for x in dicionario:
#     print (x,"[")
#     for y in dicionario[x]:
#         print(y, end=" ")
    
#     print ("]")


    