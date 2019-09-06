"""
Created by Evgeny Ivanov for Emodnet Hackatlon 2019
"""

time,lt,ln,p,t,s = [],[],[],[],[],[]
for line in open('Phyto2.txt','r').readlines()[:]:
	a=line.split('\t')
	time.append(a[0])
	lt.append(a[1])
	ln.append(a[2])
	p.append(a[3].split('\n')[0])

for line in open('Temp2.txt','r').readlines()[:]:
	a=line.split('\t')
	t.append(a[3].split('\n')[0])

for line in open('Salt2.txt','r').readlines()[:]:
	a=line.split('\t')
	s.append(a[3].split('\n')[0])

f= open("Altogether_Phyto_Temp_Salt.txt","w")
for i in range(len(t)):
	f.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (time[i],lt[i],ln[i],p[i],t[i],s[i]))
f.close()
