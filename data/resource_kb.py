"""
Resource Knowledge Base
────────────────────────
ChromaDB-free implementation:
  - Resources stored in a simple Python dict keyed by skill
  - Semantic similarity computed directly via sentence-transformers cosine similarity
  - No external vector DB, no protobuf conflicts, no ONNX download on cloud
"""
from __future__ import annotations
import os
import numpy as np
from data.skill_graph import GOLD_STANDARD_ANSWERS as _GOLD_ANSWERS

# Lazy-loaded sentence-transformer model
_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# --- Curated Learning Resources (keyed by skill for O(1) lookup) ---
_RESOURCES: dict[str, list[dict]] = {

    # ── BACKEND ────────────────────────────────────────────────────
    "Python": [
        {"title": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "documentation", "hours": 8},
        {"title": "Real Python – Advanced Python", "url": "https://realpython.com/tutorials/advanced/", "type": "article", "hours": 10},
        {"title": "Build a CLI Tool with Click", "url": "https://realpython.com/python-click/", "type": "project", "hours": 5},
    ],
    "Django": [
        {"title": "Django Official Tutorial", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "type": "documentation", "hours": 6},
        {"title": "Django REST Framework Tutorial", "url": "https://www.django-rest-framework.org/tutorial/quickstart/", "type": "documentation", "hours": 8},
        {"title": "Build a Blog API – Project", "url": "https://learndjango.com/tutorials/django-rest-framework-tutorial-todo-api", "type": "project", "hours": 10},
    ],
    "FastAPI": [
        {"title": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "documentation", "hours": 6},
        {"title": "FastAPI + PostgreSQL CRUD", "url": "https://testdriven.io/blog/fastapi-crud/", "type": "project", "hours": 8},
    ],
    "Flask": [
        {"title": "Flask Official Tutorial", "url": "https://flask.palletsprojects.com/en/latest/tutorial/", "type": "documentation", "hours": 5},
        {"title": "REST API with Flask & SQLAlchemy", "url": "https://realpython.com/flask-connexion-rest-api/", "type": "project", "hours": 8},
    ],
    "Node.js": [
        {"title": "Node.js Official Docs – Guides", "url": "https://nodejs.org/en/docs/guides", "type": "documentation", "hours": 6},
        {"title": "The Node.js Handbook – freeCodeCamp", "url": "https://www.freecodecamp.org/news/the-complete-nodejs-guide/", "type": "article", "hours": 8},
        {"title": "Build a REST API with Node & Express", "url": "https://www.digitalocean.com/community/tutorials/nodejs-express-apis", "type": "project", "hours": 6},
    ],
    "Express": [
        {"title": "Express.js Official Guide", "url": "https://expressjs.com/en/guide/routing.html", "type": "documentation", "hours": 4},
        {"title": "Build a Node/Express REST API", "url": "https://www.freecodecamp.org/news/build-a-restful-api-using-node-express-and-mongodb/", "type": "project", "hours": 6},
    ],
    "Spring Boot": [
        {"title": "Spring Boot Official Getting Started", "url": "https://spring.io/guides/gs/spring-boot/", "type": "documentation", "hours": 5},
        {"title": "Building REST Services with Spring", "url": "https://spring.io/guides/tutorials/rest/", "type": "project", "hours": 8},
    ],
    "Go": [
        {"title": "A Tour of Go – Official", "url": "https://go.dev/tour/", "type": "course", "hours": 6},
        {"title": "Build a Web Application with Go", "url": "https://www.jetbrains.com/guide/go/tutorials/build_web_apps/", "type": "project", "hours": 10},
    ],
    "REST APIs": [
        {"title": "REST API Design Best Practices", "url": "https://www.freecodecamp.org/news/rest-api-design-best-practices-build-a-rest-api/", "type": "article", "hours": 3},
        {"title": "HTTP Status Codes Reference – MDN", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status", "type": "documentation", "hours": 1},
    ],
    "GraphQL": [
        {"title": "GraphQL Official Introduction", "url": "https://graphql.org/learn/", "type": "documentation", "hours": 5},
        {"title": "Full Stack GraphQL – Apollo", "url": "https://www.apollographql.com/tutorials/", "type": "course", "hours": 10},
    ],
    "Microservices": [
        {"title": "Microservices.io Patterns", "url": "https://microservices.io/patterns/", "type": "documentation", "hours": 8},
        {"title": "Build Microservices with FastAPI", "url": "https://testdriven.io/blog/fastapi-microservices/", "type": "project", "hours": 12},
    ],
    "System Design": [
        {"title": "System Design Primer – GitHub", "url": "https://github.com/donnemartin/system-design-primer", "type": "documentation", "hours": 20},
        {"title": "Grokking System Design Interview", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "type": "course", "hours": 30},
    ],

    # ── FRONTEND ────────────────────────────────────────────────────
    "React": [
        {"title": "React Official Docs – Learn React", "url": "https://react.dev/learn", "type": "documentation", "hours": 10},
        {"title": "Full Stack Open – React Module", "url": "https://fullstackopen.com/en/part1", "type": "course", "hours": 15},
    ],
    "Redux": [
        {"title": "Redux Official Documentation", "url": "https://redux.js.org/introduction/getting-started", "type": "documentation", "hours": 6},
        {"title": "Redux Toolkit Official Guide", "url": "https://redux-toolkit.js.org/introduction/getting-started", "type": "documentation", "hours": 5},
        {"title": "Redux Toolkit Tutorial – freeCodeCamp", "url": "https://www.freecodecamp.org/news/redux-and-redux-toolkit-for-beginners/", "type": "article", "hours": 4},
    ],
    "TypeScript": [
        {"title": "TypeScript Official Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "documentation", "hours": 8},
        {"title": "TypeScript Deep Dive – GitBook", "url": "https://basarat.gitbook.io/typescript/", "type": "book", "hours": 12},
        {"title": "TypeScript for React Developers", "url": "https://www.totaltypescript.com/tutorials/react-with-typescript", "type": "course", "hours": 6},
    ],
    "Next.js": [
        {"title": "Next.js Official Learn Course", "url": "https://nextjs.org/learn", "type": "course", "hours": 8},
        {"title": "Next.js Official Documentation", "url": "https://nextjs.org/docs", "type": "documentation", "hours": 6},
        {"title": "Build a Full-Stack App with Next.js", "url": "https://www.freecodecamp.org/news/build-a-full-stack-application-with-nextjs/", "type": "project", "hours": 10},
    ],
    "Vue": [
        {"title": "Vue.js Official Tutorial", "url": "https://vuejs.org/tutorial/", "type": "documentation", "hours": 6},
        {"title": "Vue Mastery – Free Intro Course", "url": "https://www.vuemastery.com/courses/intro-to-vue-3/intro-to-vue3/", "type": "course", "hours": 4},
    ],
    "Angular": [
        {"title": "Angular Official Tour of Heroes", "url": "https://angular.io/tutorial/tour-of-heroes", "type": "documentation", "hours": 8},
        {"title": "Angular – The Complete Guide (Overview)", "url": "https://angular.io/guide/architecture", "type": "documentation", "hours": 6},
    ],
    "Webpack": [
        {"title": "Webpack Official Getting Started", "url": "https://webpack.js.org/guides/getting-started/", "type": "documentation", "hours": 5},
        {"title": "Webpack 5 Full Tutorial – freeCodeCamp", "url": "https://www.freecodecamp.org/news/an-intro-to-webpack-what-it-is-and-how-to-use-it-8304ecdc3c60/", "type": "article", "hours": 4},
        {"title": "Webpack Optimization Guide", "url": "https://webpack.js.org/guides/tree-shaking/", "type": "documentation", "hours": 3},
    ],
    "Jest": [
        {"title": "Jest Official Documentation", "url": "https://jestjs.io/docs/getting-started", "type": "documentation", "hours": 5},
        {"title": "Testing React with Jest & RTL", "url": "https://testing-library.com/docs/react-testing-library/intro/", "type": "documentation", "hours": 6},
        {"title": "JavaScript Testing Best Practices", "url": "https://github.com/goldbergyoni/javascript-testing-best-practices", "type": "article", "hours": 4},
    ],
    "Enzyme": [
        {"title": "Enzyme Official Documentation", "url": "https://enzymejs.github.io/enzyme/", "type": "documentation", "hours": 4},
        {"title": "React Testing with Jest & Enzyme", "url": "https://medium.com/codeclan/testing-react-with-jest-and-enzyme-20505fec4675", "type": "article", "hours": 3},
    ],
    "Mocha": [
        {"title": "Mocha Official Documentation", "url": "https://mochajs.org/", "type": "documentation", "hours": 3},
        {"title": "Node.js Testing with Mocha & Chai", "url": "https://www.digitalocean.com/community/tutorials/how-to-use-mocha-with-node-js", "type": "article", "hours": 4},
    ],
    "JavaScript": [
        {"title": "The Modern JavaScript Tutorial – javascript.info", "url": "https://javascript.info/", "type": "documentation", "hours": 20},
        {"title": "You Don't Know JS (book series)", "url": "https://github.com/getify/You-Dont-Know-JS", "type": "book", "hours": 30},
    ],
    "HTML/CSS": [
        {"title": "MDN Web Docs – HTML Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "documentation", "hours": 6},
        {"title": "CSS Tricks – A Complete Guide to Flexbox", "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/", "type": "article", "hours": 2},
    ],

    # ── DATABASES ────────────────────────────────────────────────────
    "SQL": [
        {"title": "SQLZoo – Interactive SQL Tutorial", "url": "https://sqlzoo.net/wiki/SQL_Tutorial", "type": "course", "hours": 8},
        {"title": "Mode SQL Tutorial – Intermediate", "url": "https://mode.com/sql-tutorial/", "type": "course", "hours": 5},
        {"title": "Use The Index, Luke – Query Optimization", "url": "https://use-the-index-luke.com/", "type": "documentation", "hours": 6},
    ],
    "PostgreSQL": [
        {"title": "PostgreSQL Official Tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html", "type": "documentation", "hours": 5},
        {"title": "PostgreSQL Crash Course", "url": "https://www.youtube.com/watch?v=qw--VYLpxG4", "type": "video", "hours": 4},
    ],
    "MySQL": [
        {"title": "MySQL Official Tutorial", "url": "https://dev.mysql.com/doc/refman/8.0/en/tutorial.html", "type": "documentation", "hours": 5},
        {"title": "MySQL for Beginners – freeCodeCamp", "url": "https://www.freecodecamp.org/news/learn-sql-in-10-minutes/", "type": "article", "hours": 3},
    ],
    "MongoDB": [
        {"title": "MongoDB Official University Courses", "url": "https://learn.mongodb.com/", "type": "course", "hours": 10},
        {"title": "MongoDB Official CRUD Documentation", "url": "https://www.mongodb.com/docs/manual/crud/", "type": "documentation", "hours": 4},
    ],
    "Redis": [
        {"title": "Redis Official Tutorial", "url": "https://redis.io/docs/manual/", "type": "documentation", "hours": 4},
        {"title": "Redis with Django – Caching", "url": "https://realpython.com/caching-in-django-with-redis/", "type": "project", "hours": 3},
    ],
    "Elasticsearch": [
        {"title": "Elasticsearch Official Getting Started", "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html", "type": "documentation", "hours": 5},
        {"title": "Elasticsearch with Python (Quickstart)", "url": "https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html", "type": "documentation", "hours": 3},
    ],
    "Firebase": [
        {"title": "Firebase Official Docs – Get Started", "url": "https://firebase.google.com/docs/guides", "type": "documentation", "hours": 5},
        {"title": "Firebase + React Tutorial – freeCodeCamp", "url": "https://www.freecodecamp.org/news/react-crud-app-how-to-create-a-book-management-app-from-scratch-717764e02fd2/", "type": "project", "hours": 6},
    ],

    # ── AI / ML ──────────────────────────────────────────────────────
    "Machine Learning": [
        {"title": "fast.ai Practical Deep Learning", "url": "https://course.fast.ai/", "type": "course", "hours": 40},
        {"title": "Kaggle Learn – Intro to ML", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "course", "hours": 5},
        {"title": "Hands-On ML – Aurélien Géron", "url": "https://github.com/ageron/handson-ml3", "type": "book", "hours": 60},
    ],
    "Deep Learning": [
        {"title": "Deep Learning Specialization – Coursera", "url": "https://www.coursera.org/specializations/deep-learning", "type": "course", "hours": 80},
        {"title": "PyTorch Official 60-Minute Blitz", "url": "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html", "type": "documentation", "hours": 3},
    ],
    "PyTorch": [
        {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "documentation", "hours": 15},
        {"title": "Kaggle Learn – Deep Learning", "url": "https://www.kaggle.com/learn/deep-learning", "type": "course", "hours": 8},
    ],
    "TensorFlow": [
        {"title": "TensorFlow Official Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "documentation", "hours": 15},
        {"title": "TensorFlow for Beginners – freeCodeCamp", "url": "https://www.freecodecamp.org/news/learn-tensorflow-in-one-hour/", "type": "article", "hours": 4},
    ],
    "LangChain": [
        {"title": "LangChain Official Docs", "url": "https://python.langchain.com/docs/get_started/introduction", "type": "documentation", "hours": 8},
        {"title": "Build a RAG App – Project", "url": "https://python.langchain.com/docs/use_cases/question_answering/", "type": "project", "hours": 6},
    ],
    "Hugging Face": [
        {"title": "Hugging Face NLP Course (Free)", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "type": "course", "hours": 20},
        {"title": "Hugging Face Transformers Docs", "url": "https://huggingface.co/docs/transformers/index", "type": "documentation", "hours": 10},
    ],
    "Pandas": [
        {"title": "Pandas Official 10-Minute Guide", "url": "https://pandas.pydata.org/docs/user_guide/10min.html", "type": "documentation", "hours": 2},
        {"title": "Kaggle Learn – Pandas", "url": "https://www.kaggle.com/learn/pandas", "type": "course", "hours": 4},
    ],
    "NumPy": [
        {"title": "NumPy Official Quickstart", "url": "https://numpy.org/doc/stable/user/quickstart.html", "type": "documentation", "hours": 3},
        {"title": "NumPy Illustrated – freeCodeCamp", "url": "https://www.freecodecamp.org/news/numpy-python-tutorial/", "type": "article", "hours": 3},
    ],

    # ── DEVOPS / CLOUD ────────────────────────────────────────────────
    "Docker": [
        {"title": "Docker Get Started", "url": "https://docs.docker.com/get-started/", "type": "documentation", "hours": 4},
        {"title": "Dockerize a Python App", "url": "https://docs.docker.com/language/python/", "type": "project", "hours": 3},
        {"title": "Docker Compose for Django + PostgreSQL", "url": "https://docs.docker.com/samples/django/", "type": "project", "hours": 4},
    ],
    "Kubernetes": [
        {"title": "Kubernetes Official Tutorial", "url": "https://kubernetes.io/docs/tutorials/", "type": "documentation", "hours": 8},
        {"title": "Deploy a Django App on Kubernetes", "url": "https://testdriven.io/blog/django-kubernetes/", "type": "project", "hours": 10},
    ],
    "CI/CD": [
        {"title": "GitHub Actions Official Docs", "url": "https://docs.github.com/en/actions", "type": "documentation", "hours": 5},
        {"title": "CI/CD for Django – Practical Guide", "url": "https://testdriven.io/blog/django-github-actions/", "type": "project", "hours": 4},
    ],
    "AWS": [
        {"title": "AWS Free Tier – Hands-on Labs", "url": "https://aws.amazon.com/free/", "type": "project", "hours": 10},
        {"title": "AWS Cloud Practitioner Essentials", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "type": "course", "hours": 6},
    ],
    "Linux": [
        {"title": "The Linux Command Line – Free Book", "url": "https://linuxcommand.org/tlcl.php", "type": "book", "hours": 15},
        {"title": "Linux Basics for Hackers – Overview", "url": "https://www.freecodecamp.org/news/the-linux-commands-handbook/", "type": "article", "hours": 5},
    ],
}




def get_resources_for_skill(skill: str, score: float = 0.0, top_k: int = 3) -> list[dict]:
    """
    Return tier-appropriate resources based on the candidate's score.
      - Novice       (score < 2.0) : 1 resource  — foundational tutorial only
      - Intermediate (score < 3.0) : 2 resources — tutorial + practice project
      - Approaching  (score < 3.5) : all top_k   — full depth needed
    Resources in _RESOURCES are ordered beginner → advanced, so slicing by count works.
    """
    resources = _RESOURCES.get(skill, [])
    if not resources:
        # Fuzzy fallback: try case-insensitive match
        skill_lower = skill.lower()
        for key, value in _RESOURCES.items():
            if skill_lower in key.lower() or key.lower() in skill_lower:
                resources = value
                break

    # Pick tier count based on score
    if score < 2.0:
        count = 1        # Novice — just the beginner resource
    elif score < 3.0:
        count = 2        # Intermediate — beginner + one project
    else:
        count = top_k    # Approaching advanced — full set

    return resources[:count]


def get_semantic_similarity(answer: str, skill: str,
                             target_text: str = "") -> float:
    """
    Compute cosine similarity between the candidate's answer and a reference text.

    If target_text is provided (from the intent extractor), it is used as the
    comparison target instead of the generic gold-standard answer. This makes
    scoring question-specific.

    Falls back to the skill's gold-standard answer if no target_text is given.
    Returns a score in [0.0, 1.0].
    """
    # Prefer question-derived target over generic gold standard
    gold = target_text if target_text else _GOLD_ANSWERS.get(skill, "")
    if not gold or not answer.strip():
        return 0.5  # neutral score if no reference exists

    try:
        model = _get_model()
        embeddings = model.encode([answer, gold], normalize_embeddings=True)
        # Cosine similarity = dot product of normalised vectors
        raw_sim = float(np.dot(embeddings[0], embeddings[1]))

        # ── Rescale raw cosine to a proficiency score ────────────────────────
        # Sentence-transformers cosine similarity has a practical range of
        # ~[0.2, 0.8] for technical text:
        #   0.2  = unrelated topic          → proficiency 0.0
        #   0.45 = on-topic but shallow     → proficiency ~0.4
        #   0.60 = strong relevant answer   → proficiency ~0.7
        #   0.75 = near-perfect coverage    → proficiency ~1.0
        #   0.80+= paraphrase-level         → proficiency 1.0
        #
        # Raw cosine fed directly as 0-1 permanently caps expert answers at
        # ~0.65, making it impossible to score above 3.5/5.
        FLOOR = 0.20   # below this = completely unrelated
        CEIL  = 0.75   # above this = treat as perfect match
        rescaled = (raw_sim - FLOOR) / (CEIL - FLOOR)

        return round(max(0.0, min(1.0, rescaled)), 3)
    except Exception:
        return 0.5  # graceful fallback

