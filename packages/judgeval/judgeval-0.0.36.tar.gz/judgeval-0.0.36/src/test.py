import os
import asyncio
from typing import TypedDict, Sequence, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from judgeval.common.tracer import Tracer
from judgeval.integrations.langgraph import JudgevalCallbackHandler, set_global_handler, clear_global_handler

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Initialize Judgment tracer
judgment = Tracer(
    api_key=os.getenv("JUDGMENT_API_KEY"),
    project_name="music-recommendation-bot",
    enable_monitoring=True  # Explicitly enable monitoring
)

# Define the state type
class State(TypedDict):
    messages: Sequence[HumanMessage | AIMessage]
    preferences: Dict[str, str]
    search_results: Dict[str, Any]
    recommendations: str
    current_question_idx: int
    questions: Sequence[str]

# Node functions
def initialize_state() -> State:
    """Initialize the state with questions and predefined answers."""
    questions = [
        "What are some of your favorite artists or bands?",
        "What genres of music do you enjoy the most?",
        "Do you have any favorite songs currently?",
        "Are there any moods or themes you're looking for in new music?",
        "Do you prefer newer releases or classic songs?"
    ]
    
    # Predefined answers for testing
    answers = [
        "Taylor Swift, The Beatles, and Ed Sheeran",
        "Pop, Rock, and Folk",
        "Anti-Hero, Hey Jude, and Perfect",
        "Upbeat and energetic music for workouts",
        "I enjoy both new and classic songs"
    ]
    
    # Initialize messages with questions and answers alternating
    messages = []
    for question, answer in zip(questions, answers):
        messages.append(HumanMessage(content=question))
        messages.append(AIMessage(content=answer))
    
    return {
        "messages": messages,
        "preferences": {},
        "search_results": {},
        "recommendations": "",
        "current_question_idx": 0,
        "questions": questions
    }

def ask_question(state: State) -> State:
    """Process the next question-answer pair."""
    if state["current_question_idx"] >= len(state["questions"]):
        return state
    
    # The question is already in messages, just return the state
    return state

def process_answer(state: State) -> State:
    """Process the predefined answer and store it in preferences."""
    messages = state["messages"]
    
    # Ensure we have both a question and an answer
    if len(messages) < 2 or state["current_question_idx"] >= len(state["questions"]):
        return state
    
    try:
        last_question = state["questions"][state["current_question_idx"]]
        # Get the answer from messages - it will be after the question
        answer_idx = (state["current_question_idx"] * 2) + 1  # Calculate the index of the answer
        last_answer = messages[answer_idx].content
        
        state["preferences"][last_question] = last_answer
        state["current_question_idx"] += 1
        
        # Print the Q&A for visibility
        print(f"\nQ: {last_question}")
        print(f"A: {last_answer}\n")
        
    except IndexError:
        return state
    
    return state

async def search_music_info(state: State) -> State:
    """Search for music recommendations based on preferences."""
    preferences = state["preferences"]
    search_results = {}
    
    # Search for artist recommendations
    if preferences.get("What are some of your favorite artists or bands?"):
        artists_query = f"Music similar to {preferences['What are some of your favorite artists or bands?']}"
        search_results["artist_based"] = tavily_client.search(
            query=artists_query,
            search_depth="advanced",
            max_results=5
        )
    
    # Search for genre recommendations
    if preferences.get("What genres of music do you enjoy the most?"):
        genre_query = f"Best {preferences['What genres of music do you enjoy the most?']} songs"
        search_results["genre_based"] = tavily_client.search(
            query=genre_query,
            search_depth="advanced",
            max_results=5
        )
    
    # Search for mood-based recommendations
    mood_question = "Are there any moods or themes you're looking for in new music?"  # Fixed apostrophe
    if preferences.get(mood_question):
        mood_query = f"{preferences[mood_question]} music recommendations"
        search_results["mood_based"] = tavily_client.search(
            query=mood_query,
            search_depth="advanced",
            max_results=5
        )
    
    state["search_results"] = search_results
    return state

def generate_recommendations(state: State) -> State:
    """Generate personalized music recommendations."""
    preferences = state["preferences"]
    search_results = state["search_results"]
    
    # Prepare context from search results
    context = ""
    for category, results in search_results.items():
        context += f"\n{category.replace('_', ' ').title()} Search Results:\n"
        for result in results.get("results", []):
            context += f"- {result.get('title')}: {result.get('content')[:200]}...\n"
    
    # Create a prompt for the LLM
    prompt = f"""
    IMPORTANT: You must ONLY recommend songs by the artists explicitly listed in "What are some of your favorite artists or bands?". Do not recommend songs from any other artists, even if they appear elsewhere in the user's preferences.

    Based on the user's preferences, suggest 5-7 songs from ONLY their favorite artists/bands. For each song, include:
    1. Artist name (must be one of their favorite artists)
    2. Song title
    3. A brief explanation of why they might like it, considering their genre and mood preferences

    User Preferences:
    {preferences}

    Search Results:
    {context}

    Remember: You are STRICTLY LIMITED to recommending songs by artists listed in "What are some of your favorite artists or bands?". Do not recommend songs by any other artists, even if they're mentioned elsewhere in the preferences.
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a music recommendation expert. Your primary rule is to ONLY suggest songs by artists that the user explicitly listed as their favorite artists. Never recommend songs by other artists, even if mentioned elsewhere in their preferences."},
            {"role": "user", "content": prompt}
        ]
    )
    
    state["recommendations"] = response.choices[0].message.content
    return state

def should_continue_questions(state: State) -> bool:
    """Determine if we should continue asking questions."""
    return state["current_question_idx"] < len(state["questions"])

def router(state: State) -> str:
    """Route to the next node based on state."""
    if should_continue_questions(state):
        return "ask_question"
    return "search_music"

# Build the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("ask_question", ask_question)
workflow.add_node("process_answer", process_answer)
workflow.add_node("search_music", search_music_info)
workflow.add_node("generate_recommendations", generate_recommendations)

# Add edges
workflow.add_edge("ask_question", "process_answer")
workflow.add_conditional_edges(
    "process_answer",
    router,
    {
        "ask_question": "ask_question",
        "search_music": "search_music"
    }
)
workflow.add_edge("search_music", "generate_recommendations")
workflow.add_edge("generate_recommendations", END)

# Set entry point
workflow.set_entry_point("ask_question")

# Compile the graph
graph = workflow.compile()

# Main function with Judgment trace decorator
# @judgment.observe(span_type="workflow")
async def music_recommendation_bot():
    """Main function to run the music recommendation bot."""
    print("🎵 Welcome to the Music Recommendation Bot! 🎵")
    print("I'll ask you a few questions to understand your music taste, then suggest some songs you might enjoy.")
    print("\nRunning with predefined answers for testing...\n")
    
    # Initialize state with predefined answers
    initial_state = initialize_state()
    
    try:
        # Initialize handler and set it globally
        handler = JudgevalCallbackHandler(judgment)
        set_global_handler(handler)
        
        # Run the entire workflow with graph.invoke
        final_state = await graph.ainvoke(initial_state)
        print("\n🎧 Your Personalized Music Recommendations 🎧")
        print(final_state["recommendations"])
        return final_state["recommendations"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Ensure we clear the handler
        clear_global_handler()


if __name__ == "__main__":
    asyncio.run(music_recommendation_bot())