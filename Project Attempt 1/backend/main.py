
import os
import json
import sqlite3
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

# --- Configuration & Initialization ---
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_opportunity(data: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = [
        "title", "client", "contact_name", "contact_email", "description",
        "type", "complexity", "duration", "skills", "deal_value"
    ]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=422, detail=f"Missing field: {field}")
    # Optionally: add more validation here (e.g., email format, deal_value is float)
    return data

# --- Utility Functions ---
client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

async def generate_insights(data: dict) -> dict:
    """
    Generate insights using LLM based on the provided opportunity data.
    Returns a dictionary with insights or error information.
    """
    prompt = f"""
    Given the following opportunity data:
    Title: {data['title']}
    Client: {data['client']}
    Contact Name: {data['contact_name']}
    Contact Email: {data['contact_email']}
    Description: {data['description']}
    Type: {data['type']}
    Complexity: {data['complexity']}
    Duration: {data['duration']}
    Skills: {data['skills']}
    Deal Value: {data['deal_value']}

    Generate a JSON object with the following fields:
    - top_performing_lead_sources: (string, short summary)
    - conversion_patterns: (string, short summary)
    - recommendations: (string, short actionable recommendations)
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )
        content = response.choices[0].message.content
        try:
            if content is not None:
                insights = json.loads(content)
            else:
                insights = {"raw": "No content returned from LLM."}
        except Exception:
            insights = {"raw": content}
        return insights
    except Exception as e:
        return {"error": str(e)}

def save_opportunity_to_db(opportunity: Dict[str, Any], insights: dict) -> None:
    """
    Save the opportunity and its insights to the SQLite database.
    Raises HTTPException on failure.
    """
    try:
        with sqlite3.connect('opportunity.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO opportunities (
                    title, client, contact_name, contact_email, description, type, complexity, duration, skills, deal_value, insights
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                opportunity["title"],
                opportunity["client"],
                opportunity["contact_name"],
                opportunity["contact_email"],
                opportunity["description"],
                opportunity["type"],
                opportunity["complexity"],
                opportunity["duration"],
                opportunity["skills"],
                float(opportunity["deal_value"]),
                json.dumps(insights)
            ))
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# --- API Endpoints ---
@app.post("/opportunity", status_code=status.HTTP_201_CREATED)
async def create_opportunity(request: Request):
    """
    Receive opportunity data, generate insights, save to DB, and return insights.
    """
    data = await request.json()
    opportunity = validate_opportunity(data)
    insights = await generate_insights(opportunity)
    save_opportunity_to_db(opportunity, insights)
    return {**opportunity, "insights": insights}


# --- View Opportunities Endpoint ---
from fastapi.responses import HTMLResponse

@app.get("/view_opportunity", response_class=HTMLResponse)
def view_opportunity():
    """
    Fetch the latest 10 opportunities from the database and return as an HTML table.
    """
    try:
        with sqlite3.connect('opportunity.db') as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM opportunities ORDER BY id DESC LIMIT 10")
            rows = c.fetchall()
            if not rows:
                return "<div>No opportunities found.</div>"
            table = [
                "<table class='opp-table'><thead><tr>"
                "<th>ID</th><th>Title</th><th>Client</th><th>Contact Name</th><th>Contact Email</th>"
                "<th>Description</th><th>Type</th><th>Complexity</th><th>Duration</th><th>Skills</th><th>Deal Value</th><th>Insights</th>"
                "</tr></thead><tbody>"
            ]
            for row in rows:
                table.append(f"<tr>"
                    f"<td>{row['id']}</td>"
                    f"<td>{row['title']}</td>"
                    f"<td>{row['client']}</td>"
                    f"<td>{row['contact_name']}</td>"
                    f"<td>{row['contact_email']}</td>"
                    f"<td>{row['description']}</td>"
                    f"<td>{row['type']}</td>"
                    f"<td>{row['complexity']}</td>"
                    f"<td>{row['duration']}</td>"
                    f"<td>{row['skills']}</td>"
                    f"<td>{row['deal_value']}</td>"
                    f"<td><pre>{row['insights']}</pre></td>"
                "</tr>")
            table.append("</tbody></table>")
            return "".join(table)
    except Exception as e:
        return f"<div style='color:red;'><b>Error:</b> {e}</div>"