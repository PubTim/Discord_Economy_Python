
import os
import hashlib
import json

print(os.getcwd())
sha256_hash = hashlib.sha256()

with open('nfts.json','r') as file:
    nfts = json.load(file)


for filename in os.listdir("NFTS"):
    with open("NFTS/"+filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        hash = hashlib.sha256(bytes).hexdigest()
        if hash not in nfts:
            print("Hash not found")
            nfts[filename] = {}
            nfts[filename]['hash'] = str(hash)
            nfts[filename]['owner'] = "" 
            nfts[filename]['ownerid'] = 0 #id is number
            nfts[filename]['value'] = 0
            nfts[filename]['Prevowners'] = []
            nfts[filename]['bidstatus'] = False

with open('nfts.json','w') as file:
    json.dump(nfts,file)
            