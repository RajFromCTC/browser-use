# server.py
from flask import Flask, request, jsonify
from browser_use import Agent, ChatOpenAI
import asyncio

app = Flask(__name__)

# --------------------------
# Helper: safe async runner
# --------------------------
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()

    if loop.is_running():
        # already running (inside flask/werkzeug dev server)
        future = asyncio.ensure_future(coro)
        loop.run_until_complete(future)
        return future.result()
    else:
        return loop.run_until_complete(coro)

# --------------------------
# Core async agent runner
# --------------------------
async def run_agent(task: str):
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4.1-mini"),
    )
    history = await agent.run(max_steps=50)
    return history

# --------------------------
# Flask route
# --------------------------
@app.route("/run-task", methods=["POST"])
def run_task():
    data = request.get_json(silent=True) or {}
    task = data.get("task", "open google.com and search for weather in Delhi")

    try:
        history = run_async(run_agent(task))

        # Preferred: use final_result() if available
        final_text = None
        if hasattr(history, "final_result"):
            try:
                final_text = history.final_result()
            except Exception:
                pass

        # Fallback: last extracted_content
        if not final_text and hasattr(history, "all_results") and history.all_results:
            last = history.all_results[-1]
            final_text = getattr(last, "extracted_content", None) or getattr(last, "long_term_memory", None)

        return jsonify({
            "status": "ok",
            "task": task,
            "final_result": final_text or "No final result found"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500

# --------------------------
# Entry point
# --------------------------
if __name__ == "__main__":
    # Dev server (don’t use in production)
    app.run(host="0.0.0.0", port=8000)
