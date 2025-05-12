import pickle

with open("web.pickle", "rb") as f:
    web = pickle.load(f)
    seen_domains = pickle.load(f)
    print("Web data loaded successfully.")
    print(f"Seen domains: {len(seen_domains)}")
    print(f"Web data: {len(web)} nodes")
    with open("nodes.txt", "w") as f:
        for node in web:
            f.write(node + "\n")

    with open("seen_domains.txt", "w") as f:
        for domain in seen_domains:
            f.write(domain + "\n")
