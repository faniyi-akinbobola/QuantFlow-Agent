import re
from openai import OpenAI


def reasoning_quality_evaluator_llm(examples):
    """
    Evaluates the quality of reasoning in the answer.

    Args:
        examples (list): Each example should contain:
            - question (str)
            - answer (str)

    Returns:
        float: Reasoning quality score (0–100)
    """
    
    client = OpenAI()
    scores = []

    for example in examples:
        question = example["question"]
        answer = example["answer"]

        PROMPT = f"""You are a strict financial evaluator.

Your job is to determine the quality of reasoning in the answer.

Definition:
- High-quality reasoning: The answer demonstrates logical, coherent, and well-structured reasoning.
- Low-quality reasoning: The answer lacks logical flow, coherence, or structure.

Important:
- Focus on the reasoning process, not just the correctness of the answer.
- If the answer shows clear and logical reasoning, return 1.
- If the answer shows poor or no reasoning, return 0.

---

Question:
{question}

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
            temperature=0,
            messages=[{"role": "user", "content": PROMPT}]
        )

        output = response.choices[0].message.content.strip()

        match = re.search(r"score:\s*(\d)", output.lower())
        score = int(match.group(1)) if match else 0

        scores.append(score)

    return (sum(scores) / len(scores)) * 100 if scores else 0