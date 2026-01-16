---
name: Prompting Patterns
description: Comprehensive guide to effective prompt engineering patterns including few-shot, chain-of-thought, ReAct, and advanced prompting techniques
---

# Prompting Patterns

## Core Patterns

### Zero-Shot
```
Prompt: "Translate to French: Hello, how are you?"
Response: "Bonjour, comment allez-vous?"

Use: Simple, well-defined tasks
```

### Few-Shot
```
Prompt:
"Translate to French:
English: Hello → French: Bonjour
English: Goodbye → French: Au revoir
English: Thank you → French: Merci
English: How are you? → French:"

Response: "Comment allez-vous?"

Use: Complex tasks, specific formats
```

### Chain-of-Thought (CoT)
```
Prompt:
"Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. 
Each can has 3 tennis balls. How many tennis balls does he have now?

A: Let's think step by step.
Roger started with 5 balls.
2 cans × 3 balls = 6 balls
5 + 6 = 11 balls
Answer: 11"

Use: Reasoning, math, complex logic
```

### Self-Consistency
```
# Generate multiple reasoning paths
prompts = [same_question] * 5
responses = [llm.generate(p) for p in prompts]

# Take majority vote
answer = most_common([extract_answer(r) for r in responses])

Use: Improve accuracy on reasoning tasks
```

---

## Advanced Patterns

### ReAct (Reasoning + Acting)
```
Prompt:
"Question: What is the capital of the country where the Eiffel Tower is located?

Thought: I need to find where the Eiffel Tower is located first.
Action: search[Eiffel Tower location]
Observation: The Eiffel Tower is in Paris, France.

Thought: Now I need to find the capital of France.
Action: search[capital of France]
Observation: Paris is the capital of France.

Thought: I now know the answer.
Answer: Paris"

Use: Multi-step reasoning with tool use
```

### Tree of Thoughts (ToT)
```
# Explore multiple reasoning paths
def tree_of_thoughts(question, depth=3):
    # Generate multiple thoughts
    thoughts = llm.generate_multiple(f"Possible approaches to: {question}")
    
    # Evaluate each thought
    scores = [evaluate_thought(t) for t in thoughts]
    
    # Expand best thoughts
    best = thoughts[argmax(scores)]
    
    if depth == 0:
        return best
    else:
        return tree_of_thoughts(best, depth-1)

Use: Complex problem-solving
```

### Self-Ask
```
Prompt:
"Question: Who was president when the iPhone was released?

Are follow-up questions needed? Yes.
Follow-up: When was the iPhone released?
Intermediate answer: 2007
Follow-up: Who was president in 2007?
Intermediate answer: George W. Bush
Final answer: George W. Bush"

Use: Questions requiring multiple facts
```

---

## Prompt Engineering Techniques

### Role Prompting
```
"You are an expert Python developer with 10 years of experience.
Write a function to reverse a string."

Use: Improve quality, set expertise level
```

### Format Specification
```
"Generate a product description in JSON format:
{
  \"name\": \"...\",
  \"description\": \"...\",
  \"price\": ...,
  \"features\": [...]
}"

Use: Structured output
```

### Constraints
```
"Write a summary in exactly 3 sentences.
Use simple language suitable for a 10-year-old.
Do not use technical jargon."

Use: Control output characteristics
```

### Examples (In-Context Learning)
```
"Classify sentiment:
'I love this!' → Positive
'This is terrible' → Negative
'It's okay' → Neutral
'Best purchase ever!' → "

Use: Classification, pattern matching
```

---

## Prompt Templates

### Question Answering
```python
template = """
Context: {context}

Question: {question}

Answer based only on the context above. If the answer is not in the context, say "I don't know."

Answer:"""

prompt = template.format(
    context=retrieved_docs,
    question=user_question
)
```

### Summarization
```python
template = """
Summarize the following text in {num_sentences} sentences:

Text: {text}

Summary:"""

prompt = template.format(
    num_sentences=3,
    text=long_text
)
```

### Code Generation
```python
template = """
Write a Python function that {description}.

Requirements:
- Include docstring
- Add type hints
- Handle edge cases
- Include example usage

Function:"""

prompt = template.format(
    description="calculates fibonacci numbers"
)
```

---

## Prompt Optimization

### Iterative Refinement
```python
# Version 1
prompt_v1 = "Translate to French: {text}"

# Test and refine
# Version 2 (more specific)
prompt_v2 = "Translate the following English text to French. Maintain formal tone: {text}"

# Version 3 (with examples)
prompt_v3 = """
Translate English to French (formal):
English: Hello → French: Bonjour
English: Thank you → French: Merci
English: {text} → French:"""
```

### A/B Testing
```python
prompts = {
    "A": "Summarize: {text}",
    "B": "Provide a concise summary of: {text}",
    "C": "In 3 sentences, summarize: {text}"
}

# Test each variant
for name, template in prompts.items():
    response = llm.generate(template.format(text=text))
    score = evaluate(response)
    print(f"{name}: {score}")
```

---

## Best Practices

### 1. Be Specific
```
Bad:  "Write about dogs"
Good: "Write a 200-word article about dog training techniques for puppies"
```

### 2. Provide Examples
```
Bad:  "Extract entities"
Good: "Extract entities:
       'John works at Google' → Person: John, Company: Google
       'Apple released iPhone' → Company: Apple, Product: iPhone
       '{text}' → "
```

### 3. Use Delimiters
```
"Summarize the text between triple quotes:
\"\"\"
{text}
\"\"\"

Summary:"
```

### 4. Specify Output Format
```
"Generate response in JSON:
{
  \"answer\": \"...\",
  \"confidence\": 0.0-1.0,
  \"sources\": [...]
}"
```

### 5. Handle Edge Cases
```
"Answer the question. If you don't know, say 'I don't know'.
If the question is unclear, ask for clarification."
```

---

## Summary

**Prompting Patterns:**
- Zero-shot (no examples)
- Few-shot (with examples)
- Chain-of-thought (reasoning)
- ReAct (reasoning + actions)

**Techniques:**
- Role prompting
- Format specification
- Constraints
- In-context learning

**Best Practices:**
- Be specific
- Provide examples
- Use delimiters
- Specify format
- Handle edge cases
