import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = list()   #making a list of all the from_ids in the links table
for row in cur:
    from_ids.append(row[0])

to_ids = list()
links = list()
cur.execute('SELECT DISTINCT from_id,to_id FROM Links')   #filtering the links to make sure the crawler doesn't deviate too much
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if from_id == to_id:
        continue
    if from_id not in from_ids:
        continue
    if to_id not in from_ids:
        continue  # we only want the pages that point to pages that have already been retrieved
    links.append(row)
    if to_id not in to_ids:
        to_ids.append(to_id) #list to to_ids after filtering

prev_ranks = dict()
for node in from_ids:
    cur.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (node,))
    row=cur.fetchone()
    prev_ranks[node]= row[0]        #making a dictionary where we take the ranks of all the from ids and connect them to their Links

sval=input('How many iterations:')
many=1
if (len(sval)>1):
    many=int(sval)

#sanity check to make sure program isnt bad
if len(prev_ranks)<1:
    print("Nothing in page rank, problem with database")
    quit()

for i in range(many):
    new_ranks=dict()
    total=0.0
    for (node,old_rank) in list(prev_ranks.items()):
        print(node, old_rank,total)
        total=total + old_rank
        new_ranks[node]=0.0

    for (node,old_rank) in list(prev_ranks.items()):
        give_ids = list()
        for(from_id,to_id) in links:
            print(from_id, to_id)
            if from_id !=node:
                continue
            if to_id not in to_ids:
                continue
            give_ids.append(to_id)  #this is a list of outbound links that a node contains
        if len(give_ids)<1:
            continue
        amount= old_rank/len(give_ids)

        for id in give_ids:
            new_ranks[id]=new_ranks[id]+amount

    new_total=0
    for (node, new_rank) in list(new_ranks.items()):
        new_total=new_total + new_rank
    evap = (total - new_total) / len(new_ranks)
    print(evap,new_total)

    for node in new_ranks:
        new_ranks[node]=new_ranks[node]+evap

    new_total=0
    for (node, new_rank) in list(new_ranks.items()):
        new_total=new_total + new_rank
    print(evap, new_total)

    total_diff=0
    for(node,old_rank) in list(prev_ranks.items()):
        new_rank = new_ranks[node]
        diff = abs(old_rank - new_rank)
        total_diff+=diff

    average_diff=total_diff / len(prev_ranks)
    print('Average Difference:',average_diff)

    prev_ranks=new_ranks

print(list(new_ranks.items())[:5])
cur.execute('UPDATE Pages SET old_rank=new_rank''')
for (id,new_rank) in list(new_ranks.items()):
    cur.execute('''UPDATE Pages SET new_rank=? WHERE id=?''',(new_rank, id))

conn.commit()
cur.close()
