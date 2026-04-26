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
    "React": ["hooks", "useEffect", "useState", "props", "virtual DOM", "JSX", "component"],
    "AWS": ["EC2", "S3", "RDS", "Lambda", "IAM", "VPC", "ECS"],
    "CI/CD": ["pipeline", "automated testing", "deployment", "GitHub Actions", "artifact", "rollback"],
    "Redis": ["cache", "pub/sub", "TTL", "eviction", "cluster", "persistence"],
    "MongoDB": ["document", "collection", "aggregation", "index", "NoSQL", "schema"],
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
