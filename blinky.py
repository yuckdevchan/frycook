import pickle

def present_data():
    with open("web.pickle", "rb") as f:
        loaded_file = pickle.load(f)
        web, seen_domains = loaded_file[0], loaded_file[1]
        print("Web data loaded successfully.")
        print(f"Seen domains: {len(seen_domains)}")
        print(f"Web data: {len(web)} nodes")
        with open("nodes.txt", "w") as f:
            for node in web:
                f.write(node + "\n")

        with open("seen_domains.txt", "w") as f:
            for domain in seen_domains:
                f.write(domain + "\n")

if __name__ == "__main__":
    present_data()
