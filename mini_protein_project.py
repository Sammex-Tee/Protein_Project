import random

hydrophobic = "AILV"
hydrophilic = "EKRS"
helix_propensity= {"A": 1.45, "L": 1.34, "E": 1.53, "K": 1.23, 
                   "R": 0.79, "S": 0.79,"I": 1.00, "V": 0.79}


patterns = {"alternating_HP": "HP", "two_hydrophobic_two_hydrophilic": "HHPP", 
           "one_hydrophobic_two_hydrophilic": "HPP", "two_hydrophobic_one_hydrophilic": "HHP"}

# def generate_protein(length):

#     aa = hydrophobic + hydrophilic

#     sequence= ""
    
#     for i in range(length):#amino acid that would be added to the chain
#         if i%2 == 0:
#             sequence+= random.choice(hydrophobic)
#         else:
#             sequence += random.choice(hydrophilic)

#     return sequence

def generate_patterned_protein(length, pattern):
    sequence = ""
    
    for i in range(length):
        symbol = pattern[i % len(pattern)]

        if symbol == "H":
            sequence += random.choice(hydrophobic)
        else: 
            sequence += random.choice(hydrophilic)
    return sequence


def amino_acid_composition(sequence):
    #Counts the frequency of each individual amino acid."""
    counts = {}
    for amino_acid in sequence:
        if amino_acid not in counts:
            counts[amino_acid] = 1
        else: 
            counts[amino_acid] += 1
    return counts

# a shorter method of doing this is 
# from collections import Counter

# # This single line replaces your entire 7-line if/else loop:
# counts = Counter(sequence)

def calculate_helix_score(sequence):
    total_score = 0
    
    for amino_acid in sequence:
        total_score+= helix_propensity.get(amino_acid, 0)
    average_score = total_score/len(sequence)

    return average_score 

def analyze_protein(sequence):
    hydrophobic = "AILV"
    hydrophobic_count = 0


    # for amino_acid in sequence:
    #     # if amino_acid in hydrophobic: #loops through every aa 
    #     #     hydrophobic_count+=1
    # # Instead of looping manually:
    hydrophobic_count = sum(sequence.count(amino_acid) for amino_acid in hydrophobic) 
    #another method of doing the count

    composition = amino_acid_composition(sequence)
    helix_score = calculate_helix_score(sequence)
    
    results = {"sequence": sequence, "length": len(sequence), "hydrophobic_count": hydrophobic_count,
               "hydrophobic_fraction": hydrophobic_count/len(sequence),"composition": composition, "helix_score": helix_score }
    
    return (results)

def generate_protein_dataset(no_of_proteins, length):

    dataset = []

    for pattern_name, pattern in patterns.items():
        for x in range(no_of_proteins):

            protein = generate_patterned_protein(length, pattern)
            analysis= analyze_protein(protein)
            analysis["pattern"]= pattern_name
            dataset.append(analysis)

    return dataset


def select_candidates(dataset, mini_hydro, max_hydro): #select proteins whose hydrophobic fraction is within a desired range

    candidates= []
    
    for protein in dataset:
        hydro_fraction = protein["hydrophobic_fraction"]

        if mini_hydro<= hydro_fraction<= max_hydro: # check whether the desired protein is in the desired range
            candidates.append(protein)

        
    return candidates

def score_protein(protein, target_hydro): # gives the protein a score based on how close it is to the target score

    hydro_fraction = protein["hydrophobic_fraction"] #get the proteins hydrophobic fraction
    helix_score = protein["helix_score"]

    distance = abs(hydro_fraction-target_hydro) #calculate distance from a target hydrophobic fraction

    score = 1- distance # converts distance into a score, a smaller distance means a better score i.e. closer to 1
    final_score= score + helix_score

    return final_score


def rank_candidates(candidates, target_hydro): #rank candidates by how close they are to target value

    ranked= sorted(candidates, key = lambda protein: score_protein(protein, target_hydro), reverse = True)

    return ranked

def summarize_by_pattern(dataset, target_hydro):
    summary = {}

    for protein in dataset:
        pattern = protein["pattern"]
        final_score = score_protein(protein, target_hydro)

        if pattern not in summary:
            summary[pattern] = {"count": 0, "total_score": 0, "best_score": final_score, 
                                "best_sequence": protein["sequence"]}
            
        summary[pattern]["count"] += 1
        summary[pattern]["total_score"] += final_score

        if final_score > summary[pattern]["best_score"]: 
            summary[pattern]["best_score"] = final_score
            summary[pattern]["best_sequence"] = protein["sequence"]

    for pattern in summary:
            summary[pattern]["average_score"] = summary[pattern]["total_score"]/summary[pattern]["count"]

    return summary
    
def save_summary_to_csv(summary, filename):
    file = open(filename, "w")

    file.write("pattern,Count,Average_Score,Best_Score,Best_sequence\n")

    for pattern, info in summary.items():
        row = (pattern + "," + str(info["count"])+ "," + str(info["average_score"]) + "," +  str(info["best_score"]) + "," + info["best_sequence"])

        file.write(row + "\n")
    
    file.close()

def save_to_csv(proteins, filename, target_hydro):

    aa = hydrophobic + hydrophilic #total amino acids used

    file = open(filename, "w") #open file for writing

    header = "Pattern, Sequence, Length, Hydrophobic_Fraction, Helix_Score, Final_Score" #add a column for each amino acid
    for amino_acid in aa:
        header+= "," + amino_acid # Example add A, then I then L etc


    file.write(header+ "\n")

    for protein in proteins:

        final_score = score_protein(protein,target_hydro)
        row = (protein['pattern']+"," + protein["sequence"]+ "," + str(protein["length"]) + "," + str(protein["hydrophobic_fraction"])
               + "," + str(protein["helix_score"])+ "," + str(final_score))
        
        composition = protein["composition"] # get the composition dictionary

        for amino_acid in aa:
        
            count= composition.get(amino_acid,0) # we are onlu using this because every colum of the csv has to contain a count value
            #for all aa present, else it will give an error 

            row+= "," + str(count)

        file.write(row + "\n")
 

    file.close()


target_hydro = 0.5
dataset = generate_protein_dataset(100,40) # generate and analyze 100 proteins each 40 amino acid long

#select candidates with desired hydrophobic fractions
# candidates= select_candidates(dataset, 0.4, 0.60)

#rank candidates by closeness to 0.50 hydrophobic fraction
ranked_candidates= rank_candidates(dataset, target_hydro)
pattern_summary = summarize_by_pattern (dataset, target_hydro)

print("pattern Summary")
print("-" * 40)


save_to_csv(ranked_candidates, "protein_results.csv", target_hydro)
save_summary_to_csv(pattern_summary, "pattern_summary.csv")

print("Results saved to protein_results.csv")

print("Pattern summary saved to protein_summary.csv")

#how many proteins were generated
# print("Total number of protein generated:", len(dataset))

# #print how many passed the filter
# print("Total selected proteins:", len(candidates))
# print ("Top ranked candidates:")
# print("-"*40)

# for protein in ranked_candidates[:5]:

