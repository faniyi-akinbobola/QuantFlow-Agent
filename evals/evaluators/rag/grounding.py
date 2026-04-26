import re
from openai import OpenAI


def grounding_evaluator_llm(examples):
    """
    Evaluates whether the answer is grounded in the retrieved context.

    Args:
        examples (list): Each example should contain:
            - question (str)
            - answer (str)
            - context (str)

    Returns:
        float: Grounding score (0–100)
    """
    
    client = OpenAI()
    scores = []

    for example in examples:
        question = example["question"]
        answer = example["answer"]
        context = example.get("context", "")

        PROMPT = f"""
You are a strict financial evaluator.

Your job is to determine whether the answer is grounded in the provided context.

Definition:
- Grounded answer: The answer clearly uses and relies on the provided context.
- Ungrounded answer: The answer ignores the context or relies mostly on outside/general knowledge.

Important:
- The answer does NOT need to copy the context exactly.
- Paraphrasing is allowed.
- If the answer could have been written WITHOUT the context, return 0.

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
            temperature=0.3,  # Increased from 0 for more lenient judging
            messages=[{"role": "user", "content": PROMPT}]
        )

        output = response.choices[0].message.content.strip()

        match = re.search(r"score:\s*(\d)", output.lower())
        score = int(match.group(1)) if match else 0

        scores.append(score)

    return (sum(scores) / len(scores)) * 100 if scores else 0