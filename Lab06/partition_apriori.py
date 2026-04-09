# -------- PARTITION APRIORI + ASSOCIATION RULES --------

from itertools import combinations

# -------- READ DATA FROM FILE --------
def load_transactions(filename):
    transactions = []
    with open(filename, 'r') as f:
        for line in f:
            items = set(line.strip().split())
            if items:
                transactions.append(items)
    return transactions

# -------- SUPPORT FUNCTIONS --------
def support_count(itemset, transactions):
    count = 0
    for t in transactions:
        if itemset.issubset(t):
            count += 1
    return count

def support(itemset, transactions):
    return support_count(itemset, transactions) / len(transactions)

# -------- GENERATE CANDIDATES --------
def generate_candidates(prev_L, k):
    candidates = set()
    prev_L = list(prev_L)

    for i in range(len(prev_L)):
        for j in range(i + 1, len(prev_L)):
            union = prev_L[i] | prev_L[j]
            if len(union) == k:
                candidates.add(frozenset(union))

    return candidates

# -------- LOCAL APRIORI --------
def local_apriori(transactions, min_count):
    items = set()

    for t in transactions:
        for item in t:
            items.add(frozenset([item]))

    L = []
    L1 = set()

    for item in items:
        if support_count(item, transactions) >= min_count:
            L1.add(item)

    L.append(L1)

    k = 2
    while True:
        Ck = generate_candidates(L[-1], k)
        Lk = set()

        for c in Ck:
            if support_count(c, transactions) >= min_count:
                Lk.add(c)

        if not Lk:
            break

        L.append(Lk)
        k += 1

    result = set()
    for level in L:
        result |= level

    return result

# -------- PARTITION APRIORI --------
def partition_apriori(transactions, min_support):
    n = len(transactions)
    partition_size = n // 2  # 2 partitions

    partitions = [
        transactions[:partition_size],
        transactions[partition_size:]
    ]

    global_candidates = set()

    # Step 1: Local frequent itemsets
    for part in partitions:
        min_count = min_support * len(part)
        local_freq = local_apriori(part, min_count)
        global_candidates |= local_freq

    # Step 2: Global validation
    final_freq = set()
    min_global = min_support * n

    for c in global_candidates:
        if support_count(c, transactions) >= min_global:
            final_freq.add(c)

    return final_freq

# -------- ASSOCIATION RULES --------
def generate_rules(freq_itemsets, transactions, min_conf):
    rules = []

    for itemset in freq_itemsets:
        if len(itemset) < 2:
            continue

        for i in range(1, len(itemset)):
            for subset in combinations(itemset, i):
                subset = frozenset(subset)
                remain = itemset - subset

                conf = support(itemset, transactions) / support(subset, transactions)

                if conf >= min_conf:
                    rules.append((subset, remain, conf))

    return rules

# -------- MAIN --------
filename = "transactions.txt"
min_support = 0.3
min_conf = 0.6

transactions = load_transactions(filename)

# Frequent itemsets
freq_itemsets = partition_apriori(transactions, min_support)

print("Frequent Itemsets:")
for item in freq_itemsets:
    print(set(item))

# Association rules
rules = generate_rules(freq_itemsets, transactions, min_conf)

print("\nAssociation Rules:")
for r in rules:
    print(f"{set(r[0])} -> {set(r[1])} (confidence = {r[2]:.2f})")