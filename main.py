"""
Stock Analysis Agent - Main Entry Point

This is a simple entry point that starts the Chainlit UI.
All UI logic is in ui/ui.py (separation of concerns).

Run with: 
    python main.py
    OR
    uv run chainlit run ui/ui.py
"""

import subprocess
import sys
import os


def run_ui():
    """Run the Chainlit UI by executing chainlit command."""
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "ui.py")
    
    try:
        # Try running with uv first (for projects using uv package manager)
        print("🔧 Starting with uv...")
        subprocess.run(["uv", "run", "chainlit", "run", ui_path], check=True)
    except FileNotFoundError:
        # Fallback to direct chainlit command
        print("🔧 Trying direct chainlit command...")
        try:
            subprocess.run(["chainlit", "run", ui_path], check=True)
        except FileNotFoundError:
            print("❌ Chainlit not found. Installing...")
            subprocess.run(["uv", "pip", "install", "chainlit"], check=True)
            print("✅ Chainlit installed. Starting app...")
            subprocess.run(["uv", "run", "chainlit", "run", ui_path], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"💡 Try running directly: uv run chainlit run {ui_path}")


if __name__ == "__main__":
    print("🚀 Starting Stock Analysis Agent...")
    run_ui()
