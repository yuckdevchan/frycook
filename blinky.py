import json

import linky

def get_seen_domains(web):
    l = []
    for domain in web.keys():
        try:
            l.append(linky.link_to_domain(domain))
        except IndexError: pass
        for domain_pair in web[domain]:
            try:
                l.append(linky.link_to_domain(domain_pair))
            except IndexError: pass
    l = list(set(l))
    return l

if __name__ == "__main__":
    with open("web.json", "r") as f:
        web = json.load(f)
    print(len(get_seen_domains(web)))
