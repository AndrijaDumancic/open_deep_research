import asyncio
import os
import sys

# Add src to path so we can import the module
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Load env vars before importing logic that might use them
from dotenv import load_dotenv
load_dotenv()

from open_deep_research.deep_researcher import deep_researcher
from langchain_core.messages import HumanMessage
question1 = "What are the main differences between Python 3.12 and 3.13?"
question2 = "I want technical comparison with code examples."
async def main():
    # 1. Define a simple query
    initial_state = {
        "messages": [
            HumanMessage(content=question1),
        ]
    }

    print("🚀 Starting research agent with LiteLLM...")

    # 2. Run the graph
    async for event in deep_researcher.astream(initial_state, stream_mode="values"):
        # Print the last message from the latest step
        if "messages" in event and event["messages"]:
            last_msg = event["messages"][-1]
            # Print just a snippet to keep console clean
            content_snippet = str(last_msg.content)[:200].replace('\n', ' ')
            print(f"\n[{last_msg.type.upper()}]: {content_snippet}...")

        # If we have a final report, print it!
        if "final_report" in event and event["final_report"]:
            print("\n\n✅ FINAL REPORT GENERATED:")
            print("="*60)
            print(event["final_report"])
            print("="*60)
            break # Exit loop once done

if __name__ == "__main__":
    asyncio.run(main())