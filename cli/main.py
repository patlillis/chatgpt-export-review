import argparse
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
    # Set up argparse to take in the file path and keyword
    parser = argparse.ArgumentParser(
        description="Search conversations from a JSON file."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Path to the conversations.json file",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        required=True,
        help="Keyword to search for in conversations",
    )

    # Parse arguments
    args = parser.parse_args()

    # Get the directory where the script is located
    file_path = Path(args.file)

    # Load the data
    if file_path.exists():
        data = load_data(file_path)
    else:
        print(f"Error: File '{file_path}' not found.")
        exit(1)

    # Search for the keyword in conversations
    search_results = search_conversations(args.keyword, data)

    # Display the results in TUI style
    display_results_tui(search_results)
