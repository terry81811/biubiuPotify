# aggregate new biz for first 3000 users

subsets = [0, 1, 2, 3, 4, 5]
for i in range(10, 30):
	subsets.append(i)

users = {}
biz = set()
biz2 = []

for subset in subsets:

	f = open('outputData/newBiz_' + str(subset*100) + '.tsv', 'r')
	businessParts = [line.rstrip('\n\r').split("\t") for line in f]
	businesses = [businessPart[2] for businessPart in businessParts]

	for parts in businessParts:
		if parts[1] in users:
			users[parts[1]] += 1
		else:
			users[parts[1]] = 1


	print ">>> read " + str(len(businessParts)) + " from newBiz_" + str(subset*100) + ".tsv"

	biz2.extend(businesses)
	biz = biz | set(businesses)




print len(users)
print len(biz)
print len(biz2)


# print subsets

# f = open('outputData/user_id_mapping_all.tsv', 'r')
# users = [line.rstrip('\n\r').split("\t")[1] for line in f]

# print len(set(users))

cnt = 1
f_newBiz = open('outputData/newBiz_all_3000.tsv', 'w')
for biz in biz:
	f_newBiz.write(str(cnt) + "\t" +  biz + "\n")
	cnt += 1
