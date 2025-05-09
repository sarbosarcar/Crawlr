import os
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from typing import Optional, Dict, Any, List
import trafilatura
import requests

load_dotenv()
TAVILY: Optional[str] = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")

class SearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Searches the web for recent and relevant information."

    def _run(self, input_data: Dict[str, Any]) -> str:
        if isinstance(input_data.get("query"), dict):
            query = list(input_data["query"].keys())[0]
        elif isinstance(input_data.get("query"), str):
            query = input_data["query"]
        elif isinstance(input_data.get("description"), str):
            query = input_data["description"]
        else:
            return "⚠️ Invalid input. No query provided."

        if not isinstance(query, str) or not query.strip():
            return "⚠️ Query must be a non-empty string."

        try:
            if not TAVILY:
                raise ValueError("Tavily API key not found")

            tav = TavilyClient(api_key=TAVILY)
            result = tav.search(
                query=query,
                max_results=5,
                search_depth="advanced"
            )
            links = [item['url'] for item in result['results'][:5]]
            return "\n".join(links)
        except Exception as e:
            return f"⚠️ Search failed. Error: {str(e)}"

def fetch_and_format_content(urls: List[str]) -> str:
    output = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                extracted = trafilatura.extract(response.text)
                formatted = (extracted[:1024] if extracted else "")
                output.append(f"## Source: {url}\n\n{formatted}\n")
        except Exception as e:
            output.append(f"## Source: {url}\n\n⚠️ Failed to fetch: {str(e)}\n")
    return "\n---\n".join(output)

def set_llm() -> ChatOpenAI:
    if not GROQ_API_KEY:
        raise ValueError("Groq API key not found")

    return ChatOpenAI(
        model="groq/gemma2-9b-it",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.5,
        max_tokens=1024
    )

def form_crew(query: str) -> Crew:
    llm = set_llm()

    search_agent = Agent(
        role="Web Search Agent",
        goal="Fetch relevant URLs from the web",
        backstory="Expert at finding recent data sources online.",
        tools=[SearchTool()],
        llm=llm,
        verbose=True
    )

    parser_agent = Agent(
        role="Content Extractor",
        goal="Extract and format readable content from webpages",
        backstory="Skilled at parsing raw HTML and cleaning it for analysis.",
        llm=llm,
        verbose=True
    )

    answer_agent = Agent(
        role="Research Synthesizer",
        goal="Answer the user query using only the parsed content",
        backstory="Synthesizes answers strictly from formatted web data.",
        llm=llm,
        verbose=True
    )

    search_task = Task(
        description=(
            f"User query: {query}\nFind 3–5 high-quality URLs with relevant information."
        ),
        expected_output="List of 3–5 URLs, newline-separated.",
        agent=search_agent,
        output_file="search_output.md"
    )

    def parsing_task_func(inputs):
        urls = inputs["search_task"].split("\n")
        formatted_content = fetch_and_format_content(urls)
        with open("context_output.md", "w") as f:
            f.write(formatted_content)
        return formatted_content

    context_task = Task(
        description="Parse content from URLs and format it using Trafilatura.",
        expected_output="Formatted readable content from the URLs.",
        agent=parser_agent,
        context=[search_task],
        output_func=parsing_task_func,
        output_file="context_output.md"
    )

    final_task = Task(
        description=(
            f"""User query: '{query}'
Using ONLY the following context, generate the most relevant answer."""
        ),
        expected_output="Final answer tailored to the query, using formatted context only.",
        context=[context_task],
        output_file="research_output.md",
        agent=answer_agent
    )

    return Crew(
        agents=[search_agent, parser_agent, answer_agent],
        tasks=[search_task, context_task, final_task],
        verbose=True,
        process="sequential"
    )

def main() -> None:
    print("🤖 AI Research Assistant (Ctrl+C or 'exit' to stop)\n")
    while True:
        try:
            query = input("🔎 What would you like to research? ")
            if query.strip().lower() in ['exit', 'quit']:
                break

            print("\n🧠 Researching... please wait...\n")
            crew = form_crew(query)
            result = crew.kickoff()

            print("\n✅ Research Result:\n")
            print(result)

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()