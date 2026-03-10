from retrieval.hybrid_search import hybrid_search

results = hybrid_search("What regulations apply to electronic waste?")

for r in results:
    print(r[:200])
