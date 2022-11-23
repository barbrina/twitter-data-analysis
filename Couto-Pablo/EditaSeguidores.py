listaIds=set()

with open('./backup/seguidores.txt', 'r') as filehandle:
    for line in filehandle:
        curr_place = line[:-1]
        listaIds.add(int(curr_place))
filehandle.close()
        
# Salva em arquivo
with open('./backup/seguidoresNaoRepet.txt', 'w') as fp:
    for item in listaIds:
        fp.write("%s\n" % str(item))
    print('Done')
fp.close()
# Salva em arquivo