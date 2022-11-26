import nltk
import matplotlib.pyplot as plt
import networkx as nx
import regex as re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class GraphVisualization:
   
    def __init__(self):
        self.nos=dict()
        self.arestas = dict()
          
    def addNode(self,palavra):
        self.nos[palavra]=self.nos.setdefault(palavra,0)+10
    
    def addEdge(self, a, b):
        self.arestas[frozenset([a,b])]=self.arestas.setdefault(frozenset([a,b]),0)+1
          
    def visualize(self):
        G = nx.Graph()
        remove = {key:val for key, val in self.nos.items() if val <2000}
        self.arestas = {key:val for key, val in self.arestas.items() if list(key)[0] not in remove and list(key)[1] not in remove}
        print("removeu arestas pequenas")
        self.nos = {key:val for key, val in self.nos.items() if val >=2000}
        print("removeu nós pequenos")
        temp=[]
        for x in self.arestas:
            aux=list(x)
            temp.append((aux[0],aux[1],self.arestas[x]))
        print("criou arestas com peso")
        G.add_nodes_from(list(self.nos.keys()))
        G.add_weighted_edges_from(temp)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos,nodelist=list(self.nos.keys()), node_size=list(self.nos.values()))
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, "weight"))
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
        
        
G = GraphVisualization()

with open('./backup/tweets.txt', mode='r',encoding='utf-8') as file:
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
texto = re.sub(r'$', ' ', texto) # remove todo duplo espaco

print("removeu simbolos")

text_tokens=word_tokenize(texto)
tokens_without_swpt=[word for word in text_tokens if not word in (stopwords.words('portuguese'))]
tokens_without_swpten=[word for word in tokens_without_swpt if not word in (stopwords.words('english'))]
texto=' '.join(tokens_without_swpten)

print("removeu stopwords")

data_set=texto.split("; ; ;")

for tweet in range(len(data_set)):
    for palavraChave in data_set[tweet].split():
        G.addNode(palavraChave)
        for palavra in data_set[tweet].replace(palavraChave,'').split():
            G.addEdge(palavraChave, palavra)

print("adicionou nós e arestas")

G.visualize()

    