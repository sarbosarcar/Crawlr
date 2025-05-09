import os
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from typing import Optional, Dict, Any


load_dotenv()
TAVILY: Optional[str] = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")


class SearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = "Searches the web for recent and relevant information."

    def _run(self, query: str) -> str:
        try:
            if not TAVILY:
                raise ValueError("Tavily API key not found")
                
            tav = TavilyClient(api_key=TAVILY)
            result = tav.search(
                query=query,
                include_answers=True,
                max_results=5,
                search_depth="advanced"
            )
            links = [f"{i+1}. {item['title']}\n   {item['url']}"
                    for i, item in enumerate(result['results'][:3])]
            answer = result.get('answer', 'I found these resources:')
            return f"{answer}\n\nTop Links:\n" + "\n\n".join(links)
        except Exception as e:
            return f"⚠️ Search failed. Error: {str(e)}"


def set_llm() -> ChatOpenAI:
    if not GROQ_API_KEY:
        raise ValueError("Groq API key not found")
    
    return ChatOpenAI(
        model="groq/llama3-70b-8192", 
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.5,
        max_tokens=1024
    )


def form_crew(query: str) -> Crew:
    llm = set_llm()
    researcher = Agent(
        role="AI Research Specialist",
        goal="Deliver precise and informative answers with credible sources",
        backstory=(
            "You're an elite researcher who uses advanced tools to find and "
            "synthesize information from verified web sources."
        ),
        tools=[SearchTool()],
        llm=llm,
        verbose=True,
        max_iter=3
    )

    task = Task(
        description=(
            f"Research the topic: '{query}'\n"
            "Instructions:\n"
            "- Only use verified, recent information\n"
            "- Present a clear and concise comparison\n"
            "- Highlight key differences in specs, features, and price\n"
            "- Provide 3–5 relevant sources with titles and URLs"
        ),
        expected_output=(
            "1. Overview of both products\n"
            "2. Key specifications comparison (table format)\n"
            "3. Feature comparison\n"
            "4. Price comparison\n"
            "5. Buying recommendation\n"
            "6. 3–5 Reference links with titles"
        ),
        agent=researcher,
        output_file="research_output.md"
    )

    return Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True,
        process="sequential"
    )

# ------------------- Main Runner -------------------
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