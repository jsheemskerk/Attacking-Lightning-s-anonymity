import json
from networkx.algorithms.distance_measures import center
import numpy as np
import nested_dict as nd
import matplotlib.pyplot as plt



def perc(num):
    return round(num * 100, 2)



# pick file used in paper
# file = "results/barabasi-dovetail-1000-500-5.json"

file = "results.json"

results = []
with open(file,'r') as json_file:
    results_json = json.load(json_file)
results.append(results_json)



tx_success = 0
tx_total = 0
tx_attacked = 0
tx_path_lengths = 0
tx_fee = 0
tx_hops = 0

path1_attack = 0
path2_attack = 0
center_attack = 0

path1_sender_size = 0
path1_sender_of_dest_size = 0
path1_rec_size = 0
path1_pair_found = 0
path2_sender_size = 0
path2_sender_of_dest_size = 0
path2_rec_size = 0
path2_pair_found = 0
center_sender_size = 0
center_sender_of_dest_size = 0
center_rec_size = 0
center_pair_found = 0
position_false_guess = 0

pair_found = 0
pair_not_found = 0
pairs_total = 0

path1_pair_total = 0
path2_pair_total = 0
center_pair_total = 0


path1_sing_dest = 0
path1_sing_dest_fp = 0
path2_sing_dest = 0
path2_sing_dest_fp = 0
center_sing_dest = 0
center_sing_dest_fp = 0

path1_sing_source = 0
path1_sing_source_fp = 0
path2_sing_source = 0
path2_sing_source_fp = 0
center_sing_source = 0
center_sing_source_fp = 0

path1_sing_either = 0
path1_sing_either_fp = 0
path2_sing_either = 0
path2_sing_either_fp = 0
center_sing_either = 0
center_sing_either_fp = 0


connectivities = np.zeros(0)
pairssizes = np.zeros(0)
conhops = np.zeros(0)

for i in results:
    for j in i:
        for k in j:
            tx_total += 1
            tx_path_lengths += len(k["path"])
            tx_fee += k["Cost"] - k["amount"]
            tx_hops += (len(k["path"]) - 1)
            if k["success"]:
                tx_success += 1

            if k["attacked"]:
                tx_attacked += 1

            for (a,v) in k["attack_position"].items():
                # print("connectivity:", k["dove_connectivity"])
                if (k["dove_connectivity"] >= len(connectivities)):
                    connectivities.resize(k["dove_connectivity"] + 1, refcheck= False)
                    pairssizes.resize(k["dove_connectivity"] + 1, refcheck = False)
                    conhops.resize(k["dove_connectivity"] + 1, refcheck = False)
                connectivities[k["dove_connectivity"]] += 1
                attacker = int(a)
                dove = k['dovetail']
                sender = k['sender']
                recipient = k['recipient']

                guess_position = k['attack_position'][a]
                index_dove = k["path"].index(dove)
                index_attacker = k["path"].index(attacker)
                if (dove == attacker):
                    real_position = 1
                elif (index_attacker < index_dove):
                    real_position = 0
                else:
                    real_position = 2
                

                if (guess_position != real_position):
                    position_false_guess += 1
                else:

                    anonset = k["anon_sets"][a]
                    recset = list(anonset.keys())
                    senderset = []
                    pairs = 0
                    for senders in anonset.values():
                        for s in senders:
                            pairs += 1
                            pairs_total += 1
                            if s not in senderset:
                                senderset.append(s)
                    
                    pairssizes[k["dove_connectivity"]] += pairs
                    conhops[k["dove_connectivity"]] += (len(k["path"]) - 1)

                    source = sender if real_position != 2 else dove
                    dest = recipient if real_position != 0 else dove

                    if (real_position == 0):
                        path1_pair_total += pairs
                        path1_sender_size += len(senderset)
                        if (str(dest) in recset):
                            path1_sender_of_dest_size += len(anonset[str(dest)])
                            if (source in anonset[str(dest)]):
                                path1_pair_found += 1
                        path1_rec_size += len(recset)
                        path1_attack += 1


                        Either = False
                        if (len(recset) == 1):
                            if (int(recset[0]) == dest):
                                Either = True
                                path1_sing_dest += 1
                            else:
                                path1_sing_dest_fp += 1
                        if (len(senderset) == 1):
                            if (senderset[0] == source):
                                Either = True
                                path1_sing_source += 1
                            else:
                                path1_sing_source_fp += 1
                        if Either:
                            path1_sing_either += 1
                            


                    elif (real_position == 1):
                        center_pair_total += pairs
                        center_sender_size += len(senderset)
                        if (str(dest) in recset):
                            center_sender_of_dest_size += len(anonset[str(dest)])
                            if (source in anonset[str(dest)]):
                                center_pair_found += 1
                        center_rec_size += len(recset)
                        center_attack += 1

                        Either = False
                        if (len(recset) == 1):
                            if (int(recset[0]) == dest):
                                Either = True
                                center_sing_dest += 1
                            else:
                                center_sing_dest_fp += 1
                        if (len(senderset) == 1):
                            if (senderset[0] == source):
                                Either = True
                                center_sing_source += 1
                            else:
                                center_sing_source_fp += 1
                        if Either:
                            center_sing_either += 1
                    else:
                        path2_pair_total += pairs
                        path2_sender_size += len(senderset)
                        if (str(dest) in recset):
                            path2_sender_of_dest_size += len(anonset[str(dest)])
                            if (source in anonset[str(dest)]):
                                path2_pair_found += 1
                        path2_rec_size += len(recset)
                        path2_attack += 1

                        Either = False
                        if (len(recset) == 1):
                            if (int(recset[0]) == dest):
                                Either = True
                                path2_sing_dest += 1
                            else:
                                path2_sing_dest_fp += 1
                        if (len(senderset) == 1):
                            if (senderset[0] == source):
                                Either = True
                                path2_sing_source += 1
                            else:
                                path2_sing_source_fp += 1
                        if Either:
                            path2_sing_either += 1
                    
                    if (str(dest) in recset and source in anonset[str(dest)]):
                            pair_found += 1
                    else:
                        pair_not_found += 1
                        path = k["path"]

                        # check for faulty transactions
                        # iss = path.index(source)
                        # ia = path.index(attacker)
                        # id = path.index(dest)

                        # if (ia - iss < 4 and id - ia < 4):
                        #     print(k)
                        #     print(f"{real_position} {path.index(source)} {path.index(attacker)} {path.index(dest)}")
                    
print(f"Total number of transactions: {tx_total}")
print("Pairs found:",pair_found)
print("Pairs missed:",pair_not_found)


correct_attacks = path1_attack + path2_attack + center_attack
print(f"Total number of (correct) attacks: {correct_attacks}")
total_pairs = path1_pair_total + path2_pair_total + center_pair_total
# print(f"Successfull position guesses: {correct_attacks}, failed: {position_false_guess}")
# print(f"Percentage correct: {perc(correct_attacks/(correct_attacks + position_false_guess))}%")
print(f"Path 1 attacks: {path1_attack}")
if path1_attack == 0: path1_attack = 1
print(f"Path 1 average sender size: {path1_sender_size/path1_attack}")
print(f"Path 1 average sender size for correct dest: {path1_sender_of_dest_size/path1_attack}")
print(f"Path 1 average rec (dovetail) size: {path1_rec_size/path1_attack}")
avg_pair_path1 = path1_pair_total/path1_attack
print(f"Path 1 average number of pairs: {avg_pair_path1}")
print(f"Path 1 correct pair present: {perc(path1_pair_found / path1_attack)}%")
print(f"Path 1 singular dest: {perc(path1_sing_dest / path1_attack)}%")
print(f"Path 1 singular dest fp: {perc(path1_sing_dest_fp / path1_attack)}%")
print(f"Path 1 singular source: {perc(path1_sing_source / path1_attack)}%")
print(f"Path 1 singular source fp: {perc(path1_sing_source_fp / path1_attack)}%")
print(f"Path 1 either singular: {perc(path1_sing_either / path1_attack)}%")
print(f"Path 2 attacks: {path2_attack}")
if path2_attack == 0: path2_attack = 1
print(f"Path 2 average sender (dovetail) size: {path2_sender_size/path2_attack}")
print(f"Path 2 average sender (dovetail) size for correct dest: {path2_sender_of_dest_size/path2_attack}")
print(f"Path 2 average rec size: {path2_rec_size/path2_attack}")
avg_pair_path2 = path2_pair_total/path2_attack
print(f"Path 2 average number of pairs: {avg_pair_path2}")
print(f"Path 2 correct pair present: {perc(path2_pair_found / path2_attack)}%")
print(f"Path 2 singular dest: {perc(path2_sing_dest / path2_attack)}%")
print(f"Path 2 singular dest fp: {perc(path2_sing_dest_fp / path2_attack)}%")
print(f"Path 2 singular source: {perc(path2_sing_source / path2_attack)}%")
print(f"Path 2 singular source fp: {perc(path2_sing_source_fp / path2_attack)}%")
print(f"Path 2 either singular: {perc(path2_sing_either / path2_attack)}%")
print(f"Center attacks: {center_attack}")
if center_attack == 0: center_attack = 1
print(f"Center average sender size: {center_sender_size/center_attack}")
print(f"Center average sender size for correct dest: {center_sender_of_dest_size/center_attack}")
print(f"Center average rec size: {center_rec_size/center_attack}")
avg_pair_center = center_pair_total/center_attack
print(f"Center average number of pairs: {avg_pair_center}")
print(f"Center correct pair present: {perc(center_pair_found / center_attack)}%")
print(f"Center singular dest: {perc(center_sing_dest / center_attack)}%")
print(f"Center singular dest fp: {perc(center_sing_dest_fp / center_attack)}%")
print(f"Center singular source: {perc(center_sing_source / center_attack)}%")
print(f"Center singular source fp: {perc(center_sing_source_fp / center_attack)}%")
print(f"Center either singular: {perc(center_sing_either / center_attack)}%")

print(f"Total average number of pairs {pairs_total/correct_attacks}")
print(f"Total average number of pairs {(avg_pair_path1 * path1_attack + avg_pair_path2 * path2_attack+ avg_pair_center * center_attack) / correct_attacks }")


print(f"Avg hops: {tx_hops / tx_total}")
print(f"Avg fee: {tx_fee / tx_total}")
print(f"Transaction success rate: {perc(tx_success / tx_total)}%")
print(f"Transactions attacked: {perc(tx_attacked / tx_total)}%")



print(connectivities)
avgpairs = pairssizes / connectivities
avghops = conhops / connectivities
avgpairs = np.nan_to_num(avgpairs)
avghops = np.nan_to_num(avghops)
print(connectivities)
print(avgpairs)
print(conhops)

con = np.arange(len(connectivities))

plt.figure()
plt.xlabel('Connectivity of Dovetail node', fontsize=12)
plt.ylabel('$AVG_{pair}$', fontsize=12)
plt.hist(con, weights=avgpairs, bins=len(avgpairs)//2)
plt.ticklabel_format(axis='both',style='sci')
plt.figure()
plt.xlabel('Connectivity of Dovetail node', fontsize=12)
plt.ylabel('$N_{att}$', fontsize=12)
plt.hist(con, weights=connectivities, bins=len(connectivities))
plt.figure()
plt.xlabel('Connectivity of Dovetail node', fontsize=12)
plt.ylabel('$AVG_{hops}$', fontsize=12)
plt.hist(con, weights=avghops, bins=len(avghops))
plt.show()
