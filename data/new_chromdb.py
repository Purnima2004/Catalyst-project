import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_collection("gold_answers")

all_items = col.get(include=["metadatas", "documents"])

skills_covered = {}
for meta, doc in zip(all_items["metadatas"], all_items["documents"]):
    skill = meta.get("skill", "unknown")
    if skill not in skills_covered:
        skills_covered[skill] = []
    skills_covered[skill].append(doc[:80])  # first 80 chars

for skill, answers in skills_covered.items():
    print(f"\n{skill} ({len(answers)} answers):")
    for a in answers:
        print(f"  - {a}")