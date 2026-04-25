import math

def retrieval_evaluator(results, dataset, k=5):
    """
    Computes Recall@k, Precision@k, MRR, and nDCG.

    Args:
        results: list of dicts with "retrieved_docs" (each doc has "id")
        dataset: list with "relevant_doc_ids"
        k: cutoff

    Returns:
        dict of metrics
    """

    total_recall = 0
    total_precision = 0
    total_mrr = 0
    total_ndcg = 0

    n = len(results)

    for result, example in zip(results, dataset):
        retrieved = result.get("retrieved_docs", [])[:k]
        retrieved_ids = [doc["id"] for doc in retrieved]

        relevant = set(example.get("relevant_doc_ids", []))

        if not relevant:
            continue

        # ---- Recall@k ----
        hits = sum(1 for doc_id in retrieved_ids if doc_id in relevant)
        recall = hits / len(relevant)

        # ---- Precision@k ----
        precision = hits / k

        # ---- MRR ----
        rr = 0
        for rank, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in relevant:
                rr = 1 / rank
                break

        # ---- nDCG ----
        dcg = 0
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant:
                dcg += 1 / math.log2(i + 2)

        # Ideal DCG
        ideal_hits = min(len(relevant), k)
        idcg = sum(1 / math.log2(i + 2) for i in range(ideal_hits))

        ndcg = dcg / idcg if idcg > 0 else 0

        total_recall += recall
        total_precision += precision
        total_mrr += rr
        total_ndcg += ndcg

    return {
        f"recall@{k}": (total_recall / n) * 100 if n else 0,
        f"precision@{k}": (total_precision / n) * 100 if n else 0,
        "MRR": (total_mrr / n) * 100 if n else 0,
        "nDCG": (total_ndcg / n) * 100 if n else 0,
    }