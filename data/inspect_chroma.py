import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
col = client.get_collection("learning_resources")

# Get all items
all_items = col.get(include=["documents", "metadatas"])

# Simple rule: documentation = beginner, article = intermediate, project = advanced
type_to_level = {
    "documentation": "beginner",
    "article": "intermediate", 
    "project": "advanced"
}

# Update metadata with level
updated_metadatas = []
for meta in all_items["metadatas"]:
    resource_type = meta.get("type", "article")
    meta["level"] = type_to_level.get(resource_type, "intermediate")
    updated_metadatas.append(meta)

# Update in ChromaDB
col.update(
    ids=all_items["ids"],
    metadatas=updated_metadatas
)

print("Done! All resources now have a level field.")

# Verify
peek = col.peek(limit=3)
print(peek["metadatas"])