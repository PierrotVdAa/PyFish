"""
Created by Evgeny Ivanov for Emodnet Hackatlon 2019
"""

from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics; from collections import Counter

t,lt,ln,p,temp,s = [],[],[],[],[],[]
for line in open('Altogether_Phyto_Temp_Salt.txt','r').readlines()[:]:
	a=line.split('\t')
	if a[3] != '--' and a[4] != '--' and a[5] != '--':
		t.append(datetime.strptime(a[0], '%Y-%m-%d 00:00:00'))
		lt.append(float(a[1]))
		ln.append(float(a[2]))
		p.append(float(a[3]))
		temp.append(float(a[4]))
		s.append(float(a[5].split('\n')[0]))


tt = np.zeros((366)); k=0
marker = np.zeros((len(t)))
distance = np.zeros((366))
m = np.zeros((366))
lt2,ln2,p2,temp2,s2,m2 = [],[],[],[],[],[]
for i in range(1,len(t)-1):
	if t[i].day != t[i-1].day:
		k = k+1
		print(k)
	#tt[k] = tt[k] + 1
	distance1 = np.sqrt((ln[i]-ln[i-1])**2*np.cos(np.deg2rad((lt[i]+lt[i-1])/2))*40000/360 + (lt[i]-lt[i-1])**2*111.3)
	if distance1<15:
		#distance[k] = distance[k] + distance1; m[k] = m[k]+1
		marker[i] = 1
	if marker[i] != marker[i-1] :
		lt2.append(lt[i-1])
		ln2.append(ln[i-1])
		p2.append(p[i-1])
		temp2.append(temp[i-1])
		s2.append(s[i-1])
		m2.append(marker[i-1])
	#if marker[i] == 0 and marker[i-1] ==1 :
	#	lt2.append(lt[i-1])
	#	ln2.append(ln[i-1])
	#	p2.append(p[i-1])
	#	temp2.append(temp[i-1])
	#	s2.append(s[i-1])
	#	m2.append(marker[i-1])
	#elif marker[i] == 0 and marker[i-1] == 0:
	#	lt2.append(lt[i-1])
	#	ln2.append(ln[i-1])
	#	p2.append(p[i-1])
	#	temp2.append(temp[i-1])
	#	s2.append(s[i-1])
	#	m2.append(marker[i-1])

lt,ln,p,temp,s,marker = lt2,ln2,p2,temp2,s2,m2


def kn(X_train,y_train,X_test,nn=5):
	from sklearn.neighbors import KNeighborsClassifier
	knn = KNeighborsClassifier(algorithm='auto', leaf_size=30, n_neighbors=nn, p=2,weights='uniform')
	knn.fit(X_train,y_train) 
	y_predict = knn.predict(X_test)
	return y_predict
def mp(X_train,y_train,X_test,hid=(100,100)):
	from sklearn.neural_network import MLPClassifier
	knn = MLPClassifier(solver='adam', hidden_layer_sizes=hid)
	knn.fit(X_train,y_train) 
	y_predict = knn.predict(X_test)
	return y_predict

from sklearn.preprocessing import normalize
X_train_4 = lt / np.linalg.norm(lt)
X_train_5 = ln / np.linalg.norm(ln)
X_train_1 = p / np.linalg.norm(p)
X_train_2 = temp / np.linalg.norm(temp)
X_train_3 = s / np.linalg.norm(s)


X_full = []
for i in range(len(X_train_1)):
	#X_full.append(list([X_train_4[i],X_train_5[i],X_train_1[i],X_train_2[i],X_train_3[i],marker[i]]))
	X_full.append(list([X_train_1[i],X_train_2[i],X_train_3[i],marker[i]]))
np.random.shuffle(X_full)
X_full = np.array(X_full).T
lens = len(marker)
X_train = X_full[:-1,0:int(lens/4)].T
X_test = X_full[:-1,int(lens/4):].T
y_train = X_full[-1,0:int(lens/4)]
y_test = X_full[-1,int(lens/4):]


y_predict = mp(X_train,y_train,X_test) #kn

print('accuracy',np.round(100*np.sum(np.abs(y_predict-y_test))/len(y_predict),2))
