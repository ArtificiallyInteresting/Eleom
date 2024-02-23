
def get_facts():
    f = open("Eleom/data/facts.txt", "r")
    facts = []
    for line in f.readlines():
        facts.append(line.split("#")[0])
    f.close()
    return facts