#!/usr/bin/env python3
"""Weekly topic research for Sekunde 30 / LENZI — runs inside GitHub Actions."""
import os, json, re, sys
import urllib.request, urllib.error
from datetime import datetime, timezone

api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
    sys.exit(1)

now   = datetime.now(timezone.utc)
today = now.strftime("%B %d, %Y")
week  = now.strftime("%Y-W%V")

PROMPT = """You are the intelligence analyst for Michael Kamukulu's personal content brand LENZI.

Today is """ + today + """. Generate the weekly Sekunde 30 content research brief.

======================================================
WHO IS MICHAEL KAMUKULU
======================================================
Executive Director of LearnImpact, Dar es Salaam, Tanzania. Personal brand: LENZI — "Learning, Technology, Systems." He speaks to Africa's professional class about systems thinking, AI in education, learning reform, and building institutions that work. RCT evidence published in Quarterly Journal of Economics. ~500K followers: TikTok 211K, Facebook 161K, Instagram 104K. 10+ years inside Tanzania's education system.

POSITIONING: Influential Leader. Not a motivational coach. Not a development worker. An African systems thinker who speaks plainly about what it takes to change things.

ABSOLUTE CONTENT RULES:
- Michael is always first-person. Never institutional.
- LearnImpact, KiuFunza, SOMA must NOT appear.
- Audience: Africa's professional class — people thinking about systems, AI, careers, Africa's future.
- Every topic needs a "what only Michael can say" angle from his Tanzania/Kenya fieldwork.
- Bridge formula: start with "I" (personal relatable moment) land on "we" (systemic insight).

HIS 6 CONTENT PILLARS:
1. AI & Humanity — AI's actual role in African education and work (vs the hype)
2. Africa — pan-African systems thinking, not poverty narrative
3. Education — evidence-based, reform-focused, ground-truth
4. Employability — Africa's youth, skills gap, systems that serve or fail them
5. Leadership — institutional leaders, decision-making, accountability
6. TZ/KE Context — Tanzania and Kenya specific, Swahili-speaking professional class

TRANSITION GAP (critical context):
Current TikTok: 62 Relationships posts, 52 Growth Mindset, 38 Motivation. Only 6 AI & Technology.
Bridge formula: human personal entry point that lands on a systems insight.

======================================================
RESEARCH BRIEF
======================================================
Think carefully about what is happening in the world during the week of """ + today + """.

GLOBAL SIGNALS to reason through:
- What UNESCO, World Bank, IMF, OECD, ILO have released recently on education, AI, employment
- What is trending on LinkedIn among African professionals and global thought leaders this week
- What AI + education or AI + jobs news is generating significant conversation globally
- What counter-narrative positions are resonating in professional circles
- What tensions exist between global development frameworks and African reality

EAST AFRICA SPECIFIC:
- What is happening in Tanzania and Kenya in education policy, youth employment, governance
- What debates are live in the TZ/KE professional and public sector space
- What would resonate with Swahili-speaking professionals

======================================================
OUTPUT REQUIREMENTS
======================================================
Generate exactly 18 topics: 12 global (ids 1-12) + 6 TZ/KE specific (ids 13-18, tzke: true).

Scoring:
- virality (1-10): emotional charge + counter-narrative strength + shareability
- brandFit (1-10): alignment with LENZI Influential Leader positioning
- bridge (1-10): how well this bridges existing audience toward systems/AI/education

Quality bar: every topic must be publishable immediately. No filler. Hook must be under 15 words.

Return ONLY a raw JSON array. No markdown. No explanation. No code fences. Start with [ end with ].

Each object must have exactly these fields:
id, title, category, virality, brandFit, bridge, trendingBecause, michaelAngle, hook, angle, platforms, sourceContext, tzke

Example of ONE object (do not copy — generate 18 unique original ones):
{"id":1,"title":"Example topic title here","category":"AI & Humanity","virality":9,"brandFit":9,"bridge":8,"trendingBecause":"One sentence why timely","michaelAngle":"First-person unique angle","hook":"Under 15 words hook","angle":"The distinctive take","platforms":["LinkedIn","TikTok"],"sourceContext":"UNESCO 2026","tzke":false}
"""

payload = json.dumps({
    "model": "claude-sonnet-4-6",
    "max_tokens": 8000,
    "messages": [{"role": "user", "content": PROMPT}]
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=payload,
    headers={
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")
    print(f"API error {e.code}: {body}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Request failed: {e}", file=sys.stderr)
    sys.exit(1)

raw = data.get("content", [{}])[0].get("text", "")
match = re.search(r"\[[\s\S]*\]", raw)
if not match:
    print(f"No JSON array in response. Raw (first 500):\n{raw[:500]}", file=sys.stderr)
    sys.exit(1)

try:
    topics = json.loads(match.group(0))
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}", file=sys.stderr)
    sys.exit(1)

if not isinstance(topics, list) or len(topics) < 12:
    print(f"Expected 18 topics, got {len(topics)}", file=sys.stderr)
    sys.exit(1)

output = {
    "generated": now.isoformat(),
    "week": week,
    "topics": topics
}

with open("topics.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

usage = data.get("usage", {})
print(f"OK: {len(topics)} topics for week {week}")
print(f"Tokens: {usage.get('input_tokens','?')} in / {usage.get('output_tokens','?')} out")
