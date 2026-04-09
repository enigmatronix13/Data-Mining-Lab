from itertools import combinations

# ----------- LOAD DATA -----------
def load_data():
    # Example transactional dataset
    return [
        {'milk', 'bread', 'butter'},
        {'bread', 'butter'},
        {'milk', 'bread'},
        {'milk', 'butter'},
        {'bread'},
        {'milk', 'bread', 'butter'}
    ]

# ----------- SUPPORT COUNT -----------
def get_support(itemset, transactions):
    count = 0
    for t in transactions:
        if itemset.issubset(t):
            count += 1
    return count / len(transactions)

# ----------- GENERATE CANDIDATES -----------
def generate_candidates(prev_L, k):
    candidates = set()
    prev_L = list(prev_L)

    for i in range(len(prev_L)):
        for j in range(i+1, len(prev_L)):
            union = prev_L[i] | prev_L[j]
            if len(union) == k:
                candidates.add(frozenset(union))
    return candidates

# ----------- APRIORI -----------
def apriori(transactions, min_support):
    # Step 1: C1
    items = set()
    for t in transactions:
        for item in t:
            items.add(frozenset([item]))

    L = []
    L1 = set()

    for item in items:
        if get_support(item, transactions) >= min_support:
            L1.add(item)

    L.append(L1)

    k = 2
    while True:
        Ck = generate_candidates(L[-1], k)
        Lk = set()

        for c in Ck:
            if get_support(c, transactions) >= min_support:
                Lk.add(c)

        if not Lk:
            break

        L.append(Lk)
        k += 1

    return L

# ----------- ASSOCIATION RULES -----------
def generate_rules(L, transactions, min_conf):
    rules = []

    for level in L[1:]:
        for itemset in level:
            for i in range(1, len(itemset)):
                for subset in combinations(itemset, i):
                    subset = frozenset(subset)
                    remain = itemset - subset

                    conf = get_support(itemset, transactions) / get_support(subset, transactions)

                    if conf >= min_conf:
                        rules.append((subset, remain, conf))

    return rules

# ----------- MAIN -----------
transactions = load_data()
min_support = 0.3
min_conf = 0.6

L = apriori(transactions, min_support)

print("Frequent Itemsets:")
for level in L:
    print(level)

rules = generate_rules(L, transactions, min_conf)

print("\nAssociation Rules:")
for r in rules:
    print(f"{set(r[0])} -> {set(r[1])}, confidence={r[2]:.2f}")