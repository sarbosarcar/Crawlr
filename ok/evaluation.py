import os
import time
from datetime import datetime
import re
from typing import List, Optional
from agent import form_crew
from evaluation_of_responses import (
    scaled_entropy, contextuality, recency, alpha,
    coherence, groundedness, readability, beta,
    gamma, omega, parse_multiple_text_blocks
)

def ensure_string(text) -> str:
    """Ensure the input is a string"""
    if isinstance(text, str):
        return text
    elif isinstance(text, list):
        return " ".join(map(str, text))
    elif text is None:
        return ""
    return str(text)

def run_full_pipeline(query: str) -> dict:
    """Run the full pipeline and return results with metrics"""
    start_time = time.time()
    
    # Validate query
    query = ensure_string(query)
    
    # Run the agent pipeline
    crew = form_crew(query)
    result = crew.kickoff()
    response = ensure_string(result)
    latency = time.time() - start_time

    # Read context from all three files
    context = ""
    files = ["context_output.md", "research_output.md", "search_output.md"]
    for file_name in files:
        try:
            with open(file_name, "r", encoding='utf-8') as f:
                context += f.read() + "\n"  # Append content from each file
        except Exception as e:
            print(f"❌ Error reading {file_name}: {e}")

    context = ensure_string(context)

    parsed_context = parse_multiple_text_blocks(context)
    dates = [extract_publication_date(source.get('content', '')) for source in parsed_context]
    dates = [d for d in dates if d is not None]

    return {
        'query': query,
        'response': response,
        'context': context,
        'dates': dates,
        'latency': latency,
        'metrics': calculate_all_metrics(query, response, context, dates, latency)
    }


def extract_publication_date(content: str) -> Optional[str]:
    """Extract publication date from content"""
    content = ensure_string(content)
    date_patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b"
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, content)
        if match:
            date_str = match.group()
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"):
                try:
                    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
    return None

def calculate_all_metrics(query: str, response: str, context: str, dates: List[str], latency: float) -> dict:
    """Calculate all evaluation metrics"""
    query = ensure_string(query)
    response = ensure_string(response)
    context = ensure_string(context)

    E = scaled_entropy(response)
    T = contextuality(query, context)
    r = recency(dates, 0.005) if dates else 0.5
    A = 0.9  # Placeholder for accuracy

    alpha_val = alpha(A, T, r)
    # Directly pass coherence result here
    C = coherence(query, response)
    G = groundedness(response, context)
    R = readability(response)
    beta_val = beta(C, G, E)
    gamma_val = gamma(latency, R)
    omega_val = omega(alpha_val, beta_val, gamma_val)

    return {
        'Basic Metrics': {
            'Scaled Entropy (E)': f"{E:.3f}",
            'Contextuality (T)': f"{T:.3f}",
            'Recency (r)': f"{r:.3f}",
            'Coherence (C)': f"{C:.3f}",  # Coherence is now directly passed
            'Groundedness (G)': f"{G:.3f}",
            'Readability (R)': f"{R:.3f}",
            'Latency (seconds)': f"{latency:.2f}"
        },
        'Composite Scores': {
            'Alpha (α = A*T*r)': f"{alpha_val:.3f}",
            'Beta (β = C*G*(1-E))': f"{beta_val:.3f}",
            'Gamma (γ = (1-exp(-L*λ))*R)': f"{gamma_val:.3f}",
            'Omega (ω = (sα+(1-s)β)^γ)': f"{omega_val:.3f}"
        }
    }

def save_to_readme(results: dict, filename: str = "EVALUATION.md"):
    """Save evaluation results in Markdown"""
    try:
        mode = 'a' if os.path.exists(filename) else 'w'
        
        with open(filename, mode, encoding='utf-8') as f:
            if mode == 'w':
                f.write("# Model Evaluation Results\n\n")
                f.write("| Metric | Description |\n")
                f.write("|--------|-------------|\n")
                f.write("| E | Scaled Entropy (0-1) |\n")
                f.write("| T | Contextuality (0-1) |\n")
                f.write("| r | Recency (0-1) |\n")
                f.write("| C | Coherence (0-1) |\n")
                f.write("| G | Groundedness (0-1) |\n")
                f.write("| R | Readability (0-1) |\n")
                f.write("| α | Alpha Score (A*T*r) |\n")
                f.write("| β | Beta Score (C*G*(1-E)) |\n")
                f.write("| γ | Gamma Score |\n")
                f.write("| ω | Omega Score |\n\n")
                f.write("---\n\n")

            f.write(f"## Query\n```\n{results['query']}\n```\n\n")
            f.write("## Response\n```\n")
            f.write(results['response'][:2000])
            if len(results['response']) > 2000:
                f.write("\n... [response truncated]")
            f.write("\n```\n\n")

            f.write("## Evaluation Metrics\n### Basic Metrics\n")
            for name, value in results['metrics']['Basic Metrics'].items():
                f.write(f"- **{name}**: {value}\n")

            f.write("\n### Composite Scores\n")
            for name, value in results['metrics']['Composite Scores'].items():
                f.write(f"- **{name}**: {value}\n")

            if results['dates']:
                f.write("\n### Source Dates\n")
                f.write(", ".join(results['dates']) + "\n")

            f.write(f"\n**Evaluation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n---\n\n")

    except Exception as e:
        print(f"❌ Error saving to README: {str(e)}")

def main():
    print("🚀 Evaluation Pipeline - Enter queries to evaluate (type 'exit' to quit)")
    
    while True:
        query = input("\n🔍 Enter your query: ").strip()
        if query.lower() in ('exit', 'quit'):
            break

        print("\n⏳ Running evaluation pipeline...")

        try:
            # Measure time for each query
            start_time = time.time()
            results = run_full_pipeline(query)
            latency = results['latency']

            save_to_readme(results)

            # Print evaluation summary and latency info
            print("\n✅ Evaluation Complete!")
            print(f"\n📋 Results saved to EVALUATION.md with this structure:")

            print(f"""
=======================================
QUERY:
{results['query'][:100]}...

RESPONSE:
{results['response'][:100]}...

METRICS:
- Basic: {', '.join([f"{k}: {v}" for k,v in results['metrics']['Basic Metrics'].items()][:3])}...
- Composite: Ω = {results['metrics']['Composite Scores']['Omega (ω = (sα+(1-s)β)^γ)']}
=======================================

Latency: {latency:.2f} seconds
Recency: {results['metrics']['Basic Metrics']['Recency (r)']}
=======================================
""")
        except Exception as e:
            print(f"\n❌ Error during evaluation: {str(e)}")

if __name__ == "__main__":
    main()
