# Map for lists: map list: list map: listmap: lmap - do you see?
def lmap(f,l):
	l1 = []
	for i in l:
		l1.append(f(i))
	return l1

def foldl(f,acc,l):
	for i in l:
		acc = f(acc,i)
	return acc

# Filter
def fil(p,l):
	ret = []
	for i in l:
		if p(i): ret.append(i)
	return ret

# Find first e such that e is in l and p(e)
def find(p,l):
	for i in l:
		if p(i):
			return i
	return None
