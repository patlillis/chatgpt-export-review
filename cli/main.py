import json
from pathlib import Path
from rich.console import Console
from rich.table import Table


# Load the JSON file
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Define a function to search conversations by keyword with context handling
def search_conversations(keyword, data, context_chars=30):
    results = []
    for conversation in data:
        title = conversation.get("title", "No Title")
        messages = conversation.get("mapping", {})

        # Search in message contents
        for msg_id, msg_data in messages.items():
            if msg_data and msg_data.get(
                "message"
            ):  # Ensure msg_data and message exist
                message_parts = msg_data["message"].get("content", {}).get("parts", [])
                for part in message_parts:
                    if isinstance(part, str) and keyword.lower() in part.lower():
                        # Get a snippet with context around the keyword
                        keyword_index = part.lower().find(keyword.lower())
                        start = max(keyword_index - context_chars, 0)
                        end = min(
                            keyword_index + len(keyword) + context_chars, len(part)
                        )
                        snippet = part[start:end]

                        results.append(
                            {
                                "title": title,
                                "context": snippet.strip(),
                                "conversation_id": conversation.get("id", "Unknown ID"),
                                "message_id": msg_id,
                            }
                        )
    return results


# Display results in a TUI-style table using Rich
def display_results_tui(results):
    if results:
        console = Console()
        table = Table(title="Search Results", show_lines=True)

        table.add_column("Title", justify="left", style="cyan", no_wrap=True)
        table.add_column("Context", justify="left", style="magenta")
        table.add_column("Conversation ID", justify="left", style="green")
        table.add_column("Message ID", justify="left", style="yellow")

        for result in results:
            table.add_row(
                result["title"],
                result["context"],
                result["conversation_id"],
                result["message_id"],
            )

        console.print(table)
    else:
        print("No results found.")


if __name__ == "__main__":
    # Get the directory where the script is located
    current_dir = Path(__file__).parent

    # Path to your JSON file
    file_path = current_dir / ".." / "data" / "conversations.json"

    # Load the data
    data = load_data(file_path)

    # Get the keyword from user input
    keyword = input("Enter a keyword to search for: ")

    # Search for the keyword in conversations
    search_results = search_conversations(keyword, data)

    # Display the results in TUI style
    display_results_tui(search_results)
