import chromadb
import os

# Define expert reference answers for multi-reference semantic scoring
_REFERENCES = {
    "Redux": [
        "I use Redux Toolkit's createSlice to define reducers and actions together. For async logic like API calls, I use createAsyncThunk and handle the pending, fulfilled, and rejected states in extraReducers to update loading and error flags.",
        "I structure the Redux store by feature. I keep the state normalized using createEntityAdapter, which stores data in an entities dictionary keyed by ID and an array of ids. This prevents data duplication and makes updates O(1).",
        "To optimize React components connected to Redux, I use the selector pattern with reselect (createSelector in RTK). This memoizes derived state calculations so components only re-render when their specific slice of data changes."
    ],
    "React": [
        "I build functional components using hooks. For local state I use useState, and for side effects like data fetching or subscriptions I use useEffect with a dependency array. I always include a cleanup function in useEffect to prevent memory leaks.",
        "For complex state logic involving multiple sub-values, I prefer useReducer over useState. If state needs to be accessed deeply in the component tree without prop drilling, I wrap the tree in a Context Provider and use useContext.",
        "I optimize rendering performance by wrapping expensive components in React.memo and wrapping callback functions in useCallback. For heavy calculations that shouldn't run on every render, I use useMemo."
    ],
    "JavaScript": [
        "I handle asynchronous operations using Promises and the async/await syntax. For multiple independent API calls, I use Promise.all to run them in parallel and await the combined results, or Promise.allSettled if I want to handle partial failures.",
        "I understand closures as functions that remember the lexical scope in which they were created, even after the outer function has returned. I use them for data privacy, currying, and maintaining state in event handlers.",
        "I am familiar with the JavaScript event loop, the call stack, and the task queues. Microtasks like Promise callbacks have priority over macrotasks like setTimeout, which is crucial for preventing UI blocking."
    ],
    "Webpack": [
        "I optimize bundle size by enabling tree shaking in production mode, ensuring sideEffects is set correctly in package.json. I extract common vendor libraries into a separate chunk using SplitChunksPlugin to improve caching.",
        "I implement code splitting at the route level using React.lazy and dynamic import(). This ensures the initial payload is small and additional chunks are only loaded over the network when the user navigates to those routes.",
        "For long-term caching, I configure output filenames with [contenthash]. I use loaders like babel-loader for transpiling JSX and ES6, and plugins like MiniCssExtractPlugin to extract CSS into separate files."
    ],
    "Redis": [
        "I use Redis as a cache-aside layer to reduce database load. When a read misses the cache, I query the primary database and write the result to Redis with a TTL (using SETEX) to ensure data eventually expires and doesn't become stale.",
        "I choose the appropriate data structure for the use case: STRING for simple serialized JSON objects, HASH for user profiles where I need to read or update individual fields with HGET/HSET, and Sorted Sets (ZSET) for leaderboards.",
        "To prevent cache stampedes under heavy load when a key expires, I implement a distributed lock using SETNX. Only the thread that acquires the lock queries the database and repopulates the cache, while others wait or return stale data."
    ],
    "SQL": [
        "I write complex queries using INNER and LEFT JOINs across multiple tables. For aggregations that also need to retain individual row details, I use window functions like ROW_NUMBER() and RANK() partitioned by specific columns.",
        "I improve query readability and modularity using Common Table Expressions (CTEs) instead of nested subqueries. I also ensure transactions are properly scoped with BEGIN, COMMIT, and ROLLBACK to maintain ACID compliance.",
        "To optimize slow queries, I analyze the execution plan using EXPLAIN ANALYZE. I ensure appropriate indexes exist, such as covering indexes or composite indexes that match the query's WHERE and ORDER BY clauses, avoiding full table scans."
    ],
    "Advanced SQL": [
        "I diagnose slow queries with EXPLAIN ANALYZE and pg_stat_statements. I optimize with composite and partial indexes, table partitioning by date, CTEs, materialized views, and query rewrites. I replace full-table scans with partition pruning and precompute aggregations into summary tables.",
        "I manage large datasets by partitioning tables by date so queries can leverage partition pruning. For heavy reporting queries, I build materialized views and refresh them concurrently during off-peak hours to avoid blocking reads.",
        "I handle concurrency issues by understanding transaction isolation levels. I use pessimistic locking (SELECT FOR UPDATE) or optimistic locking with version columns to prevent lost updates in high-transaction environments."
    ],
    "Database Design": [
        "I design schemas following normalization rules up to 3NF to eliminate data redundancy. I define strict foreign key constraints for referential integrity and create primary keys using UUIDs or auto-incrementing integers.",
        "I use a hybrid modeling approach for flexible schemas. I store common structured attributes in standard columns and use a JSONB column with a GIN index for diverse, sparse attributes like product specifications in an e-commerce catalog.",
        "I evaluate the trade-offs between normalization and denormalization. For read-heavy analytical workloads, I might denormalize data into a star schema or wide tables to eliminate expensive joins at query time."
    ],
    "ETL": [
        "I design idempotent ETL pipelines. For incremental extracts, I track high-watermarks like updated_at timestamps. During the load phase, I use UPSERT or MERGE statements keyed on a natural business key to prevent duplicates on retries.",
        "I ensure data quality by implementing validation checks and assertions at each stage. I monitor row counts, check for nulls in critical columns, and perform reconciliation by comparing source system totals against data warehouse aggregates.",
        "I orchestrate pipelines using DAGs in tools like Airflow. I structure tasks so they are modular, retryable, and handle failures gracefully by sending alerts and logging detailed error metrics without corrupting the target tables."
    ],
    "Database Security": [
        "I enforce least-privilege access by creating dedicated database roles per microservice with only the tables and operations they need. I revoke PUBLIC schema access, enable row-level security for tenant isolation, and rotate credentials regularly via a secrets manager like Vault or AWS KMS.",
        "For data at rest I use column-level encryption with pgcrypto for sensitive fields like SSNs and card numbers, and disk-level encryption for backups. I enforce TLS for all connections in transit and store encryption keys outside the database.",
        "I implement audit logging for all DDL and DML on sensitive tables, ship logs to a SIEM, and configure alerts for anomalous access. I comply with PCI-DSS by tokenizing PANs and minimizing PII persistence scope."
    ],
    "Database Performance Tuning": [
        "I diagnose slow queries by running EXPLAIN ANALYZE to read the actual execution plan, checking pg_stat_statements for cumulative statistics, and querying pg_stat_activity and pg_locks to detect blocking transactions or lock contention.",
        "I optimize through indexing: adding composite indexes that cover the WHERE and ORDER BY columns, partial indexes for filtered subsets, and covering indexes to avoid heap fetches. I also run ANALYZE to refresh planner statistics when they go stale.",
        "For queries that cannot be fast on-demand, I precompute results into materialized views refreshed concurrently on a schedule, partition large tables by date for pruning, and offload analytics to read replicas or columnar stores to avoid contention with OLTP writes."
    ],
    "Advanced Database Design": [
        "I design schemas following normalization up to 3NF for transactional data, then selectively denormalize into summary tables or star schemas for analytical workloads to eliminate expensive joins at query time.",
        "I use a hybrid approach for flexible product catalogs: a core relational table for common fields and a JSONB column with GIN index for diverse per-product attributes. This avoids EAV join complexity while keeping the schema evolvable.",
        "I apply partitioning by date on large append-only tables so queries leverage partition pruning. I use foreign key constraints and check constraints to enforce data integrity at the database level rather than relying solely on application validation."
    ]
}

# Map LLM-generated verbose names to canonical references
_REFERENCES["Advanced SQL and Query Optimization"] = _REFERENCES["Advanced SQL"]
_REFERENCES["Query Optimization"] = _REFERENCES["Advanced SQL"]
_REFERENCES["Database Design and Data Modeling"] = _REFERENCES["Database Design"]
_REFERENCES["Data Modeling"] = _REFERENCES["Database Design"]
_REFERENCES["Advanced Database Design and Data Modeling"] = _REFERENCES["Advanced Database Design"]
_REFERENCES["Advanced Database Design and Modeling"] = _REFERENCES["Advanced Database Design"]
_REFERENCES["ETL Pipeline Development"] = _REFERENCES["ETL"]
_REFERENCES["ETL Pipelines"] = _REFERENCES["ETL"]
_REFERENCES["Data Pipeline"] = _REFERENCES["ETL"]
_REFERENCES["Database Performance"] = _REFERENCES["Database Performance Tuning"]
_REFERENCES["Performance Tuning"] = _REFERENCES["Database Performance Tuning"]
_REFERENCES["Database Security and Compliance"] = _REFERENCES["Database Security"]


# ── ChromaDB initialisation ───────────────────────────────────────────────────

_chroma_client = None
_collection = None


def _get_collection(force_repopulate: bool = False):
    global _chroma_client, _collection

    if _chroma_client is None:
        db_path = os.path.join(os.getcwd(), "chroma_db")
        _chroma_client = chromadb.PersistentClient(path=db_path)

    # If the existing collection was built with the old L2 metric, delete it
    # so we recreate it with the correct cosine metric below.
    if _collection is None:
        existing_names = [c.name for c in _chroma_client.list_collections()]
        if "skill_references" in existing_names:
            existing = _chroma_client.get_collection("skill_references")
            if (existing.metadata or {}).get("hnsw:space") != "cosine":
                _chroma_client.delete_collection("skill_references")

        _collection = _chroma_client.get_or_create_collection(
            name="skill_references",
            metadata={"hnsw:space": "cosine"}   # cosine distance in [0, 2]
        )

    # Auto-repopulate when new skills have been added to _REFERENCES
    expected_docs = sum(len(refs) for refs in _REFERENCES.values())
    if _collection.count() < expected_docs or force_repopulate:
        try:
            _collection.delete(where={"tier": "expert"})
        except Exception:
            pass
        _populate_collection(_collection)

    return _collection


def _populate_collection(col):
    """Insert all expert references into ChromaDB."""
    documents = []
    metadatas = []
    ids = []

    for skill, refs in _REFERENCES.items():
        for idx, text in enumerate(refs):
            documents.append(text)
            metadatas.append({"skill": skill, "tier": "expert"})
            ids.append(f"ref_{skill.replace(' ', '_')}_{idx}")

    if documents:
        col.add(documents=documents, metadatas=metadatas, ids=ids)


def get_semantic_score(answer: str, skill: str) -> float:
    """
    Query ChromaDB for the closest expert reference for the given skill.

    With cosine distance (hnsw:space=cosine), ChromaDB returns values in [0, 2]:
      0.0 = identical  (perfect match)
      ~0.3 = very similar (expert-level)
      ~0.6 = on-topic but different phrasing
      1.0 = orthogonal  (unrelated)

    We query the top-3 refs for the skill, take the best (lowest distance),
    then convert to a 0-1 proficiency score.
    """
    if not answer.strip():
        return 0.5

    try:
        col = _get_collection()
        n = min(3, col.count())
        if n == 0:
            return 0.5

        # Fuzzy matching for composite skill names (e.g. "Advanced SQL & Database Design")
        query_skill = skill
        if col.count() > 0:
            # If the exact skill isn't in our references, try to find a substring match
            # We know the known skills are keys in _REFERENCES (excluding aliases)
            known_skills = list(_REFERENCES.keys())
            if skill not in known_skills:
                for ks in known_skills:
                    if ks.lower() in skill.lower():
                        query_skill = ks
                        break

        results = col.query(
            query_texts=[answer],
            n_results=n,
            where={"skill": query_skill}
        )

        distances = results.get("distances")
        if not distances or not distances[0]:
            # Try without the where filter if still not found, just get the closest text
            results = col.query(query_texts=[answer], n_results=1)
            distances = results.get("distances")
            if not distances or not distances[0]:
                return 0.5

        # Take the best (lowest cosine distance) among returned results
        best_dist = min(distances[0])

        # Map cosine distance → proficiency [0, 1]
        # CEIL: distance at or below this → score 1.0 (expert match)
        # FLOOR: distance at or above this → score 0.0 (unrelated)
        # Relaxed bounds for MiniLM embeddings to be more forgiving of phrasing differences
        CEIL  = 0.35   # good thematic match
        FLOOR = 0.85   # effectively unrelated
        rescaled = (FLOOR - best_dist) / (FLOOR - CEIL)

        return round(max(0.0, min(1.0, rescaled)), 3)

    except Exception as e:
        print(f"[ChromaDB] Semantic scoring failed for '{skill}': {e}")
        return 0.5
