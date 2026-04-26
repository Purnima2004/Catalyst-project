import os
import chromadb
from chromadb.utils import embedding_functions

# Persistent ChromaDB stored in project root
_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
_client = chromadb.PersistentClient(path=_DB_PATH)
_ef = embedding_functions.DefaultEmbeddingFunction()

# Collections
_resource_col = _client.get_or_create_collection("learning_resources", embedding_function=_ef)
_gold_col = _client.get_or_create_collection("gold_answers", embedding_function=_ef)

# --- Curated Learning Resources ---
RESOURCES = [
    # Python
    {"id": "py1", "skill": "Python", "title": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "documentation", "hours": 8},
    {"id": "py2", "skill": "Python", "title": "Real Python – Advanced Python", "url": "https://realpython.com/tutorials/advanced/", "type": "article", "hours": 10},
    {"id": "py3", "skill": "Python", "title": "Build a CLI Tool with Click – Project", "url": "https://realpython.com/python-click/", "type": "project", "hours": 5},
    # Django
    {"id": "dj1", "skill": "Django", "title": "Django Official Tutorial", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "type": "documentation", "hours": 6},
    {"id": "dj2", "skill": "Django", "title": "Django REST Framework Tutorial", "url": "https://www.django-rest-framework.org/tutorial/quickstart/", "type": "documentation", "hours": 8},
    {"id": "dj3", "skill": "Django", "title": "Build a Blog API – Project", "url": "https://learndjango.com/tutorials/django-rest-framework-tutorial-todo-api", "type": "project", "hours": 10},
    # FastAPI
    {"id": "fa1", "skill": "FastAPI", "title": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "documentation", "hours": 6},
    {"id": "fa2", "skill": "FastAPI", "title": "FastAPI + PostgreSQL CRUD – Project", "url": "https://testdriven.io/blog/fastapi-crud/", "type": "project", "hours": 8},
    # Docker
    {"id": "dk1", "skill": "Docker", "title": "Docker Get Started", "url": "https://docs.docker.com/get-started/", "type": "documentation", "hours": 4},
    {"id": "dk2", "skill": "Docker", "title": "Dockerize a Python App – Project", "url": "https://docs.docker.com/language/python/", "type": "project", "hours": 3},
    {"id": "dk3", "skill": "Docker", "title": "Docker Compose for Django + PostgreSQL", "url": "https://docs.docker.com/samples/django/", "type": "project", "hours": 4},
    # SQL
    {"id": "sq1", "skill": "SQL", "title": "SQLZoo – Interactive SQL Tutorial", "url": "https://sqlzoo.net/wiki/SQL_Tutorial", "type": "course", "hours": 8},
    {"id": "sq2", "skill": "SQL", "title": "Mode SQL Tutorial – Intermediate", "url": "https://mode.com/sql-tutorial/", "type": "course", "hours": 5},
    {"id": "sq3", "skill": "SQL", "title": "Use The Index, Luke – Query Optimization", "url": "https://use-the-index-luke.com/", "type": "documentation", "hours": 6},
    # PostgreSQL
    {"id": "pg1", "skill": "PostgreSQL", "title": "PostgreSQL Official Tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html", "type": "documentation", "hours": 5},
    {"id": "pg2", "skill": "PostgreSQL", "title": "PostgreSQL Crash Course – Video", "url": "https://www.youtube.com/watch?v=qw--VYLpxG4", "type": "video", "hours": 4},
    # REST APIs
    {"id": "re1", "skill": "REST APIs", "title": "REST API Design Best Practices", "url": "https://www.freecodecamp.org/news/rest-api-design-best-practices-build-a-rest-api/", "type": "article", "hours": 3},
    {"id": "re2", "skill": "REST APIs", "title": "HTTP Status Codes Reference – MDN", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status", "type": "documentation", "hours": 1},
    # Machine Learning
    {"id": "ml1", "skill": "Machine Learning", "title": "fast.ai Practical Deep Learning", "url": "https://course.fast.ai/", "type": "course", "hours": 40},
    {"id": "ml2", "skill": "Machine Learning", "title": "Kaggle Learn – Intro to ML", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "course", "hours": 5},
    {"id": "ml3", "skill": "Machine Learning", "title": "Hands-On ML – Aurélien Géron", "url": "https://github.com/ageron/handson-ml3", "type": "book", "hours": 60},
    # System Design
    {"id": "sd1", "skill": "System Design", "title": "System Design Primer – GitHub", "url": "https://github.com/donnemartin/system-design-primer", "type": "documentation", "hours": 20},
    {"id": "sd2", "skill": "System Design", "title": "Grokking System Design Interview", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "type": "course", "hours": 30},
    # Microservices
    {"id": "ms1", "skill": "Microservices", "title": "Microservices.io Patterns", "url": "https://microservices.io/patterns/", "type": "documentation", "hours": 8},
    {"id": "ms2", "skill": "Microservices", "title": "Build Microservices with FastAPI – Project", "url": "https://testdriven.io/blog/fastapi-microservices/", "type": "project", "hours": 12},
    # React
    {"id": "rx1", "skill": "React", "title": "React Official Docs – Learn React", "url": "https://react.dev/learn", "type": "documentation", "hours": 10},
    {"id": "rx2", "skill": "React", "title": "Full Stack Open – React Module", "url": "https://fullstackopen.com/en/part1", "type": "course", "hours": 15},
    # AWS
    {"id": "aw1", "skill": "AWS", "title": "AWS Free Tier – Hands-on Labs", "url": "https://aws.amazon.com/free/", "type": "project", "hours": 10},
    {"id": "aw2", "skill": "AWS", "title": "AWS Cloud Practitioner Essentials", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "type": "course", "hours": 6},
    # Kubernetes
    {"id": "k8s1", "skill": "Kubernetes", "title": "Kubernetes Official Tutorial", "url": "https://kubernetes.io/docs/tutorials/", "type": "documentation", "hours": 8},
    {"id": "k8s2", "skill": "Kubernetes", "title": "Deploy a Django App on Kubernetes – Project", "url": "https://testdriven.io/blog/django-kubernetes/", "type": "project", "hours": 10},
    # LangChain
    {"id": "lc1", "skill": "LangChain", "title": "LangChain Official Docs", "url": "https://python.langchain.com/docs/get_started/introduction", "type": "documentation", "hours": 8},
    {"id": "lc2", "skill": "LangChain", "title": "Build a RAG App – Project", "url": "https://python.langchain.com/docs/use_cases/question_answering/", "type": "project", "hours": 6},
    # CI/CD
    {"id": "ci1", "skill": "CI/CD", "title": "GitHub Actions Official Docs", "url": "https://docs.github.com/en/actions", "type": "documentation", "hours": 5},
    {"id": "ci2", "skill": "CI/CD", "title": "CI/CD for Django – Practical Guide", "url": "https://testdriven.io/blog/django-github-actions/", "type": "project", "hours": 4},
    # Redis
    {"id": "rd1", "skill": "Redis", "title": "Redis Official Tutorial", "url": "https://redis.io/docs/manual/", "type": "documentation", "hours": 4},
    {"id": "rd2", "skill": "Redis", "title": "Redis with Django – Caching – Project", "url": "https://realpython.com/caching-in-django-with-redis/", "type": "project", "hours": 3},
]


def _seed_resources():
    """Seed resources into ChromaDB if empty."""
    if _resource_col.count() > 0:
        return
    docs = [f"{r['title']} – {r['skill']} ({r['type']}, ~{r['hours']}h)" for r in RESOURCES]
    ids = [r["id"] for r in RESOURCES]
    metas = [{"skill": r["skill"], "url": r["url"], "type": r["type"], "hours": r["hours"], "title": r["title"]} for r in RESOURCES]
    _resource_col.add(documents=docs, ids=ids, metadatas=metas)


def _seed_gold_answers():
    """Seed gold standard answers into ChromaDB if empty."""
    from data.skill_graph import GOLD_STANDARD_ANSWERS
    if _gold_col.count() > 0:
        return
    for skill, answer in GOLD_STANDARD_ANSWERS.items():
        _gold_col.add(documents=[answer], ids=[f"gold_{skill}"], metadatas=[{"skill": skill}])


def get_resources_for_skill(skill: str, top_k: int = 3) -> list[dict]:
    """Retrieve top-k learning resources for a skill via semantic search."""
    results = _resource_col.query(
        query_texts=[f"learning resources for {skill}"],
        n_results=min(top_k, _resource_col.count()),
        where={"skill": skill}
    )
    resources = []
    if results and results["metadatas"]:
        for meta, doc in zip(results["metadatas"][0], results["documents"][0]):
            resources.append({**meta, "description": doc})
    return resources


def get_semantic_similarity(answer: str, skill: str) -> float:
    """Compare answer to gold standard, return similarity score 0.0-1.0."""
    results = _gold_col.query(
        query_texts=[answer],
        n_results=1,
        where={"skill": skill}
    )
    if results and results["distances"] and results["distances"][0]:
        distance = results["distances"][0][0]
        # ChromaDB returns cosine distance (0=identical, 2=opposite)
        # Convert to similarity score 0-1
        similarity = max(0.0, 1.0 - (distance / 2.0))
        return round(similarity, 3)
    return 0.0


# Seed on import
_seed_resources()
_seed_gold_answers()
