import networkx as nx

# --- Skill Registry ---
SKILLS = {
    "Python": "Programming", "Django": "Web Backend", "FastAPI": "Web Backend",
    "Flask": "Web Backend", "REST APIs": "Web Backend", "GraphQL": "Web Backend",
    "Celery": "Web Backend", "Node.js": "Web Backend", "Spring Boot": "Web Backend",
    "SQL": "Database", "PostgreSQL": "Database", "MySQL": "Database",
    "MongoDB": "Database", "Redis": "Database",
    "Docker": "DevOps", "Kubernetes": "DevOps", "CI/CD": "DevOps", "Linux": "DevOps",
    "AWS": "Cloud", "GCP": "Cloud", "Azure": "Cloud",
    "JavaScript": "Frontend", "TypeScript": "Frontend", "React": "Frontend",
    "Vue": "Frontend", "HTML/CSS": "Frontend",
    "Machine Learning": "AI/ML", "Deep Learning": "AI/ML", "LangChain": "AI/ML",
    "PyTorch": "AI/ML", "TensorFlow": "AI/ML",
    "Microservices": "Architecture", "System Design": "Architecture",
    "Git": "Tools", "Java": "Programming",
    "Data Structures": "CS Fundamentals", "Algorithms": "CS Fundamentals",
}

EDGES = [
    # PREREQUISITE_OF
    ("Python", "Django"), ("Python", "FastAPI"), ("Python", "Flask"),
    ("Python", "Celery"), ("Python", "Machine Learning"),
    ("SQL", "PostgreSQL"), ("SQL", "MySQL"),
    ("Docker", "Kubernetes"),
    ("JavaScript", "React"), ("JavaScript", "Vue"),
    ("JavaScript", "TypeScript"), ("JavaScript", "Node.js"),
    ("Machine Learning", "Deep Learning"),
    ("Java", "Spring Boot"),
    ("HTML/CSS", "JavaScript"),
    ("Data Structures", "Algorithms"),
    # ADJACENT_TO
    ("Django", "REST APIs"), ("FastAPI", "REST APIs"), ("Flask", "REST APIs"),
    ("REST APIs", "GraphQL"), ("Django", "PostgreSQL"), ("FastAPI", "PostgreSQL"),
    ("Docker", "CI/CD"), ("Kubernetes", "AWS"), ("Kubernetes", "GCP"),
    ("Microservices", "Docker"), ("Microservices", "REST APIs"),
    ("System Design", "Microservices"), ("LangChain", "Python"),
    ("Redis", "Django"), ("Redis", "FastAPI"), ("Celery", "Redis"),
    ("AWS", "CI/CD"),
]

SAME_DOMAIN = [
    ("Django", "FastAPI"), ("Django", "Flask"),
    ("PostgreSQL", "MySQL"), ("PostgreSQL", "MongoDB"),
    ("React", "Vue"), ("AWS", "GCP"), ("AWS", "Azure"),
    ("PyTorch", "TensorFlow"),
]

# --- Gold Standard Answers (for semantic scoring) ---
GOLD_STANDARD_ANSWERS = {
    "Python": "I use Python extensively with async programming via asyncio, decorators, context managers, and generators. I build production systems leveraging OOP design patterns and use list comprehensions for efficient data processing. I understand the GIL and when to use multiprocessing vs threading.",
    "Django": "I build scalable Django applications using ORM for complex queries with select_related and prefetch_related, custom middleware, signals for decoupled logic, and Celery for async tasks. I'm proficient with migrations, DRF for APIs, and Django admin customization.",
    "FastAPI": "I build production APIs with FastAPI using async/await, Pydantic models for request validation, dependency injection for database sessions and auth, and automatic OpenAPI docs. I leverage type hints throughout for better code quality and IDE support.",
    "Docker": "I containerize applications with multi-stage Dockerfiles to minimize image size. I use Docker Compose for orchestrating multi-service local environments with proper volume mounts, health checks, and network configuration.",
    "REST APIs": "I design REST APIs following HTTP semantics: proper verbs, meaningful status codes, versioning strategies, cursor-based pagination, JWT authentication, and rate limiting. I use OpenAPI specs for documentation and contract testing.",
    "SQL": "I write complex SQL including multi-table JOINs, CTEs, window functions, and aggregations. I optimize queries using EXPLAIN ANALYZE, create appropriate indexes including composite and partial indexes, and understand transaction isolation levels.",
    "PostgreSQL": "I use PostgreSQL-specific features like JSONB columns, full-text search, advisory locks, and connection pooling with PgBouncer. I monitor with pg_stat_views and use EXPLAIN ANALYZE to optimize slow queries.",
    "Machine Learning": "I build end-to-end ML pipelines: EDA, feature engineering, model selection using cross-validation, hyperparameter tuning, and production deployment with monitoring for data drift and model degradation.",
    "System Design": "I design distributed systems considering CAP theorem tradeoffs, implement caching layers with Redis, use load balancers, database sharding strategies, and event-driven architectures for loose coupling and scalability.",
    "Microservices": "I architect microservices with API gateway patterns, service discovery, and async messaging via queues. I implement circuit breakers for resilience, distributed tracing, and design services around bounded contexts.",
    "React": "I build React apps with functional components and hooks. I manage complex state with useReducer and Context API or Zustand, optimize re-renders with useMemo/useCallback, and code-split for performance.",
    "AWS": "I deploy on AWS using EC2 with auto-scaling groups, RDS for managed databases, S3 for storage, Lambda for serverless functions, and ECS/EKS for containers. I configure VPCs, security groups, and IAM roles for least-privilege access.",

    # ── FRONTEND ──
    "Redux": "I use Redux Toolkit with createSlice and createAsyncThunk for predictable state management. I structure the store by feature, use RTK Query for server state, and apply the selector pattern with memoization using reselect to avoid unnecessary re-renders.",
    "TypeScript": "I use TypeScript across the entire stack with strict mode enabled. I write generic utility types, discriminated unions for state machines, and use interface vs type aliases appropriately. I leverage mapped types and conditional types for advanced type transformations.",
    "Next.js": "I build production Next.js applications using the App Router with React Server Components for data fetching, dynamic routes, and static generation. I use next/image for optimization, middleware for auth, and deploy on Vercel with ISR for content-heavy pages.",
    "Vue": "I build Vue 3 applications using the Composition API with reactive refs and computed properties. I manage state with Pinia, handle routing with Vue Router, and use Vite for fast builds with tree-shaking.",
    "Angular": "I build Angular applications with TypeScript, using modules, services, and dependency injection. I manage state with NgRx, implement lazy loading for routes, use RxJS observables for async operations, and write unit tests with Jasmine and Karma.",
    "Webpack": "I configure Webpack with custom loaders and plugins for a React project. I set up code splitting with dynamic imports, tree-shaking, asset optimization, and separate dev/production configs with environment variables. I profile bundle size using webpack-bundle-analyzer.",
    "Jest": "I write unit and integration tests using Jest with React Testing Library. I mock modules and API calls with jest.mock, use beforeEach/afterEach for setup and teardown, test async code with waitFor, and measure code coverage to identify gaps.",
    "Enzyme": "I use Enzyme to shallow and mount React components in tests. I simulate user interactions, inspect props and state, and test component lifecycle methods. I prefer shallow rendering for unit tests to isolate components from their children.",
    "Mocha": "I use Mocha as a test runner for Node.js applications paired with Chai for assertions and Sinon for mocks and spies. I structure tests with describe/it blocks, handle async tests with done callbacks or async/await, and integrate with Istanbul for coverage.",
    "JavaScript": "I have deep JavaScript knowledge including closures, prototypal inheritance, the event loop, promises, async/await, and ES2022+ features. I understand hoisting, scope chains, and can optimize performance by avoiding memory leaks and unnecessary re-renders.",
    "HTML/CSS": "I write semantic HTML5 with proper ARIA attributes for accessibility. I build responsive layouts using Flexbox and CSS Grid, use CSS custom properties for theming, and write BEM-structured class names. I understand the cascade, specificity, and box model deeply.",

    # ── BACKEND ──
    "Node.js": "I build scalable Node.js applications using the event loop for non-blocking I/O. I use streams for large file processing, worker threads for CPU-bound tasks, and cluster mode for multi-core utilization. I profile memory leaks using the V8 heap profiler.",
    "Express": "I build REST APIs with Express using middleware for logging, auth, and error handling. I structure projects with the MVC pattern, use Joi or Zod for request validation, implement JWT auth middleware, and write integration tests with Supertest.",
    "Flask": "I build Flask APIs with Blueprints for modularity, Flask-SQLAlchemy for ORM, and Marshmallow for serialization. I implement JWT auth, handle CORS, use Flask-Migrate for schema migrations, and deploy with Gunicorn behind Nginx.",
    "Spring Boot": "I build Spring Boot microservices using REST controllers, JPA repositories, and Spring Security for authentication. I use dependency injection with @Autowired, configure profiles for different environments, and write unit tests with JUnit 5 and Mockito.",
    "Go": "I write idiomatic Go with goroutines and channels for concurrency. I build HTTP APIs using net/http or Gin, use interfaces for dependency injection and testing, handle errors explicitly, and use Go modules for dependency management.",
    "GraphQL": "I design GraphQL schemas with queries, mutations, and subscriptions. I implement resolvers with DataLoader to avoid N+1 queries, handle authentication via context, use Apollo Server or Strawberry, and write schema-first with code generation.",

    # ── AI / ML ──
    "Deep Learning": "I build neural networks using PyTorch or TensorFlow with custom training loops, learning rate schedulers, and gradient clipping. I implement CNNs for image tasks and Transformers for NLP, track experiments with MLflow, and deploy models as REST APIs.",
    "PyTorch": "I implement custom neural network architectures by subclassing nn.Module. I write efficient training loops with gradient accumulation, use DataLoader with custom datasets, apply transfer learning from pretrained models, and export models to ONNX for production.",
    "TensorFlow": "I build TensorFlow models using the Keras API with custom layers and training loops. I use tf.data pipelines for efficient data ingestion, apply model quantization for edge deployment, and use TensorFlow Serving for production inference.",
    "Hugging Face": "I fine-tune pretrained Transformer models using the Hugging Face Trainer API with custom datasets. I use tokenizers, pipelines for inference, PEFT methods like LoRA for efficient fine-tuning, and push models to the Hub for sharing and deployment.",
    "Pandas": "I use pandas for data wrangling including groupby aggregations, merge/join operations, and time-series resampling. I optimize memory usage with dtype casting, use vectorized operations instead of loops, and handle missing data with fillna and interpolation strategies.",
    "NumPy": "I use NumPy for efficient numerical computation with broadcasting, vectorized operations, and linear algebra routines. I understand memory layout (C vs Fortran order), use fancy indexing for filtering, and integrate with pandas and scikit-learn pipelines.",

    # ── DATABASES ──
    "MySQL": "I design normalized MySQL schemas with proper indexes including composite and covering indexes. I write complex queries with JOINs, subqueries, and stored procedures. I analyze slow queries using EXPLAIN and optimize with query caching and connection pooling.",
    "MongoDB": "I design MongoDB document schemas balancing embedding vs referencing based on query patterns. I use the aggregation pipeline for complex data transformations, create compound indexes for performance, and implement change streams for real-time features.",
    "Elasticsearch": "I use Elasticsearch for full-text search with custom analyzers, tokenizers, and filters. I design index mappings with appropriate field types, use bool queries with must/should/filter clauses, implement aggregations for analytics, and manage index lifecycle policies.",
    "Firebase": "I build real-time applications with Firestore using onSnapshot listeners for live updates. I structure collections for query efficiency, implement security rules for row-level access control, use Cloud Functions for server-side logic, and use Firebase Auth for authentication.",
    "Redis": "I use Redis as a cache-aside layer to reduce database latency. I choose between STRING for simple JSON blobs and HASH for partial field updates. I set TTLs with SETEX/EXPIRE for automatic eviction, invalidate keys on writes, and use SETNX locks to prevent cache stampedes under high load.",
    "SQL": "I write complex SQL including multi-table JOINs, CTEs, window functions, and aggregations. I optimize queries using EXPLAIN ANALYZE, create appropriate indexes including composite and partial indexes, and understand transaction isolation levels.",
    "Advanced SQL": "I diagnose slow queries with EXPLAIN ANALYZE and pg_stat_statements. I optimize with composite and partial indexes, table partitioning by date, CTEs, materialized views, and query rewrites. I replace full-table scans with partition pruning and precompute aggregations into summary tables.",
    "Advanced SQL and Query Optimization": "I diagnose slow queries with EXPLAIN ANALYZE and pg_stat_statements. I optimize with composite and partial indexes, table partitioning by date, CTEs, materialized views, and query rewrites. I replace full-table scans with partition pruning and precompute aggregations into summary tables.",
    "Query Optimization": "I diagnose slow queries with EXPLAIN ANALYZE and pg_stat_statements. I optimize with composite and partial indexes, table partitioning by date, CTEs, materialized views, and query rewrites. I replace full-table scans with partition pruning and precompute aggregations into summary tables.",
    "Database Design": "I design relational schemas with normalized tables, proper primary and foreign keys, and indexes aligned to query patterns. For flexible attributes I use JSONB columns with GIN indexes instead of EAV tables. I consider read vs write trade-offs and choose between normalization and denormalization based on access patterns.",
    "Database Design and Data Modeling": "I design relational schemas with normalized tables, proper primary and foreign keys, and indexes aligned to query patterns. For flexible attributes I use JSONB columns with GIN indexes instead of EAV tables. I consider read vs write trade-offs and choose between normalization and denormalization based on access patterns.",
    "Data Modeling": "I design relational schemas with normalized tables, proper primary and foreign keys, and indexes aligned to query patterns. For flexible attributes I use JSONB columns with GIN indexes instead of EAV tables. I consider read vs write trade-offs and choose between normalization and denormalization based on access patterns.",
    "ETL": "I build reliable ETL pipelines that extract data with idempotent high-watermark queries, transform with validation and reconciliation checks, and load using upserts keyed on natural business keys. I embed data quality assertions, monitor row counts and sum totals at each stage, and alert on anomalies before dashboards are served.",
    "ETL Pipeline Development": "I build reliable ETL pipelines that extract data with idempotent high-watermark queries, transform with validation and reconciliation checks, and load using upserts keyed on natural business keys. I embed data quality assertions, monitor row counts and sum totals at each stage, and alert on anomalies before dashboards are served.",
    "ETL Pipelines": "I build reliable ETL pipelines that extract data with idempotent high-watermark queries, transform with validation and reconciliation checks, and load using upserts keyed on natural business keys. I embed data quality assertions, monitor row counts and sum totals at each stage, and alert on anomalies before dashboards are served.",
    "Data Pipeline": "I build reliable ETL pipelines that extract data with idempotent high-watermark queries, transform with validation and reconciliation checks, and load using upserts keyed on natural business keys. I embed data quality assertions, monitor row counts and sum totals at each stage, and alert on anomalies before dashboards are served.",
    "Azure": "I deploy and manage services on Azure including Azure SQL Database, Blob Storage, Azure Data Factory for pipelines, and Azure Kubernetes Service. I configure managed identities for secure access, use Key Vault for secrets, monitor with Application Insights, and deploy via Azure DevOps pipelines.",
    "Azure Data Engineering": "I deploy and manage services on Azure including Azure SQL Database, Blob Storage, Azure Data Factory for pipelines, and Azure Kubernetes Service. I configure managed identities for secure access, use Key Vault for secrets, monitor with Application Insights, and deploy via Azure DevOps pipelines.",

    # ── DEVOPS ──
    "Linux": "I am proficient with Linux command-line tools including bash scripting, process management with systemd, file permissions with chmod/chown, network diagnostics with netstat and curl, and log analysis with grep, awk, and sed. I manage packages with apt/yum and configure cron jobs.",
}

# --- Expected Keywords per Skill ---
SKILL_KEYWORDS = {
    "Python": ["decorator", "generator", "asyncio", "GIL", "OOP", "lambda", "context manager", "list comprehension"],
    "Django": ["ORM", "migrations", "middleware", "signals", "queryset", "DRF", "admin", "views"],
    "FastAPI": ["async", "pydantic", "dependency injection", "OpenAPI", "type hints", "swagger"],
    "Docker": ["Dockerfile", "container", "image", "volume", "compose", "layer", "multi-stage"],
    "REST APIs": ["HTTP", "status codes", "authentication", "pagination", "serialization", "JWT", "versioning"],
    "SQL": ["JOIN", "GROUP BY", "INDEX", "transaction", "normalization", "window function", "CTE"],
    "PostgreSQL": ["JSONB", "indexing", "explain analyze", "connection pooling", "pg_stat"],
    "Kubernetes": ["pod", "deployment", "service", "ingress", "configmap", "helm", "scaling", "namespace"],
    "Machine Learning": ["training", "overfitting", "cross-validation", "feature engineering", "model selection"],
    "System Design": ["scalability", "load balancer", "caching", "CAP theorem", "sharding"],
    "Microservices": ["service discovery", "API gateway", "circuit breaker", "event-driven", "bounded context"],
    "React": ["hooks", "useEffect", "useState", "props", "virtual DOM", "JSX", "component",
               "loading", "error", "useReducer", "conditional", "useCallback", "useMemo",
               "re-render", "deps", "cleanup", "async", "fetch", "Promise"],
    "AWS": ["EC2", "S3", "RDS", "Lambda", "IAM", "VPC", "ECS"],
    "CI/CD": ["pipeline", "automated testing", "deployment", "GitHub Actions", "artifact", "rollback"],
    "Redis": ["cache", "pub/sub", "TTL", "eviction", "cluster", "persistence"],
    "MongoDB": ["document", "collection", "aggregation", "index", "NoSQL", "schema"],

    # ── FRONTEND ──
    "Redux": ["slice", "reducer", "action", "store", "dispatch", "selector", "middleware", "thunk", "RTK"],
    "TypeScript": ["interface", "type", "generic", "union", "enum", "strict", "infer", "mapped type", "type guard"],
    "Next.js": ["server component", "app router", "ISR", "static generation", "SSR", "middleware", "route handler"],
    "Vue": ["composition API", "ref", "reactive", "computed", "emit", "props", "Pinia", "Vue Router"],
    "Angular": ["component", "service", "module", "NgRx", "RxJS", "observable", "dependency injection", "decorator"],
    "Webpack": ["bundle", "loader", "plugin", "code splitting", "tree shaking", "entry", "output", "HMR"],
    "Jest": ["describe", "it", "expect", "mock", "spy", "beforeEach", "coverage", "snapshot", "async"],
    "Enzyme": ["shallow", "mount", "wrapper", "simulate", "props", "state", "find", "render"],
    "Mocha": ["describe", "it", "before", "after", "Chai", "assert", "async", "done", "Sinon"],
    "JavaScript": ["closure", "prototype", "event loop", "Promise", "async", "await", "hoisting",
                    "scope", "ES6", "fetch", "Promise.all", "Promise.allSettled", "then",
                    "catch", "finally", "destructure", "spread", "arrow function", "module"],
    "HTML/CSS": ["semantic", "flexbox", "grid", "responsive", "ARIA", "specificity", "cascade", "BEM"],

    # ── BACKEND ──
    "Node.js": ["event loop", "async", "stream", "buffer", "cluster", "middleware", "npm", "callback"],
    "Express": ["route", "middleware", "request", "response", "router", "JWT", "cors", "body-parser"],
    "Flask": ["Blueprint", "route", "request", "SQLAlchemy", "Marshmallow", "JWT", "Gunicorn", "CORS"],
    "Spring Boot": ["controller", "service", "repository", "JPA", "autowired", "bean", "REST", "Spring Security"],
    "Go": ["goroutine", "channel", "interface", "struct", "error handling", "defer", "context", "module"],
    "GraphQL": ["schema", "query", "mutation", "resolver", "subscription", "DataLoader", "Apollo", "type"],

    # ── AI / ML ──
    "Deep Learning": ["neural network", "backpropagation", "gradient", "epoch", "loss", "CNN", "Transformer", "layer"],
    "PyTorch": ["tensor", "autograd", "nn.Module", "DataLoader", "optimizer", "backward", "CUDA", "checkpoint"],
    "TensorFlow": ["tensor", "Keras", "layer", "optimizer", "tf.data", "graph", "session", "model.fit"],
    "Hugging Face": ["Trainer", "tokenizer", "pipeline", "fine-tuning", "BERT", "LoRA", "Hub", "transformer"],
    "Pandas": ["DataFrame", "groupby", "merge", "apply", "fillna", "index", "pivot", "resample"],
    "NumPy": ["array", "broadcasting", "vectorized", "reshape", "dot", "axis", "dtype", "slicing"],

    # ── DATABASES ──
    "MySQL": ["JOIN", "index", "transaction", "stored procedure", "EXPLAIN", "normalization", "foreign key"],
    "Elasticsearch": ["index", "mapping", "query DSL", "aggregation", "analyzer", "shard", "replica", "bool query"],
    "Firebase": ["Firestore", "collection", "document", "onSnapshot", "security rules", "Cloud Functions", "Auth"],
    "Redis": ["cache", "HASH", "STRING", "TTL", "SETEX", "HGETALL", "HGET", "cache-aside", "invalidate", "SETNX",
              "expire", "pub/sub", "eviction", "stampede", "warm"],
    "SQL": ["JOIN", "GROUP BY", "INDEX", "transaction", "normalization", "window function", "CTE"],
    # Advanced SQL keywords cover BOTH diagnosis (EXPLAIN, pg_stat) AND architecture (materialized view, OLAP)
    "Advanced SQL": ["EXPLAIN", "EXPLAIN ANALYZE", "index", "composite index", "partition", "CTE",
                     "materialized view", "window function", "execution plan", "ANALYZE",
                     "pg_stat", "covering index", "OLAP", "read replica", "precompute",
                     "pg_locks", "pg_stat_activity", "blocking"],
    "Advanced SQL and Query Optimization": ["EXPLAIN", "EXPLAIN ANALYZE", "index", "composite index",
                                             "partition", "CTE", "materialized view", "window function",
                                             "execution plan", "pg_stat", "covering index", "ANALYZE",
                                             "OLAP", "read replica", "precompute"],
    "Query Optimization": ["EXPLAIN", "index", "composite index", "partition", "CTE",
                            "materialized view", "execution plan", "pg_stat", "covering index"],
    "Database Design": ["normalization", "foreign key", "primary key", "index", "JSONB", "GIN",
                         "EAV", "schema", "partition", "denormalization", "ERD", "constraint"],
    "Database Design and Data Modeling": ["normalization", "foreign key", "primary key", "index",
                                           "JSONB", "GIN", "EAV", "schema", "partition",
                                           "denormalization", "ERD", "constraint", "trade-off"],
    "Advanced Database Design": ["normalization", "denormalization", "star schema", "JSONB", "GIN",
                                  "partition", "foreign key", "constraint", "3NF", "ERD", "EAV",
                                  "check constraint", "index", "schema"],
    "Advanced Database Design and Data Modeling": ["normalization", "denormalization", "star schema",
                                                    "JSONB", "GIN", "partition", "foreign key",
                                                    "constraint", "3NF", "ERD", "EAV", "schema"],
    "Advanced Database Design and Modeling": ["normalization", "denormalization", "JSONB", "GIN",
                                               "partition", "foreign key", "constraint", "3NF", "schema"],
    "Data Modeling": ["normalization", "foreign key", "JSONB", "schema", "ERD", "constraint"],
    "Database Security": ["least privilege", "role", "GRANT", "REVOKE", "row-level security",
                           "encryption", "TLS", "pgcrypto", "audit", "SIEM", "PCI", "GDPR",
                           "tokenize", "secrets manager", "Vault", "KMS", "pg_audit"],
    "Database Security and Compliance": ["least privilege", "role", "GRANT", "REVOKE", "encryption",
                                          "TLS", "pgcrypto", "audit", "PCI", "GDPR", "tokenize"],
    "Database Performance Tuning": ["EXPLAIN ANALYZE", "pg_stat_statements", "pg_stat_activity",
                                     "pg_locks", "index", "composite index", "partition",
                                     "materialized view", "read replica", "ANALYZE", "OLAP",
                                     "blocking", "execution plan", "precompute", "covering index"],
    "Performance Tuning": ["EXPLAIN ANALYZE", "pg_stat", "index", "partition", "materialized view",
                            "read replica", "ANALYZE", "OLAP", "execution plan"],
    "Database Performance": ["EXPLAIN ANALYZE", "pg_stat", "index", "partition", "materialized view",
                              "read replica", "execution plan", "blocking"],
    "ETL": ["extract", "transform", "load", "idempotent", "upsert", "reconciliation",
            "watermark", "data quality", "pipeline", "row count", "MERGE", "stale", "freshness"],
    "ETL Pipeline Development": ["extract", "transform", "load", "idempotent", "upsert",
                                   "reconciliation", "watermark", "data quality", "row count",
                                   "MERGE", "stale", "freshness", "assertion", "late data"],
    "ETL Pipelines": ["extract", "transform", "load", "idempotent", "upsert", "reconciliation",
                       "watermark", "data quality", "row count", "MERGE", "stale"],
    "Data Pipeline": ["extract", "transform", "load", "idempotent", "upsert", "reconciliation",
                       "watermark", "data quality", "row count", "MERGE"],
    "Azure": ["Azure SQL", "Blob Storage", "Data Factory", "AKS", "Key Vault", "managed identity",
               "Application Insights", "Azure DevOps", "resource group", "subscription"],
    "Azure Data Engineering": ["Data Factory", "Azure SQL", "Blob Storage", "Synapse", "pipeline",
                                 "trigger", "linked service", "dataset", "managed identity"],

    # ── DEVOPS ──
    "Linux": ["bash", "chmod", "cron", "systemd", "grep", "awk", "ssh", "process", "pipe"],
}


def build_skill_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    for skill, domain in SKILLS.items():
        G.add_node(skill, domain=domain)
    for src, dst in EDGES:
        G.add_edge(src, dst, relation="PREREQUISITE_OF")
    for a, b in SAME_DOMAIN:
        G.add_edge(a, b, relation="SAME_DOMAIN_AS")
        G.add_edge(b, a, relation="SAME_DOMAIN_AS")
    return G


skill_graph = build_skill_graph()


def get_domain(skill: str) -> str:
    return skill_graph.nodes.get(skill, {}).get("domain", "General")


def get_prerequisites(skill: str) -> list[str]:
    return [src for src, dst, d in skill_graph.in_edges(skill, data=True)
            if d.get("relation") == "PREREQUISITE_OF"]


def get_adjacent_skills(skill: str) -> list[str]:
    adjacent = []
    for _, dst, d in skill_graph.out_edges(skill, data=True):
        if d.get("relation") in ("PREREQUISITE_OF", "SAME_DOMAIN_AS"):
            adjacent.append(dst)
    return adjacent


def find_skills_in_text(text: str) -> list[str]:
    """Find known skills mentioned in a text (JD or resume)."""
    text_lower = text.lower()
    found = []
    for skill in SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)
    return found


def get_skill_gaps(jd_skills: list[str], resume_skills: list[str]) -> list[str]:
    """Return skills in JD but not in resume."""
    resume_set = set(s.lower() for s in resume_skills)
    return [s for s in jd_skills if s.lower() not in resume_set]
