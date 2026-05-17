"""
Intent Extractor
─────────────────
Deterministically parses an interview question to extract the expected
technical concepts the answer should contain.

Design principles:
  - Zero LLM calls — pure string matching and phrase lookup
  - Output is used to replace the generic gold-standard in scoring
  - Confidence tells the scoring engine whether to call LLM as fallback
"""

from __future__ import annotations
import re


# ─────────────────────────────────────────────────────────────────────────────
# INTENT MAP
# Each entry: (trigger_phrase_regex, reference_sentence, [expected_keywords])
# Phrases are matched case-insensitively against the interview question.
# ─────────────────────────────────────────────────────────────────────────────
_INTENT_MAP: list[tuple[str, str, list[str]]] = [

    # ── STATE MANAGEMENT / REDUX ──────────────────────────────────────────────
    (r"set.{0,10}up.{0,15}redux|manage.{0,15}redux|redux.{0,15}manage",
     "I would set up a Redux store using configureStore from Redux Toolkit, create feature slices with createSlice for each domain, and use useSelector and useDispatch hooks in components to read and update state predictably.",
     ["configureStore", "createSlice", "useSelector", "useDispatch", "store", "reducer", "slice"]),

    (r"filter.{0,20}redux|redux.{0,20}filter|product.{0,20}filter",
     "I would store the active filters in a dedicated slice and dispatch actions when the user changes them, then derive the filtered results using a memoized selector with createSelector.",
     ["filter", "createSelector", "memoized", "selector", "dispatch", "slice"]),

    (r"recently.{0,10}viewed|view.{0,10}history",
     "I would maintain a capped array of recently viewed item IDs in the Redux store, deduplicating on insert and persisting to localStorage with redux-persist.",
     ["recentlyViewed", "localStorage", "redux-persist", "dedupe", "persist"]),

    (r"normaliz|entities|lookup",
     "I would normalize the data into an entities object keyed by ID so that both the product grid and the recently viewed section reference the same objects without duplication.",
     ["entities", "normalize", "byId", "ids", "lookup", "denormalize"]),

    # Loading state — framework-neutral keywords that work for both
    # React (loading=true, spinner) and Redux (status='loading', isLoading)
    (r"loading.{0,30}state|spinner|while.{0,15}loading|loading.{0,20}indicator",
     "I track loading state with a boolean or status field. While loading, I show a spinner and disable submit actions. On completion I update the UI with data or an error.",
     ["loading", "spinner", "isLoading", "status", "disabled", "indicator", "true", "false"]),

    # React useState / useEffect hook-based state pattern
    (r"usestate|useeffect|functional.{0,15}component.{0,20}state|hook.{0,20}state|react.{0,20}state",
     "I use useState for local state and useEffect for side effects like data fetching. I destructure state as [value, setValue] and put async calls inside useEffect with a cleanup function.",
     ["useState", "useEffect", "loading", "error", "data", "cleanup", "deps", "async", "fetch", "conditional"]),

    (r"error.{0,30}state|api.{0,20}fail|call.{0,10}fail",
     "I would handle failures by catching the error in a rejected thunk and storing the error message in the state to display an error banner to the user.",
     ["error", "failed", "rejected", "catch", "error message"]),

    (r"api.{0,20}request.{0,20}lifecycle|request lifecycle|pending.{0,20}fulfilled|createAsyncThunk|extraReducers",
     "I would use Redux Toolkit's createAsyncThunk, which automatically dispatches pending, fulfilled, and rejected actions that I can handle in extraReducers.",
     ["pending", "fulfilled", "rejected", "createAsyncThunk", "extraReducers"]),

    # General async API call — pure JS keywords, NO Redux-specific terms
    # (createAsyncThunk / thunk are in the Redux-specific pattern above)
    (r"async.{0,20}api|fetch.{0,20}api|api.{0,20}call",
     "I would handle the asynchronous API call using async/await inside a try/catch block, dispatching to update state on success or failure.",
     ["async", "await", "fetch", "try", "catch", "Promise", "resolve", "reject"]),

    # JavaScript parallel / multiple requests
    (r"parallel|both.{0,15}request|two.{0,15}api|both.{0,15}api|independent.{0,15}api|multiple.{0,15}api",
     "I would use Promise.all to fire both requests simultaneously, awaiting them together so neither blocks the other, then destructure the results.",
     ["Promise.all", "Promise.allSettled", "parallel", "await", "fetch", "destructure", "resolve", "allSettled"]),

    (r"throughout.{0,20}application|app.{0,10}wide|global.{0,10}state",
     "To make data accessible globally, I would configure a Redux store, provide it at the root of the app, and use useSelector to read the state in any component.",
     ["store", "useSelector", "Provider", "global state", "configureStore"]),

    (r"actions.{0,10}reducers|reducers.{0,10}actions",
     "I would use createSlice to automatically generate actions and reducers for my state, keeping the mutation logic predictable and centralized.",
     ["action", "reducer", "createSlice", "extraReducers", "dispatch"]),

    (r"store.{0,20}structure|structure.{0,20}redux|redux.{0,20}store",
     "I structure the Redux store by combining feature-based slices using configureStore, keeping related state and reducers together.",
     ["configureStore", "slice", "reducer", "middleware", "store"]),

    (r"debounce|debouncing|300.{0,5}ms|delay.{0,15}dispatch",
     "I would debounce the dispatch by keeping a timer reference in module scope or a closure, clearing it on each new call so only the final invocation after the delay period actually triggers the API request.",
     ["setTimeout", "clearTimeout", "debounce", "timer", "300ms", "closure"]),

    (r"thunk.{0,20}test|test.{0,20}thunk|jest.{0,20}thunk",
     "I would test the thunk by creating a mock store, dispatching the thunk, advancing fake timers with jest.advanceTimersByTime, and asserting the sequence of dispatched actions matches pending then fulfilled or rejected.",
     ["jest.useFakeTimers", "advanceTimersByTime", "mockStore", "getActions", "mockResolvedValue", "dispatch"]),

    (r"abort|cancel.{0,15}request|abortcontroller",
     "I would use an AbortController to cancel in-flight requests when a new one starts, passing the signal to fetch and calling controller.abort() before each new request.",
     ["AbortController", "abort", "signal", "cancel", "fetch"]),

    (r"enzyme",
     "I would use Enzyme to shallow or mount render the component wrapped in a Provider, simulate user events on the input, advance fake timers to trigger the debounce, and assert that dispatch was called once with the correct payload.",
     ["shallow", "mount", "simulate", "Provider", "wrapper", "find", "props", "state"]),

    (r"context.{0,20}test|test.{0,20}context|feature.{0,5}flag.{0,20}test|provide.{0,20}context.{0,20}value",
     "I would wrap the component in a context Provider with the desired mock value, mount it, and assert that the correct child component renders based on the flag value.",
     ["Provider", "context", "mount", "value", "flag", "wrapper", "find"]),

    # ── A/B TESTING / FEATURE FLAGS ──────────────────────────────────────────
    (r"a.{0,3}b.{0,5}test|feature.{0,5}flag|launchdarkly|optimizely|split.{0,5}test",
     "I would integrate a feature flag SDK by wrapping the app in a provider, initializing with a stable user ID for consistent bucketing, and using a hook to read flag values that determine which variant the user sees.",
     ["feature flag", "provider", "variant", "bucketing", "SDK", "userId", "flag", "A/B"]),

    (r"track.{0,20}exposure|user.{0,15}variation|consistent.{0,15}experience",
     "I would track exposure events only when the user actually sees the variant, use deterministic hashing for consistent bucketing across sessions, and implement gradual rollout with a kill switch for safety.",
     ["exposure", "track", "variation", "hash", "rollout", "kill switch", "bucketing"]),

    # ── WEBPACK ──────────────────────────────────────────────────────────────
    (r"only loaded when|not.{0,10}part of.{0,10}initial|on demand|route.{0,20}bundle",
     "I would use React.lazy with dynamic import() to split the component into a separate chunk. Wrapping it in Suspense with a fallback lets the app render immediately while the chunk loads on demand.",
     ["React.lazy", "dynamic import", "import()", "Suspense", "lazy", "code splitting", "chunk"]),

    (r"initial.{0,20}load|initial.{0,10}bundle|startup.{0,10}time",
     "To improve initial load time, I would implement route-based code splitting using React.lazy to ensure users only download the JavaScript needed for the current page.",
     ["code splitting", "lazy", "dynamic import", "chunk", "bundle size", "React.lazy"]),

    (r"development.{0,20}build|slow.{0,15}build|dev.{0,10}server",
     "To speed up development, I would configure webpack-dev-server with Hot Module Replacement (HMR) and use cheap source maps instead of full source maps.",
     ["HMR", "webpack-dev-server", "source map", "devtool", "cache", "watch mode"]),

    (r"production.{0,20}bundle|production.{0,10}build",
     "For production, I would enable tree shaking, minify the code with TerserPlugin, and use content hashes in output filenames for optimal caching.",
     ["minification", "tree shaking", "TerserPlugin", "optimization", "contenthash"]),

    (r"diagnos|slow.{0,20}load|performance.{0,20}webpack|bundle.{0,10}size",
     "To diagnose the issue, I would run webpack-bundle-analyzer to visualize chunk sizes, identifying large third-party dependencies that should be separated using SplitChunksPlugin.",
     ["webpack-bundle-analyzer", "stats", "SplitChunksPlugin", "tree shaking", "lazy"]),

    (r"code.{0,5}split",
     "I would configure Webpack's SplitChunksPlugin to separate vendor code from application code, and use dynamic imports for on-demand chunk loading.",
     ["dynamic import", "import()", "React.lazy", "SplitChunksPlugin", "chunk"]),

    (r"tree.{0,5}shak",
     "I would ensure my project uses ES modules and add the 'sideEffects' flag to package.json so Webpack can safely prune unused exports during the production build.",
     ["tree shaking", "side effects", "ES modules", "unused code", "sideEffects"]),

    (r"magic.{0,10}comment|chunk.{0,10}name|prefetch|preload",
     "I would use Webpack magic comments like /* webpackChunkName */ to name chunks for debugging, and /* webpackPrefetch */ to load likely-needed chunks in the background.",
     ["webpackChunkName", "webpackPrefetch", "webpackPreload", "magic comment"]),

    (r"multiple.{0,20}section|separate.{0,15}bundle|admin.{0,20}dashboard|distinct.{0,20}section|multi.{0,5}entry",
     "I would configure Webpack with multiple entry points for each section, use SplitChunksPlugin with cacheGroups to extract shared vendor code, enable runtimeChunk for caching, and use dynamic imports within each entry for further code splitting.",
     ["entry", "splitChunks", "cacheGroups", "runtimeChunk", "Module Federation",
      "contenthash", "dynamic import", "webpack-bundle-analyzer"]),


    # ── TESTING ───────────────────────────────────────────────────────────────
    (r"integration.{0,10}test|integration.{0,5}testing",
     "For integration testing, I render the component wrapped in a Provider with a test store, and simulate user interactions using React Testing Library while verifying DOM updates.",
     ["render", "screen", "Provider", "store", "waitFor", "findByText"]),

    (r"mock.{0,15}api|mock.{0,10}fetch|control.{0,20}api",
     "I would use jest.mock or MSW to intercept API calls and return mocked resolved or rejected promises, preventing real network requests and ensuring stable tests.",
     ["jest.mock", "mockResolvedValue", "mockRejectedValue", "msw", "spy"]),

    (r"test.{0,20}loading.{0,20}state|loading.{0,20}test",
     "To test the loading state, I assert that a spinner is in the document immediately after rendering, then use a waitFor or findBy query to wait for it to disappear.",
     ["waitFor", "findBy", "loading", "spinner", "async", "findByText"]),

    (r"test.{0,20}error.{0,20}state|error.{0,20}test",
     "To test the error state, I mock the API to return a rejected promise and verify that the expected error message appears in the document.",
     ["mockRejectedValue", "findByText", "error", "rejects", "waitFor"]),

    (r"filter.{0,20}test|test.{0,20}filter|dropdown.{0,20}test",
     "I would use userEvent to interact with the dropdown, selecting a specific category, and then assert that only the filtered items remain in the document.",
     ["userEvent", "selectOptions", "findByText", "queryByText", "waitFor"]),

    (r"snapshot.{0,10}test",
     "I would use Jest's toMatchSnapshot to ensure the UI does not change unexpectedly, storing the component's rendered output as a baseline for future comparisons.",
     ["toMatchSnapshot", "snapshot", "serializer", "toMatchInlineSnapshot"]),

    # ── REACT ─────────────────────────────────────────────────────────────────
    (r"lazy.{0,5}load|route.{0,20}lazy|dynamic.{0,10}import",
     "I implement lazy loading using React.lazy and dynamic imports, paired with a Suspense component to provide a fallback UI while the chunk downloads.",
     ["React.lazy", "Suspense", "dynamic import", "import()", "fallback"]),

    (r"performance.{0,20}react|re.{0,5}render|unnecessary.{0,15}render",
     "I optimize performance by using useMemo to cache expensive calculations and React.memo to prevent unnecessary re-renders of child components when their props haven't changed.",
     ["useMemo", "useCallback", "React.memo", "virtualization", "re-render"]),

    (r"context.{0,10}api|prop.{0,5}drill",
     "I use the Context API to pass global data down the component tree without prop drilling, creating a Provider at the top and consuming it with useContext.",
     ["createContext", "useContext", "Provider", "Consumer", "Context"]),

    (r"custom.{0,10}hook",
     "I would extract the reusable logic into a custom hook, utilizing standard React hooks like useState and useEffect inside it to manage local state and side effects.",
     ["useState", "useEffect", "useRef", "custom hook", "reusable logic"]),

    # ── ASYNC / GENERAL ───────────────────────────────────────────────────────
    (r"promise|async.{0,10}await|asynchronous",
     "I would use async/await for clear asynchronous flow, wrapping the logic in a try/catch block to properly handle promise rejections.",
     ["async", "await", "Promise", "then", "catch", "finally"]),

    (r"race.{0,10}condition|concurrent|parallel",
     "To prevent race conditions, I would use an AbortController to cancel previous requests or track a boolean flag inside the useEffect cleanup function.",
     ["AbortController", "race", "cancel", "cleanup", "useEffect cleanup"]),

    # ── SERVICE WORKER / PWA ──────────────────────────────────────────────────
    (r"service.{0,10}worker|pwa|offline",
     "I configure a service worker to precache static assets during the install event and serve them from the cache for offline support.",
     ["service worker", "cache", "skipWaiting", "clients.claim", "install", "activate"]),

    (r"stale.{0,10}content|update.{0,20}pwa|new.{0,10}version",
     "To avoid stale content, I would prompt the user to reload when an update is found, and then call skipWaiting to activate the new service worker.",
     ["skipWaiting", "SKIP_WAITING", "updatefound", "controllerchange", "cache version"]),

    # ── DATABASE / BACKEND ────────────────────────────────────────────────────
    (r"n\+1|n plus 1|query.{0,20}optimiz",
     "To fix the N+1 problem, I would use eager loading techniques like JOINs in SQL or tools like DataLoader in GraphQL to batch queries.",
     ["select_related", "prefetch_related", "DataLoader", "JOIN", "eager loading"]),

    (r"transaction|acid|rollback",
     "I would wrap the operations in a database transaction, committing them if successful or rolling back the entire transaction if an error occurs to maintain ACID properties.",
     ["transaction", "commit", "rollback", "ACID", "isolation level"]),

    (r"index|slow.{0,10}query|query.{0,10}optimiz",
     "To optimize the slow query, I would use EXPLAIN to analyze the query plan and add a composite index covering the columns used in the WHERE and ORDER BY clauses.",
     ["INDEX", "EXPLAIN", "composite index", "query plan", "covering index"]),

    # ── REDIS ─────────────────────────────────────────────────────────────────
    (r"redis|cache.{0,20}latency|response.{0,15}time.{0,20}redis|cache.{0,20}strategy",
     "I implement a cache-aside strategy with Redis: check Redis first on each request, return immediately on hit. On miss, query the database, write back with SETEX and a TTL, and invalidate on writes.",
     ["cache-aside", "HASH", "STRING", "TTL", "SETEX", "HGETALL", "HGET", "cache", "invalidate", "SETNX"]),

    (r"cache.{0,20}stampede|hot.{0,10}key|cache.{0,20}evict",
     "To prevent cache stampedes when a hot key expires, I use SETNX to set a distributed lock so only one request rebuilds the cache while others wait or serve stale data.",
     ["SETNX", "lock", "stampede", "TTL", "stale", "eviction", "hot key"]),

    (r"redis.{0,20}data.{0,10}struct|hash.{0,15}string.{0,15}redis|which.{0,15}redis",
     "I choose HASH when I need partial field reads or incremental updates via HGET and HSET. I choose STRING for profiles consumed as a whole, storing JSON for simplicity.",
     ["HASH", "STRING", "HGET", "HSET", "HGETALL", "JSON", "partial", "SETEX"]),

    # ── ADVANCED SQL ──────────────────────────────────────────────────────────
    (r"slow.{0,20}batch|over.{0,10}hour|taking.{0,15}long|sql.{0,20}slow|report.{0,20}slow",
     "I diagnose with EXPLAIN ANALYZE and pg_stat_statements to find full table scans, then fix with composite indexes, date-based partitioning, CTEs, and materialized views.",
     ["EXPLAIN ANALYZE", "pg_stat_statements", "composite index", "partition", "CTE",
      "materialized view", "partial index", "covering index", "full table scan", "ANALYZE"]),

    (r"diagnos.{0,20}slow|execution.{0,10}plan|explain.{0,10}analyze",
     "I use EXPLAIN ANALYZE to see the execution plan, identify sequential scans and bad join orders, then add indexes and rewrite queries to use partition pruning.",
     ["EXPLAIN ANALYZE", "execution plan", "sequential scan", "index scan", "partition pruning",
      "pg_stat_statements", "wait events", "ANALYZE"]),

    (r"partition.{0,20}table|table.{0,20}partition|date.{0,15}partition",
     "I partition large tables by date so queries hit only the relevant partition, turning a full scan of millions of rows into a targeted scan of one day's partition.",
     ["partition", "partition pruning", "date partition", "PARTITION BY", "monthly", "daily"]),

    (r"materialized.{0,10}view|precompute|summary.{0,10}table|incremental.{0,10}refresh",
     "I precompute expensive aggregations into a materialized view or summary table and refresh it incrementally so reports read thousands of rows instead of millions.",
     ["materialized view", "precompute", "summary table", "incremental refresh", "REFRESH MATERIALIZED VIEW"]),

    # ── DATABASE DESIGN ───────────────────────────────────────────────────────
    (r"product.{0,20}attrib|diverse.{0,20}attrib|flexible.{0,20}schema|vary.{0,20}attrib",
     "I use a hybrid approach: a core relational table for shared fields, and a JSONB column for diverse per-product attributes, using GIN indexes for query performance.",
     ["JSONB", "GIN", "hybrid", "normalization", "EAV", "schema", "attribute", "trade-off", "GIN index"]),

    (r"schema.{0,20}design|model.{0,20}database|database.{0,20}schema|erd|entity.{0,20}relation",
     "I design the schema around query patterns: normalized core tables with foreign keys, indexes on filter columns, and JSONB for flexible or sparse attributes.",
     ["normalization", "foreign key", "primary key", "ERD", "index", "schema", "constraint",
      "JSONB", "denormalization", "1NF", "3NF"]),

    (r"eav|entity.{0,10}attribute|flexible.{0,20}attrib|sparse.{0,10}column",
     "EAV is maximally flexible but causes join hell at scale. I prefer JSONB for flexibility with GIN indexes for querying, promoting high-frequency attributes to real columns.",
     ["EAV", "JSONB", "GIN", "sparse", "flexible", "promote", "join", "schema"]),

    # ── ETL PIPELINES ─────────────────────────────────────────────────────────
    (r"etl|extract.{0,10}transform.{0,10}load|data.{0,10}pipeline|data.{0,20}warehouse",
     "I build idempotent ETL pipelines that extract with high-watermark queries, validate row counts at each stage, load with upserts keyed on business keys, and alert on quality failures.",
     ["extract", "transform", "load", "idempotent", "upsert", "watermark", "row count",
      "reconciliation", "data quality", "MERGE", "stale", "assertion"]),

    (r"stale.{0,20}data|inconsistent.{0,20}data|stale.{0,20}report|dashboard.{0,20}wrong",
     "I trace stale data by comparing extract timestamps, checking row counts at each stage, and validating warehouse totals against source totals for the same business date.",
     ["stale", "reconciliation", "row count", "watermark", "late data", "idempotent",
      "freshness", "max(load_date)", "assertion", "timestamp"]),

    (r"data.{0,10}quality|idempoten|upsert|dedup|duplicate.{0,10}load",
     "I enforce data quality by adding count and sum assertions that fail the job on anomalies, using upserts with MERGE keyed on natural business keys, and tracking high-watermark for incremental loads.",
     ["data quality", "assertion", "upsert", "MERGE", "idempotent", "dedup", "natural key",
      "watermark", "incremental", "duplicate"]),

    # ── AZURE ─────────────────────────────────────────────────────────────────
    (r"azure|azure.{0,10}sql|azure.{0,10}data.{0,10}factory|blob.{0,10}storage",
     "I provision Azure SQL Database for managed relational storage, use Azure Data Factory for pipeline orchestration, store raw files in Blob Storage, and secure everything with managed identities.",
     ["Azure SQL", "Data Factory", "Blob Storage", "managed identity", "Key Vault",
      "Application Insights", "AKS", "resource group", "pipeline", "trigger"]),

    (r"azure.{0,20}deploy|azure.{0,20}devops|azure.{0,20}pipeline",
     "I set up CI/CD with Azure DevOps pipelines, deploy infrastructure with ARM templates or Bicep, and monitor with Application Insights dashboards and alerts.",
     ["Azure DevOps", "CI/CD", "ARM template", "Bicep", "Application Insights",
      "pipeline", "release", "artifact", "monitoring"]),
]


def extract_intent(question: str, skill: str) -> dict:
    """
    Parse the interview question and return expected answer concepts.

    Returns:
        target_text  : str  — synthesised reference text for semantic comparison
        keywords     : list — technical terms the answer should contain
        confidence   : float 0.0-1.0 — how well we understood the question
                       (low confidence → caller should invoke LLM as fallback)
    """
    q_lower = question.lower()
    matched_sentences: list[str] = []
    matched_concepts: list[str] = []

    for pattern, sentence, concepts in _INTENT_MAP:
        if re.search(pattern, q_lower):
            matched_sentences.append(sentence)
            for c in concepts:
                if c not in matched_concepts:
                    matched_concepts.append(c)

    if not matched_sentences:
        return {"target_text": "", "keywords": [], "confidence": 0.0}

    # If we hit ANY triggers, we are highly confident we know the scenario.
    confidence = 1.0

    # Combine all matched reference sentences into a single target string
    target_text = " ".join(matched_sentences)

    return {
        "target_text": target_text,
        "keywords": matched_concepts,
        "confidence": round(confidence, 2),
    }
