#imports 
import networkx as nx
import numpy as np
from nltk.tokenize import word_tokenize ,sent_tokenize
from nltk.corpus import stopwords
import pandas as pd
import string
from nltk import pos_tag
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from nltk import pos_tag

#Fp
import itertools
import json
import numpy as np
import copy
import sys

#Hup
from  itertools import chain

def create_initialset(dataset):
    retDict = {}
    midlist = []
    for trans in dataset:
        if trans in midlist:
            retDict[frozenset(trans)] = retDict[frozenset(trans)] +1
        else:
            retDict[frozenset(trans)] = 1
        midlist.append(trans)
    return retDict

def sorter(income):
    for ii in Dataset:
        tmp =[]
        tmp2 =[]
        for i in income:
            if i in ii:
                tmp.append(ii.index(i))
            else:
                break
        tmp.sort()
        for i in tmp:
            tmp2.append(ii[i])
        if len(tmp2) == len(income):
            out = tmp2 
            break
    return out



#class of FP TREE node
class TreeNode:
    def __init__(self, Node_name,counter,parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def increment_counter(self, counter):
        self.count += counter


#To create Headertable and ordered itemsets for FP Tree
def create_FPTree(dataset, minSupport):
    HeaderTable = {}
    #term frequent of all items
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item,0) + dataset[transaction]
    #delete min item
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del(HeaderTable[k])
            
    frequent_itemset = set(HeaderTable.keys())
    #ops not have any item
    if len(frequent_itemset) == 0:
        return None, None
    #add new part to value of headertable 
    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]
    #crate null set
    retTree = TreeNode('Null Set',1,None)
    for itemset,count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            # to apply min support
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
        #if didn't com any item from ttemset skip that
        if len(frequent_transaction) > 0:
            #to get ordered itemsets form transactions
            # this part break the order 
            global ordered_itemset
            ordered_itemset = [v[0] for v in sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)]
            #to update the FPTree
            updateTree(ordered_itemset, retTree, HeaderTable, count)
    return retTree, HeaderTable


#To create the FP Tree using ordered itemsets
def updateTree(itemset, FPTree, HeaderTable, count):
    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].increment_counter(count)
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])

    if len(itemset) > 1:
        updateTree(itemset[1::], FPTree.children[itemset[0]], HeaderTable, count)

#To update the link of node in FP Tree
def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node

#To transverse FPTree in upward direction
def FPTree_uptransveral(leaf_Node, prefixPath):
    if leaf_Node.parent != None:
        prefixPath.append(leaf_Node.name)
        FPTree_uptransveral(leaf_Node.parent, prefixPath)

#To find conditional Pattern Bases
def find_prefix_path(basePat, TreeNode):
    Conditional_patterns_base = {}

    while TreeNode != None:
        prefixPath = []
        FPTree_uptransveral(TreeNode, prefixPath)
        if len(prefixPath) > 1:
            Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
        TreeNode = TreeNode.nodeLink
    return Conditional_patterns_base

def Mine_Tree(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    if HeaderTable == None:
        bigL = []
    else:
        bigL = [v[0] for v in sorted(HeaderTable.items(),key=lambda p: p[1][0])]
    
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        #add frequent itemset to final list of frequent itemsets
        sort_new_frequentset = sorter(new_frequentset)
        if len(new_frequentset) > 1:
            frequent_itemset.update({tuple(sort_new_frequentset):max([HeaderTable[w][1].count for w in list(HeaderTable.keys())])})

        #get all conditional pattern bases for item or itemsets
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        

        #call FP Tree construction to make conditional FP Tree
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases,minSupport)

        if Conditional_header != None:
            Mine_Tree(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)


def Fp_growth(dataset , min_Support):                

    
    
    global Dataset
    Dataset = dataset
    initSet = create_initialset(dataset)
    FPtree, HeaderTable = create_FPTree(initSet, min_Support)
    frequent_itemset = dict()
    #call function to mine all ferquent itemsets
    Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)
    return frequent_itemset

def myfrozenset(alllist):
    unique_list = []

    # traverse for all elements
    for x in alllist:
    # check if exists in unique_list or not \n",
        if x not in unique_list:
            unique_list.append(x) 
    return tuple(unique_list)


    
def HUP(Fp,data,sigma):

    wordfreq = []

    tmp = list(chain.from_iterable(list(Fp.keys())))

    for w in (myfrozenset(tmp)):
        wordfreq.append(list(chain.from_iterable(data)).count(w))  
    utility =  dict(list(zip(myfrozenset(tmp), wordfreq))) #key is unic word and value is word frequece

    def U(item):#Definition 2
        sum_ = 0
        if item == '':
            return(sum_)
        tmp = list(item)
        for j in tmp:
            sum_ += utility[j]
        return(sum_)

    def lists_overlap(I1, I2):
        I1 = list(I1)
        I2 = list(I2)
        tmp = []
        for i in I1:
            if i in I2:
                tmp.append(i)
        return tmp

    def O(item1,item2):
        return U(lists_overlap(item1,item2)) / (U(item1) + U(item2) - U(lists_overlap(item1,item2)))

    P = dict()
    deleted_query = []
    K = 200#len(Fp)
    for q,q_ in (Fp.items()):
        if len(P) <= K:
            #calculate pattern utility
            uq = U(q)
            sortP = sorted(P, key=P.get ,reverse=True)#######
            count = 0
            for p in sortP:
                #calculate overlap-degree
                o_p_q = O(p,q)
                if o_p_q > sigma:
                    if uq > P[p]:
                        deleted_query.append(p)
                        count += 1
                    else:
                        break
                else:
                    count += 1
            if count == len(P):
                P.update({q:uq})
                for itm in deleted_query:
                    del P[itm]
            deleted_query = []
        else:
            break
    return P


class KeywordExtractor :
    def __init__(self,lang,hu_hiper = 0.4,Number_of_keywords=10):
        self.lang = lang
        self.hu_hiper = hu_hiper
        self.Number_of_keywords = Number_of_keywords
        self.Stopwords = {
'en' : ['somehow', 'which', 'before', 'three', 'or', 'should', 'might', 'own', 'those', 'to', 'above', 'nor', 'me', 'seems', 'after', 'empty', 'put', 'that', 'will', 'while', 'across', 'been', 'something', 'ie', 'from', 'eight', 'herein', 'below', 'into', 'fifty', 'it', 'when', 'for', 'fifteen', 'top', 'hers', 'anyway', 'between', 'nevertheless', 'the', 'still', 'whither', 'and', 'found', 'our', 'through', 'have', 'whereupon', 'without', 'off', 'am', 'at', 'beside', 'four', 'himself', 'move', 'him', 'be', 'out', 'its', 'thereupon', 'third', 'well', 'yet', 'such', 'themselves', 'as', 'thereafter', 'what', 'whoever', 'sincere', 'until', 'too', 'many', 'not', 'whom', 'again', 'he', 'else', 'latter', 'of', 'on', 'anywhere', 'towards', 'done', 'same', 'side', 'almost', 'find', 'upon', 'everything', 'hundred', 'often', 'thru', 'twenty', 'are', 'afterwards', 'beforehand', 'bottom', 'except', 'ours', 'forty', 'rather', 'either', 'meanwhile', 'since', 'then', 'thereby', 'because', 'once', 'whatever', 'wherein', 'you', 'do', 'everywhere', 'during', 'front', 'she', 'detail', 'indeed', 'system', 'thin', 'name', 'his', 'others', 'somewhere', 'now', 'whereafter', 'is', 'whereas', 'around', 'more', 'cannot', 'onto', 'seem', 'whole', 'much', 'very', 'cry', 'hasnt', 'any', 'sometime', 'alone', 'etc', 'my', 'seeming', 'throughout', 'up', 'their', 'anyone', 'can', 'yours', 'thus', 'take', 'nine', 'along', 'itself', 'ten', 'thence', 'there', 'enough', 'further', 'go', 'interest', 'due', 'hereafter', 'few', 'back', 'formerly', 'here', 'nobody', 'only', 'whenever', 'each', 'moreover', 'anyhow', 'how', 'also', 'un', 'amoungst', 'may', 'hereupon', 'otherwise', 'us', 'was', 'give', 'over', 'some', 'under', 'than', 'becoming', 'amongst', 'mine', 'next', 'fill', 'first', 'please', 'so', 'though', 'another', 'beyond', 'perhaps', 'see', 'fire', 'yourself', 'none', 'whence', 'i', 'has', 'yourselves', 'full', 'noone', 'six', 'all', 'being', 'thick', 'least', 'latterly', 'ltd', 'seemed', 'where', 'together', 'eg', 'other', 'show', 'whether', 'herself', 'among', 'therefore', 'in', 'this', 'made', 'although', 'against', 'hereby', 'wherever', 'de', 'five', 'already', 'could', 'two', 'your', 'never', 'eleven', 'most', 'sixty', 'a', 'however', 'one', 'but', 'her', 'if', 'call', 'get', 'sometimes', 'twelve', 'within', 'mill', 'an', 'nowhere', 'must', 'con', 'everyone', 'per', 'these', 'bill', 'keep', 'neither', 'myself', 'serious', 'we', 'whereby', 'nothing', 'always', 'amount', 'becomes', 'namely', 'behind', 'last', 'mostly', 'therein', 'why', 'even', 'couldnt', 'ever', 'became', 'every', 'down', 'about', 'elsewhere', 'ourselves', 'co', 're', 'by', 'who', 'via', 'former', 'several', 'toward', 'both', 'would', 'someone', 'no', 'whose', 'less', 'describe', 'hence', 'anything', 'them', 'cant', 'they', 'inc', 'part', 'had', 'become', 'were', 'besides', 'with'],
'fr' : ['a', '??', '??', 'abord', 'afin', 'ah', 'ai', 'aie', 'ainsi', 'allaient', 'allo', 'all??', 'allons', 'apr??s', 'assez', 'attendu', 'au', 'aucun', 'aucune', 'aujourd', "aujourd'hui", 'auquel', 'aura', 'auront', 'aussi', 'autre', 'autres', 'aux', 'auxquelles', 'auxquels', 'avaient', 'avais', 'avait', 'avant', 'avec', 'avoir', 'ayant', 'b', 'bah', 'beaucoup', 'bien', 'bigre', 'boum', 'bravo', 'brrr', 'c', '??a', 'car', 'ce', 'ceci', 'cela', 'celle', 'celle-ci', 'celle-l??', 'celles', 'celles-ci', 'celles-l??', 'celui', 'celui-ci', 'celui-l??', 'cent', 'cependant', 'certain', 'certaine', 'certaines', 'certains', 'certes', 'ces', 'cet', 'cette', 'ceux', 'ceux-ci', 'ceux-l??', 'chacun', 'chaque', 'cher', 'ch??re', 'ch??res', 'chers', 'chez', 'chiche', 'chut', 'ci', 'cinq', 'cinquantaine', 'cinquante', 'cinquanti??me', 'cinqui??me', 'clac', 'clic', 'combien', 'comme', 'comment', 'compris', 'concernant', 'contre', 'couic', 'crac', 'd', 'da', 'dans', 'de', 'debout', 'dedans', 'dehors', 'del??', 'depuis', 'derri??re', 'des', 'd??s', 'd??sormais', 'desquelles', 'desquels', 'dessous', 'dessus', 'deux', 'deuxi??me', 'deuxi??mement', 'devant', 'devers', 'devra', 'diff??rent', 'diff??rente', 'diff??rentes', 'diff??rents', 'dire', 'divers', 'diverse', 'diverses', 'dix', 'dix-huit', 'dixi??me', 'dix-neuf', 'dix-sept', 'doit', 'doivent', 'donc', 'dont', 'douze', 'douzi??me', 'dring', 'du', 'duquel', 'durant', 'e', 'effet', 'eh', 'elle', 'elle-m??me', 'elles', 'elles-m??mes', 'en', 'encore', 'entre', 'envers', 'environ', 'es', '??s', 'est', 'et', 'etant', '??taient', '??tais', '??tait', '??tant', 'etc', '??t??', 'etre', '??tre', 'eu', 'euh', 'eux', 'eux-m??mes', 'except??', 'f', 'fa??on', 'fais', 'faisaient', 'faisant', 'fait', 'feront', 'fi', 'flac', 'floc', 'font', 'g', 'gens', 'h', 'ha', 'h??', 'hein', 'h??las', 'hem', 'hep', 'hi', 'ho', 'hol??', 'hop', 'hormis', 'hors', 'hou', 'houp', 'hue', 'hui', 'huit', 'huiti??me', 'hum', 'hurrah', 'i', 'il', 'ils', 'importe', 'j', 'je', 'jusqu', 'jusque', 'k', 'l', 'la', 'l??', 'laquelle', 'las', 'le', 'lequel', 'les', 'l??s', 'lesquelles', 'lesquels', 'leur', 'leurs', 'longtemps', 'lorsque', 'lui', 'lui-m??me', 'm', 'ma', 'maint', 'mais', 'malgr??', 'me', 'm??me', 'm??mes', 'merci', 'mes', 'mien', 'mienne', 'miennes', 'miens', 'mille', 'mince', 'moi', 'moi-m??me', 'moins', 'mon', 'moyennant', 'n', 'na', 'ne', 'n??anmoins', 'neuf', 'neuvi??me', 'ni', 'nombreuses', 'nombreux', 'non', 'nos', 'notre', 'n??tre', 'n??tres', 'nous', 'nous-m??mes', 'nul', 'o', 'o|', '??', 'oh', 'oh??', 'ol??', 'oll??', 'on', 'ont', 'onze', 'onzi??me', 'ore', 'ou', 'o??', 'ouf', 'ouias', 'oust', 'ouste', 'outre', 'p', 'paf', 'pan', 'par', 'parmi', 'partant', 'particulier', 'particuli??re', 'particuli??rement', 'pas', 'pass??', 'pendant', 'personne', 'peu', 'peut', 'peuvent', 'peux', 'pff', 'pfft', 'pfut', 'pif', 'plein', 'plouf', 'plus', 'plusieurs', 'plut??t', 'pouah', 'pour', 'pourquoi', 'premier', 'premi??re', 'premi??rement', 'pr??s', 'proche', 'psitt', 'puisque', 'q', 'qu', 'quand', 'quant', 'quanta', 'quant-??-soi', 'quarante', 'quatorze', 'quatre', 'quatre-vingt', 'quatri??me', 'quatri??mement', 'que', 'quel', 'quelconque', 'quelle', 'quelles', 'quelque', 'quelques', "quelqu'un", 'quels', 'qui', 'quiconque', 'quinze', 'quoi', 'quoique', 'r', 'revoici', 'revoil??', 'rien', 's', 'sa', 'sacrebleu', 'sans', 'sapristi', 'sauf', 'se', 'seize', 'selon', 'sept', 'septi??me', 'sera', 'seront', 'ses', 'si', 'sien', 'sienne', 'siennes', 'siens', 'sinon', 'six', 'sixi??me', 'soi', 'soi-m??me', 'soit', 'soixante', 'son', 'sont', 'sous', 'stop', 'suis', 'suivant', 'sur', 'surtout', 't', 'ta', 'tac', 'tant', 'te', 't??', 'tel', 'telle', 'tellement', 'telles', 'tels', 'tenant', 'tes', 'tic', 'tien', 'tienne', 'tiennes', 'tiens', 'toc', 'toi', 'toi-m??me', 'ton', 'touchant', 'toujours', 'tous', 'tout', 'toute', 'toutes', 'treize', 'trente', 'tr??s', 'trois', 'troisi??me', 'troisi??mement', 'trop', 'tsoin', 'tsouin', 'tu', 'u', 'un', 'une', 'unes', 'uns', 'v', 'va', 'vais', 'vas', 'v??', 'vers', 'via', 'vif', 'vifs', 'vingt', 'vivat', 'vive', 'vives', 'vlan', 'voici', 'voil??', 'vont', 'vos', 'votre', 'v??tre', 'v??tres', 'vous', 'vous-m??mes', 'vu', 'w', 'x', 'y', 'z', 'zut', 'alors', 'aucuns', 'bon', 'devrait', 'dos', 'droite', 'd??but', 'essai', 'faites', 'fois', 'force', 'haut', 'ici', 'juste', 'maintenant', 'mine', 'mot', 'nomm??s', 'nouveaux', 'parce', 'parole', 'personnes', 'pi??ce', 'plupart', 'seulement', 'soyez', 'sujet', 'tandis', 'valeur', 'voie', 'voient', '??tat', '??tions'],
'pl' : ['ach', 'aj', 'albo', 'bardzo', 'bez', 'bo', 'by??', 'ci', 'ci??', 'ciebie', 'co', 'czy', 'daleko', 'dla', 'dlaczego', 'dlatego', 'do', 'dobrze', 'dok??d', 'do????', 'du??o', 'dwa', 'dwaj', 'dwie', 'dwoje', 'dzi??', 'dzisiaj', 'gdyby', 'gdzie', 'go', 'ich', 'ile', 'im', 'inny', 'ja', 'j??', 'jak', 'jakby', 'jaki', 'je', 'jeden', 'jedna', 'jedno', 'jego', 'jej', 'jemu', 'je??li', 'jest', 'jestem', 'je??eli', 'ju??', 'ka??dy', 'kiedy', 'kierunku', 'kto', 'ku', 'lub', 'ma', 'maj??', 'mam', 'mi', 'mn??', 'mnie', 'moi', 'm??j', 'moja', 'moje', 'mo??e', 'mu', 'my', 'na', 'nam', 'nami', 'nas', 'nasi', 'nasz','nasza', 'nasze', 'natychmiast', 'ni??', 'nic', 'nich', 'nie', 'niego', 'niej', 'niemu', 'nigdy', 'nim', 'nimi', 'ni??', 'obok', 'od', 'oko??o', 'on', 'ona', 'one', 'oni', 'ono', 'owszem', 'po', 'pod', 'poniewa??', 'przed', 'przedtem', 's??', 'sam', 'sama', 'si??', 'sk??d', 'tak', 'taki', 'tam', 'ten', 'to', 'tob??', 'tobie', 'tu', 'tutaj', 'twoi', 'tw??j', 'twoja', 'twoje', 'ty', 'wam', 'wami', 'was', 'wasi', 'wasz', 'wasza', 'wasze', 'we', 'wi??c', 'wszystko', 'wtedy', 'wy', '??aden', 'zawsze', '??e', 'a', 'aby', 'acz', 'aczkolwiek', 'ale', 'ale??', 'a??', 'bardziej', 'bowiem', 'by', 'byli', 'bynajmniej', 'by??', 'by??a', 'by??o', 'by??y', 'b??dzie', 'b??d??', 'cali', 'ca??a', 'ca??y', 'cokolwiek', 'co??', 'czasami', 'czasem', 'czemu', 'czyli', 'gdy', 'gdy??', 'gdziekolwiek', 'gdzie??', 'i', 'inna', 'inne', 'innych', 'i??', 'jaka??', 'jakich??', 'jakie', 'jaki??', 'jaki??', 'jakkolwiek', 'jako', 'jako??', 'jednak', 'jednak??e', 'jeszcze', 'kilka', 'kim??', 'ktokolwiek', 'kto??', 'kt??ra', 'kt??re', 'kt??rego','kt??rej', 'kt??ry', 'kt??rych', 'kt??rym', 'kt??rzy', 'lat', 'lecz', 'mimo', 'mi??dzy', 'mog??', 'moim', 'mo??liwe', 'mo??na', 'musi', 'nad', 'naszego', 'naszych', 'natomiast', 'nawet', 'no', 'o', 'oraz', 'pan', 'pana', 'pani', 'podczas', 'pomimo', 'ponad', 'powinien', 'powinna', 'powinni', 'powinno', 'poza', 'prawie', 'przecie??', 'przede', 'przez', 'przy', 'roku', 'r??wnie??', 'sobie', 'sob??', 'spos??b', 'swoje', 'ta', 'taka', 'takie', 'tak??e', 'te', 'tego', 'tej', 'teraz', 'te??', 'totob??', 'tote??', 'trzeba', 'twoim', 'twym', 'tych', 'tylko', 'tym', 'u', 'w', 'wed??ug', 'wiele', 'wielu', 'wi??cej','wszyscy', 'wszystkich', 'wszystkie', 'wszystkim', 'w??a??nie', 'z', 'za', 'zapewne', 'zeznowu', 'zn??w', 'zosta??', '??adna', '??adne', '??adnych', '??eby'],
'pt' : ['acerca', 'agora', 'algmas', 'alguns', 'ali', 'ambos', 'antes', 'apontar', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'atr??s', 'bem', 'bom', 'cada', 'caminho', 'cima', 'com', 'como', 'comprido', 'conhecido', 'corrente', 'das', 'debaixo', 'dentro', 'desde', 'desligado', 'deve', 'devem', 'dever??', 'direita', 'diz', 'dizer', 'dois', 'dos', 'e', '??', 'ela', 'ele', 'eles', 'em', 'enquanto', 'ent??o', 'est??', 'estado', 'est??o', 'estar', 'estar??', 'este', 'estes', 'esteve', 'estive', 'estivemos', 'estiveram', 'eu', 'far??', 'faz', 'fazer', 'fazia', 'fez', 'fim', 'foi', 'fora', 'horas', 'iniciar', 'inicio', 'ir', 'ir??', 'ista', 'iste', 'isto', 'ligado', 'maioria', 'maiorias', 'mais', 'mas', 'mesmo', 'meu', 'muito', 'muitos', 'n??o', 'nome', 'n??s', 'nosso', 'novo', 'o', 'onde', 'os', 'ou', 'outro', 'para', 'parte', 'pegar', 'pelo', 'pessoas', 'pode', 'poder??', 'podia', 'por', 'porque', 'povo', 'promeiro', 'qual', 'qualquer', 'quando', 'qu??', 'quem', 'quieto', 'saber', 's??o', 'sem', 'ser', 'seu', 'somente', 'tal', 'tamb??m', 'tem', 't??m', 'tempo', 'tenho', 'tentar', 'tentaram', 'tente', 'tentei', 'teu', 'teve', 'tipo', 'tive', 'todos', 'trabalhar', 'trabalho', 'tu', '??ltimo', 'um', 'uma', 'umas', 'uns', 'usa', 'usar', 'valor', 'veja', 'ver', 'verdade', 'verdadeiro', 'voc??', 'a', '??', 'adeus', 'a??', 'ainda', 'al??m', 'algo', 'algumas', 'ano', 'anos', 'ao', 'aos', 'apenas', 'apoio', 'ap??s', 'aquilo', '??rea', 'as', '??s', 'assim', 'at??', 'atrav??s', 'baixo', 'bastante', 'boa', 'boas', 'bons', 'breve', 'c??', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cinco', 'coisa', 'conselho', 'contra', 'custa', 'da', 'd??', 'd??o', 'daquela', 'daquelas', 'daquele', 'daqueles', 'dar', 'de', 'demais', 'depois', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes', 'dez', 'dezanove', 'dezasseis', 'dezassete', 'dezoito', 'dia', 'diante', 'dizem', 'do', 'doze', 'duas', 'd??vida', 'elas', 'embora', 'entre', 'era', '??s', 'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'est??s', 'estava', 'estiveste', 'estivestes', 'estou', 'exemplo', 'fa??o', 'falta', 'favor', 'fazeis', 'fazem', 'fazemos', 'fazes', 'final', 'fomos', 'for', 'foram', 'forma', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'h??', 'hoje', 'hora', 'isso', 'j??', 'l??', 'lado', 'local', 'logo', 'longe', 'lugar', 'maior', 'mal', 'm??ximo', 'me', 'meio', 'menor', 'menos', 'm??s', 'meses', 'meus', 'mil', 'minha', 'minhas', 'momento', 'na', 'nada', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'n??vel', 'no', 'noite', 'nos', 'nossa', 'nossas', 'nossos', 'nova', 'novas', 'nove', 'novos', 'num', 'numa', 'n??mero', 'nunca', 'obra', 'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'ontem', 'onze', 'outra', 'outras', 'outros', 'parece', 'partir', 'paucas', 'pela', 'pelas', 'pelos', 'perto', 'p??de', 'podem', 'poder', 'p??e', 'p??em', 'ponto', 'pontos', 'porqu??', 'posi????o', 'poss??vel', 'possivelmente', 'posso', 'pouca', 'pouco', 'poucos', 'primeira', 'primeiras', 'primeiro', 'primeiros', 'pr??pria', 'pr??prias', 'pr??prio', 'pr??prios', 'pr??xima', 'pr??ximas', 'pr??ximo', 'pr??ximos', 'puderam', 'qu??is', 'quanto', 'quarta', 'quarto', 'quatro', 'que', 'quer', 'quereis', 'querem', 'queremas', 'queres', 'quero', 'quest??o', 'quinta', 'quinto', 'quinze', 'rela????o', 'sabe', 'sabem', 'se', 'segunda', 'segundo', 'sei', 'seis', 'sempre', 'seria', 'sete', 's??tima', 's??timo', 'seus', 'sexta', 'sexto', 'sim', 'sistema', 'sob', 'sobre', 'sois', 'somos', 'sou','sua', 'suas', 'talvez', 'tanta', 'tantas', 'tanto', 't??o', 'tarde', 'te', 'temos', 'tendes', 'tens', 'ter', 'terceira', 'terceiro', 'teus', 'tivemos', 'tiveram', 'tiveste', 'tivestes', 'toda', 'todas', 'todo', 'tr??s', 'treze', 'tua', 'tuas', 'tudo', 'vai', 'vais', 'v??o', 'v??rios', 'vem', 'v??m', 'vens', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'voc??s', 'vos', 'v??s', 'vossa', 'vossas', 'vosso', 'vossos', 'zero'],
'es' : ['alg??n', 'alguna', 'algunas', 'alguno', 'algunos', 'ambos', 'ampleamos', 'ante', 'antes', 'aquel', 'aquellas', 'aquellos', 'aqui', 'arriba', 'atras', 'bajo', 'bastante', 'bien', 'cada', 'cierta', 'ciertas', 'cierto', 'ciertos', 'como', 'con', 'conseguimos', 'conseguir', 'consigo', 'consigue', 'consiguen', 'consigues', 'cual', 'cuando', 'dentro', 'desde', 'donde', 'dos', 'el', 'ellas', 'ellos', 'empleais', 'emplean', 'emplear', 'empleas', 'empleo', 'en', 'encima', 'entonces', 'entre', 'era', 'eramos', 'eran', 'eras', 'eres', 'es', 'esta', 'estaba', 'estado', 'estais', 'estamos', 'estan', 'estoy', 'fin', 'fue', 'fueron', 'fui', 'fuimos', 'gueno', 'ha', 'hace', 'haceis', 'hacemos', 'hacen', 'hacer', 'haces', 'hago', 'incluso', 'intenta', 'intentais', 'intentamos', 'intentan', 'intentar', 'intentas', 'intento', 'ir', 'la', 'largo', 'las', 'lo', 'los', 'mientras', 'mio', 'modo', 'muchos', 'muy', 'nos', 'nosotros', 'otro', 'para', 'pero', 'podeis', 'podemos', 'poder', 'podria', 'podriais', 'podriamos', 'podrian', 'podrias', 'por', 'por qu??', 'porque', 'primero', 'puede', 'pueden', 'puedo', 'quien', 'sabe', 'sabeis', 'sabemos', 'saben', 'saber', 'sabes', 'ser', 'si', 'siendo', 'sin', 'sobre', 'sois', 'solamente', 'solo', 'somos', 'soy', 'su', 'sus', 'tambi??n', 'teneis', 'tenemos', 'tener', 'tengo', 'tiempo', 'tiene', 'tienen', 'todo', 'trabaja', 'trabajais', 'trabajamos', 'trabajan', 'trabajar', 'trabajas', 'trabajo', 'tras', 'tuyo', 'ultimo', 'un', 'una', 'unas', 'uno', 'unos', 'usa', 'usais', 'usamos', 'usan', 'usar', 'usas', 'uso', 'va', 'vais', 'valor', 'vamos', 'van', 'vaya', 'verdad', 'verdadera', 'verdadero', 'vosotras', 'vosotros', 'voy', 'yo', '??l', '??sta', '??stas', '??ste', '??stos', '??ltima', '??ltimas', '??ltimo', '??ltimos', 'a', 'a??adi??', 'a??n', 'actualmente', 'adelante', 'adem??s', 'afirm??', 'agreg??', 'ah??', 'ahora', 'al', 'algo', 'alrededor', 'anterior', 'apenas', 'aproximadamente', 'aqu??', 'as??', 'asegur??', 'aunque', 'ayer', 'buen', 'buena', 'buenas', 'bueno', 'buenos', 'c??mo', 'casi', 'cerca', 'cinco', 'coment??', 'conocer', 'consider??', 'considera', 'contra', 'cosas', 'creo', 'cuales', 'cualquier', 'cuanto', 'cuatro', 'cuenta', 'da','dado', 'dan', 'dar', 'de', 'debe', 'deben', 'debido', 'decir', 'dej??', 'del', 'dem??s', 'despu??s', 'dice', 'dicen', 'dicho', 'dieron', 'diferente', 'diferentes', 'dijeron', 'dijo', 'dio', 'durante', 'e', 'ejemplo', 'ella', 'ello', 'embargo', 'encuentra', 'esa', 'esas', 'ese', 'eso', 'esos', 'est??', 'est??n', 'estaban', 'estar', 'estar??', 'estas', 'este', 'esto', 'estos', 'estuvo', 'ex', 'existe', 'existen', 'explic??', 'expres??', 'fuera', 'gran', 'grandes', 'hab??a', 'hab??an', 'haber', 'habr??', 'hacerlo', 'hacia', 'haciendo', 'han', 'hasta', 'hay', 'haya', 'he', 'hecho', 'hemos', 'hicieron', 'hizo', 'hoy', 'hubo', 'igual', 'indic??', 'inform??', 'junto', 'lado', 'le', 'les', 'lleg??', 'lleva', 'llevar', 'luego', 'lugar', 'm??s', 'manera', 'manifest??', 'mayor', 'me', 'mediante', 'mejor', 'mencion??', 'menos', 'mi', 'misma', 'mismas', 'mismo', 'mismos', 'momento', 'mucha', 'muchas', 'mucho', 'nada', 'nadie', 'ni', 'ning??n', 'ninguna', 'ningunas', 'ninguno', 'ningunos', 'no', 'nosotras', 'nuestra', 'nuestras', 'nuestro', 'nuestros', 'nueva', 'nuevas', 'nuevo', 'nuevos', 'nunca', 'o', 'ocho', 'otra', 'otras', 'otros', 'parece', 'parte', 'partir', 'pasada', 'pasado', 'pesar', 'poca', 'pocas', 'poco', 'pocos', 'podr??', 'podr??n', 'podr??a', 'podr??an', 'poner', 'posible', 'pr??ximo', 'pr??ximos', 'primer', 'primera', 'primeros', 'principalmente', 'propia', 'propias', 'propio', 'propios', 'pudo', 'pueda', 'pues', 'qu??', 'que', 'qued??', 'queremos', 'qui??n', 'quienes', 'quiere', 'realiz??', 'realizado', 'realizar', 'respecto', 's??', 's??lo', 'se', 'se??al??', 'sea', 'sean', 'seg??n','segunda', 'segundo', 'seis', 'ser??', 'ser??n', 'ser??a', 'sido', 'siempre', 'siete', 'sigue', 'siguiente', 'sino', 'sola', 'solas', 'solos', 'son', 'tal', 'tampoco', 'tan', 'tanto', 'ten??a', 'tendr??', 'tendr??n', 'tenga', 'tenido', 'tercera', 'toda', 'todas', 'todav??a', 'todos', 'total', 'trata', 'trav??s', 'tres', 'tuvo', 'usted', 'varias', 'varios', 'veces', 'ver', 'vez', 'y', 'ya'],
'fa' : ['????????????', '????????????', '??????', '??????', '????????', '????', '????', '????', '??????????', '??????????', '????????', '????????', '??????????', '????????', '??????????', '??????????', '????????', '??????????', '????????', '????????', '??????', '??????????', '??????', '????????', '????????', '??????', '??????????', '????????', '????????', '????????', '????????', '??????????', '????????????????', '????', '????????', '????????', '????????', '????', '??????????', '??????????', '????????', '??????', '????????????', '????????', '??????', '????????', '??????????', '??????', '????????', '??????????', '??????', '????????', '??????????', '????????', '????????', '??????????', '??????', '??????', '??????', '????', '????????', '????????????', '????????', '????????', '????????', '??????', '??????', '??????', '??????', '??????????', '??????', '????????', '??????????', '??????', '????????', '??????', '??????????', '????????', '??????', '??????????', '??????', '????????','??????', '????????????', '????????', '????????', '????????????', '??????', '??????', '??????', '??????????', '??????', '????????', '????????', '??????????', '????????', '??????????', '??????', '????????', '????????', '??????????', '????????', '??????????', '??????????', '??????', '????????', '??????', '??????', '??????', '????????', '??????', '????????', '??????????', '????????', '??????????', '????????', '??????', '??????', '????', '??????', '??????????', '????????', '??????', '????', '????????', '????????', '????????', '????', '??????', '??????', '????', '????????', '????????', '????????', '????', '????', '????', '????', '????', '??????', '??????', '????', '??????', '????', '????', '????', '????', '??????', '????', '????', '????????', '??', '????', '????', '????','??????','????????','??????????','????????', '????']
}
         
    def __Pos_t(self,word):
        '''
        This function useed for POS Score
        '''
        tag = pos_tag([word])[0][1]
        if 'NN' in tag:
            return 1
        elif 'V' in tag:
            return 0.5
        elif 'jJ' in tag:
            return 0.35
        else:
            return 0.25


    def __calcCentrality(self,G,cnt):
        '''
        For calculating Graph centrality measures
        '''
        cntV = list()
        if cnt == 'deg':
            cntV = list(dict(G.degree).values())
        elif cnt == 'ei':
            cntV = list(nx.eigenvector_centrality_numpy(G).values())
        elif cnt == 'sh':
            cntV = list(nx.constraint(G).values())
        elif cnt == 'pr':
            cntV = list(nx.pagerank_numpy(G).values())
        elif cnt == 'bw':
            cntV = list(nx.betweenness_centrality(G).values())
        elif cnt == 'cl':
            cntV = list(nx.clustering(G).values())
        elif cnt == 'cc':
            cntV = list(nx.closeness_centrality(G).values())
        elif cnt == 'ec':
            cntV = list(nx.eccentricity(G).values())
    
        else:
            raise ValueError('calcCettrality: wrong cnt value or not implemented yet')
        
        return cntV

    def __getPC1(self,mtxFeatures, setCentralities):
        '''
        PC1 Function
        '''
        sc = StandardScaler()
        A = mtxFeatures.loc[:,setCentralities]
        # normalize data
        A = pd.DataFrame(data = sc.fit_transform(A),  columns = list(A))    
        # create the PCA instance
        pca = PCA(n_components=1)
        # fit on data
        pca.fit(A)
        # access values and vectors    
        PC1 = pd.DataFrame(data=pca.components_, columns = list(A))
        return PC1


    def __MCI_PC1(self,G, PC1, N):      
        '''
        calculating Graph measures with generated waiths
        '''
        sc = MinMaxScaler()
        #sc = StandardScaler()
        
        G_Words = pd.DataFrame()
        G_Words['Word'] = list(G.nodes)
        G_Words['MCI'] = np.zeros((len(G.nodes),1))
        for cnt in list(PC1):
            val = pd.DataFrame(self.__calcCentrality(G,cnt))
            # Normalizing the data
            val = sc.fit_transform(val)
            G_Words[cnt] = val
            G_Words['MCI'] += G_Words[cnt]*abs(PC1.loc[0,cnt]) 
        
        keynodes = G_Words.sort_values(by='MCI', ascending=False).loc[:,['Word','MCI']]
        
        if N == -1:
            return keynodes.reset_index(drop=True)
        else: 
            return keynodes.reset_index(drop=True).head(N)



    def __scores(self,g):
        bw = nx.betweenness_centrality(g)
        cc = nx.closeness_centrality(g)
        ei = nx.eigenvector_centrality_numpy(g)
        deg= nx.degree_centrality(g)
        pr = nx.pagerank(g)
        cl = nx.clustering(g)
        ec = nx.eccentricity(g)
        sh = nx.constraint(g)
        
        return bw , cc , ei,deg,pr, cl,ec ,sh
    def __MCI_Centrality(self,tokens):
        tokens = [s.lower() for s in tokens]
        G = nx.Graph()
        for n in set(tokens):
            G.add_node(n)
        for i in range(len(tokens)-2):
            G.add_edge(tokens[i],tokens[i+1])
            G.add_edge(tokens[i],tokens[i+2])
        

        df = pd.DataFrame({'Word' :list(self.__scores(G)[0].keys()),
                        'bw' :list(self.__scores(G)[0].values()),
                        'cc' :list(self.__scores(G)[1].values()),
                        'ei' :list(self.__scores(G)[2].values()),
                        'deg' :list(self.__scores(G)[3].values()),
                        'pr' :list(self.__scores(G)[4].values()),
                        'cl' :list(self.__scores(G)[5].values()),
                        'ec' :list(self.__scores(G)[6].values()),
                        'sh' :list(self.__scores(G)[7].values())})

        setCentralities = ['bw', 'ei', 'cc', 'deg', 'pr', 'cl', 'ec', 'sh']
            
        #PRELOADED MATRIX OF FEATURES (CENTRALITIES) FROM A RESPOSITORY
            
        mtxFeatures = df.drop(['Word'], axis=1) 



        #Number of requested nodes
        N = -1

        PC1 = self.__getPC1(mtxFeatures, setCentralities)
        keywords = self.__MCI_PC1(G, PC1, N)
        c_score = dict()
        for i in range(len(keywords)):
            c_score.update({keywords['Word'][i]:keywords['MCI'][i]})
        return c_score 

    def __posision(self,word,text):
        median = [index for index, value in enumerate(text) if value.lower() == word.lower()]
        return(np.log(np.log(3+(sum(median)/len(median)))))
    def __cast(self,word,text):
        return max(text.count(word.upper()),text.count(word[0].upper()+word[1:].lower()))/ (1+np.log([i.lower()for i in text].count(word.lower())))
        
    def __sentence(self,word,sents):
        return sum(list(map(int,[word.lower() in i.lower() for i in sents])))/ len(sents)

    def __meanTF(self,word,text):
        meanTF = [text.count(i) for i in set(text)]
        return text.count(word) / (sum(meanTF)/len(meanTF))+1

    def __local(self,tokens,sent):
        y_score = dict()
        for word in tokens:
            y_score.update({word.lower():(self.__cast(word,tokens)+self.__sentence(word,sent)+self.__meanTF(word,tokens))+self.__Pos_t(word)/self.__posision(word,tokens)})
            
        return y_score


    def __score(self,text,sent):
        s = dict()
        y = self.__local(text,sent)
        c = self.__MCI_Centrality(text)
        for i in set(list(y.keys())+list(c.keys())):
            if i not in set(list(y.keys())):
                s.update({i:
                0.3 * c[i] 
                })
                continue
            if i not in set(list(c.keys())):
                s.update({i:
                0.3 * y[i] 
                })
                continue
                
            yi = y[i] 
            ci = c[i]
            s.update({i:
                yi * ci 
                })
        return s


    def extract_keywords(self,yourInputText):
        '''
        need some big text
        '''
    
        if self.lang not in self.Stopwords.keys():
            print("'{}' is not a valid language".format(self.lang))
        text = yourInputText
        data = []

        
        data_snt = sent_tokenize(text)
        data_tmp = []
        token = []
        for i in (data_snt):
            tokens = word_tokenize(str(i))
            tokens = [(w) for w in tokens if w.lower() not in self.Stopwords[self.lang] and w not in string.punctuation and w.isalpha()]
            data_tmp.append(tokens)
            token.extend(tokens)
        data.append(data_tmp)
        z = self.__score(token,data_snt)
        # Frequent pattern section
        Hup = dict()

        for i in range(20,1,-1):
            Fp = Fp_growth(data[0],i)
            if len(Fp) == 0:
                continue
            Hup = HUP(Fp,data[0],self.hu_hiper)
            if len(Hup)>7:
                break

        kewords = dict()
        kewordsp = dict()


        Pattern_L =list(Hup.keys())

        for i in Pattern_L:
            mult = 0
            for j in i:
                if j in list(z.keys()) :
                    mult += z[j]
            mult = mult
            kewordsp.update({' '.join(i):mult})

        kewordstm =({k: (v) for k, v in sorted(kewordsp.items(), key=lambda item: item[1] , reverse= True)})

        kewords.update({k: kewordstm[k] for k in list(kewordstm)[:int(self.hu_hiper*10)]})
        kewords.update(z)


        return {k: round(v,2) for k, v in sorted(kewords.items(), key=lambda item: item[1] , reverse= True)[:self.Number_of_keywords]}