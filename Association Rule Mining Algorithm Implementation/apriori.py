from itertools import chain, combinations

#load data from the file
def load_database(filename):
    file = open(filename, 'rU')
    next(file)
    for line in file:
        row = map(str.strip, line.split())
        yield row

#build first itemset
def build_first_itemset(database, header):
    all_transactions = list()
    itemset = set()
    for row in database:
        row = list(header[i]+ " = " + row[i] for i in range(len(row)))
        all_transactions.append(frozenset(row))
        for i in range(len(row)):
            if row[i]:
                itemset.add(frozenset([row[i]]))
    return itemset, all_transactions

#applying the min_support
def apply_min_support(all_transactions, itemset, min_support=0.0):
    my_dict = {}
    len_all_transactions = len(all_transactions)
    my_list = [(item, float(sum(1 for row in all_transactions if item.issubset(row))) / (len_all_transactions - 1))for item in itemset]
    for item, support in my_list:
        if support >= min_support:
            my_dict[item] = support
    return my_dict


#generate k candidate itemset
def generate_candidate_itemset(itemset, k):
    my_list = []
    for item in itemset:
        for item_a in itemset:
            if len(item.union(item_a)) == k:
                my_list.append(item.union(item_a))
    return set(my_list)

#generate candidate subsets
def candidate_subsets(itemset):
    my_list = []
    for i,j in enumerate(itemset):
        my_list.append(combinations(itemset, i+1))
    return chain(*my_list)

#generate frequent itemset
def generate_frequent_itemset(all_transactions, candidate_itemset, min_support):
    frequent_itemset = dict()
    k = 1
    while True:
        if k > 1:
            candidate_itemset = generate_candidate_itemset(list_itemset, k)
        list_itemset = apply_min_support(all_transactions, candidate_itemset, min_support)
        if not list_itemset:
            break
        frequent_itemset.update(list_itemset)
        k = k+1

    return frequent_itemset

#create rules and write rules to file
def create_and_write_rules(database, min_support, min_confidence, header):
    itemset, all_transactions = build_first_itemset(database, header)
    len_all_transactions = len(all_transactions)
    frequent_itemset = generate_frequent_itemset(all_transactions, itemset, min_support)
    rules = list()
    for item, support in frequent_itemset.items():
        if len(item) > 1:
            for A in candidate_subsets(item):
                B = item.difference(A)
                if B:
                    A = frozenset(A)
                    AB = A | B
                    confidence = float(frequent_itemset[AB]) / frequent_itemset[A]
                    if confidence >= min_confidence:
                        rules.append((A, B, support, confidence))
    total_rules = len(rules)
    file = open("Rules", "w+")
    file.write("Summary:" + "\n")
    file.write("Total rows in the original set: " + str(len_all_transactions - 1) + "\n")
    file.write("Total rules discovered: " + str(total_rules) + "\n")
    file.write("The selected measures: Support=" + str(min_support) +", Confidence=" + str(min_confidence) + "\n")
    file.write("------------------------------------------------" + "\n")
    file.write("Discovered Rules:" + "\n" + "\n" +"\n")
    a = 0
    for A,B,support,confidence in sorted(rules,key=lambda (A,B,support,confidence):support):
        a = a + 1
        file.write("Rule#" + str(a) + ": ")
        file.write("{ ")
        file.write(', '.join(str(x) for x in A))
        file.write(" }" + " -----> " + "{ " )
        file.write(', '.join(str(x) for x in B))
        file.write(" }" + "\n")
        file.write("(Support = " + str(round(support, 2)) + ", Confidence = " + str(round(confidence, 2)) + ")" + "\n")
    file.close()
    print "The results are saved in the file Rules."
    print "********  Algorithm Finished ********"

#Run Apriori algorithm
def run_apriori():
    while True:
        try:
            filename = raw_input('What is the name of the file containing your data (data1, data2, data3)?')
            database = load_database(filename)
            header = open(filename, 'r').readline().split()
            break
        except IOError:
            print "No such file, please select again (data1, data2, data3)."
    while True:
        min_support = input('Please select the minimum support rate(0.00-1.00):')
        if min_support <= 1:
            break
        else:
            print "The selected rate is out of range, please select again."
    while True:
        min_confidence = input('Please select the mimimum confidence rate(0.00-1.00):')
        if min_confidence <= 1:
            break
        else:
            print "The selected rate is out of range, please select again."
    create_and_write_rules(database, min_support, min_confidence, header)


def main():
    run_apriori()


if __name__ == '__main__':
    main()