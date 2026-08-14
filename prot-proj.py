# Amino acids that prefer the protein interior
hydrophobic = "AILV"

 #Amino acids that often like the protein surface 
polar = "EKRS"

import random

# print (random.choice(hydrophobic)) #randomly choose one aminoacid

# sequence = ""

# for i in range(5): # repeat 5 times
#     sequence = sequence + random.choice(hydrophobic) # add one random amino acid
# #print(sequence)

seq = ""
for i in range (6):
    if i%2 == 0: # check for even positions
        seq = seq + "L"
    else: 
        seq = seq + "E"

#print(seq)

a_a = ["A", "L", "I", "V"]

# print(a_a[2]) 
proteins = []
# proteins.append(seq)

for i in range (5): 
    Nsec = ""

    for j in range (10):
        Nsec = Nsec + random.choice(hydrophobic) # add one random aa 
    proteins.append(Nsec)

print(proteins)

def generate_proteins(length): # the lenght in the bracket is manipulatable as it give us a desired length and can be changed.  
    #If it was empty then we can have a fixed length in the range() function
    sequence = ""

    for i in range(length):
        sequence= sequence + random.choice(hydrophobic) 
    return sequence # Give the completed sequence back

protein1= generate_proteins(5) # this will generate a protein 5aa in length
protein2= generate_proteins(20)

print(protein1)
print(protein2)

prot = {"sqn":seq, "lenght": 6 } # a dictionary Key:Value
prot["hydrophobicity"]=0.5 #adding a new item to the dictionary
prot["molecular_weight"]=742.3
print(prot)

print(prot["lenght"])

