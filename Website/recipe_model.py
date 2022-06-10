
import gensim
import numpy as np
import pandas as pd
import pickle
from numpy import dot
from numpy.linalg import norm
from numba import jit
import datetime

start1 = datetime.datetime.now()
#pip install scikit-learn==1.0.2    

#lst_a
with open ('./model_data/dic2.pkl', 'rb') as f:
  
  dic = pickle.load(f)
#lst_a
with open ('./model_data/lst_a.p', 'rb') as f:
  
  lst_a = pickle.load(f)
   
#title
with open ('./model_data/title.p', 'rb') as f:
  title = pickle.load(f)

#word2vec 불러오기
model = gensim.models.Word2Vec.load('./model_data/wvrecipe')

#co-occurrence matrix 불러오기
with open ('./model_data/ingredients_co.p', 'rb') as f:
  data_matrix = pickle.load(f)


#name_matrix 불러오기
with open ('./model_data/name_matrix.p', 'rb') as f:
  name_matrix = pickle.load(f)


#sim_matrix 불러오기
with open ('./model_data/sim_matrix.p', 'rb') as f:
  sim_matrix = pickle.load(f)


#재료 카테고리
with open ('./model_data/ingredients_list', 'rb') as f:
  ingredients_list = pickle.load(f)


#tfidf 불러오기
with open ('./model_data/tfidf.p', 'rb') as f:
  tfidf_v = pickle.load(f)

#r_v 불러오기
with open ('./model_data/r_v.p', 'rb') as f:
   
  r_v = pickle.load(f)


#########################

@jit(nopython = True)
def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))


def jaccard(lst_s, lst_c):
 
  res = []
  for i in lst_c:
    res2 = 0
    for k in lst_s:
      a = []
      
      for j in i:
        a.append(model.wv.similarity(j,k))
      b = max(a)
      if b <= 0.5:
        b = 0
      res2 += b
    c = res2/len(lst_s)
    res.append(c)

  num = (sum(res)/len(res))
  n = len(lst_s)
  return (n*num-1)/(n-1)


class Recipe_rec:
  def __init__(self, lst):
    self.lst = lst
    
  
  def cosin_m(self, n = 100, p = True):
    d = self.lst
    self.n = n
    self.p = p
    
    i_str = ','.join(d)   #가중치 생성
    sentence = [i_str]
    a = tfidf_v.transform(sentence).toarray().flatten()
    w = []
    for i in d:
        kkk = tfidf_v.vocabulary_[i]
        w.append(a[kkk])
    w2 = []  
    for j in range(len(d)):
        w2.append(w[j]/sum(w))
    matrix = np.zeros(shape=(model.wv.vectors.shape[1],))
    for i in range(len(d)):
        matrix += w2[i]*model.wv[d[i]]
        if p == True:
          print(w2[i])
    result = matrix

    #코사인 유사도 다 구하기
    lst2 = []
    for i in range(len(name_matrix)):
        lst2.append(cos_sim(result,name_matrix[i]))
    #코사인 유사도 상위 개

    self.max_idx = [i for i in np.argsort(lst2)[-n:][::-1]]

    return self.max_idx

  
  def rec_result(self,max_idx, n = 10):
    self.n = n
    self.max_idx = max_idx
    ing_v =[]
    lst = self.lst
    for i in range(len(lst)):
        ing_v.append(model.wv[lst[i]])
        
    ma = []
    for i in max_idx:
        a = []
        for j in lst:
            a.append(sim_matrix[j][lst_a[i]].argmax())
        ma.append(a)   
    
    res_lst = []
    for j in range(len(max_idx)):
        res = 0
        for i in range(len(ma[j])):
            
            m = ma[j][i]
            c = ing_v[i]-r_v[max_idx[j]][m]
            c = c**2
            c_sum = np.sum(c)
            res += c_sum
        res_lst.append(res/len(lst))
    res_lst_a = np.array(res_lst)
    
    dic = dict(zip(max_idx, res_lst_a))
    a = sorted(dic.items(), key=lambda x: x[1])
     
    
    self.n10 = []   
    for i in range(len(a[:n])):
        idx = a[i][0]
        self.n10.append(idx)
        

    return self.n10


class Ing_rec():
  def __init__(self, lst):
    self.lst = lst

  
  def rec(self):
    lst = self.lst
    
    rec_dic = dict(zip(ingredients_list.keys(),[[],[],[],[],[],[],[],[]]))

    ing_co_matrix = data_matrix.copy()
    ing_co_matrix2 = [1]*len(data_matrix)

    for i in lst:
      ing_co_matrix2 *= ing_co_matrix[i]

    cc = list(ing_co_matrix2.nlargest(10).index)
    for j in cc:
      for i in ingredients_list.keys():
        if j in ingredients_list[i]:
          rec_dic[i].append(j)
    if len(lst) >=2:      
      mm = Recipe_rec(lst).cosin_m(n = 100, p = False)      
      lst_c = lst_a[mm]

      jac = jaccard(lst, lst_c)
    else:
      jac = 1
    return jac, rec_dic

end1 = datetime.datetime.now()

print('로딩시간:{}'.format(end1-start1))

# ####처음 컴파일용

# test = ['소고기']
# a = Recipe_rec(test)
# start = datetime.datetime.now()

# max_idx = a.cosin_m()
# result = a.rec_result(max_idx)
# end = datetime.datetime.now()

# print(end-start)



