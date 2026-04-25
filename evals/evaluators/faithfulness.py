import re 
from openai import OpenAI


def faithfulness_evaluator_llm(examples):
    """
    Evaluates whether answers are grounded in retrieved context (no hallucinations).
    
    Args:
        examples (list): Each example should contain:
            - question
            - answer
            - context (retrieved documents)

    Returns:
        float: Faithfulness score (0–100)
    """
    
    client = OpenAI()
    scores = []

    for example in examples:
        question = example["question"]
        answer = example["answer"]
        context = example.get("context", "")

        PROMPT = f"""    
You are a strict financial evaluator.

Your job is to determine whether the answer is fully supported by the provided context.

Definitions:
- Faithful answer: All claims in the answer are directly supported by the context.
- Unfaithful answer: Contains information NOT present in the context (hallucination).

Be conservative:
If even a small part of the answer is unsupported, return 0.

---

Question:
{question}

Context:
{context}

Answer:
{answer}

---

Return ONLY in this format:
score: 1
or
score: 0
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": PROMPT}],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        match = re.search(r'score:\s*(\d)', output.lower())
        score = int(match.group(1)) if match else 0
        scores.append(score)

    return sum(scores) / len(scores) * 100 if scores else 0