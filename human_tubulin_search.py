import os

print("Current directory:", os.getcwd())
import requests
import pandas as pd

SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"

def search_tubulin(min_res, max_res):
    query = {
        "query": {"type": "group", "logical_operator": "and","nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_polymer_entity.pdbx_description",
                        "operator": "contains_words",
                        "value": "tubulin"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entity_source_organism.scientific_name",
                        "operator": "exact_match",
                        "value": "Homo sapiens"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entity_source_organism.taxonomy_lineage.name",
                        "operator": "exact_match",
                        "value": "Eukaryota"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "range",
                        "value": {
                            "from": min_res,
                            "to": max_res,
                            "include_lower": True,
                            "include_upper": True
                        }
                    }
                }
            ]
        },
        "return_type": "polymer_entity",
        "request_options": {
            "return_all_hits": True
        }
    }

    response = requests.post(SEARCH_URL, json=query)
    response.raise_for_status()
    return response.json().get("result_set", [])


rows = []

for min_res, max_res in [(1.0, 1.5), (1.5, 2.0)]:
    results = search_tubulin(min_res, max_res)

    for item in results:
        pdb_id, entity_id = item["identifier"].split("_")

        data_url = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}"
        data = requests.get(data_url).json()

        entry_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        entry = requests.get(entry_url).json()

        name = data["rcsb_polymer_entity"]["pdbx_description"]
        resolution = entry["rcsb_entry_info"]["resolution_combined"][0]

        rows.append({
            "PDB Code": pdb_id,
            "Tubulin Name": name,
            "Resolution (Å)": resolution,
            "Resolution Range": f"{min_res}-{max_res} Å",
            "Structure": f"https://www.rcsb.org/structure/{pdb_id}"
        })

df = pd.DataFrame(rows).drop_duplicates()
df.to_csv("/Users/sammextee/Desktop/human_tubulin_rcsb_table.csv", index=False)

print(df)