#!/usr/bin/env python3
"""Weekly topic research for Sekunde 30 / LENZI."""
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

PROMPT = """You are the intelligence analyst for Michael Kamukulu's personal brand LENZI.

Today is """ + today + """.

WHO IS MICHAEL KAMUKULU — the full picture
==========================================
Michael Kamukulu is an Executive Director, systems builder, and public sector leader
based in Tanzania. He builds and tests programmes that change how institutions function
— at scale, with published evidence, inside governments with limited capacity.

His work spans education, governance, technology policy, youth economic inclusion,
and institutional design. He is currently building Timamu (a new initiative — include
when relevant). His brand LENZI operates across: Learning, Technology, Systems.

He speaks to Africa's professional class and the global audience thinking seriously
about institutions that work. His authority: published RCT evidence (Quarterly Journal
of Economics) + direct access inside governments, ministries, donor systems, AND ground-
level field programmes. ~500K followers: TikTok 211K, Facebook 161K, Instagram 104K.

HIS CONTENT CANVAS — what he can speak about (DO NOT limit to education)
=========================================================================
1. AI and technology in public institutions — any sector
2. Leadership inside complex African systems — what real institutional change looks like
3. Systems thinking — why the same problems keep recurring, how to break the cycle
4. Evidence and accountability — the gap between what data says and what institutions do
5. Africa's builders — speaking to Africa's professional class designing the continent
6. Youth and economic opportunity — labour markets, skills systems, opportunity structures
7. Governance and reform — what makes public sector change succeed versus stall
8. Technology as institutional tool — data systems, AI, digital infrastructure in government
9. Tanzania/EAC as global laboratory — what East Africa's experience tells the world
10. Education and learning — ONE domain within the broader canvas, not the defining frame
11. Personal leadership — navigating evidence, power, and institutional change

CONTENT PILLARS
===============
• AI & Humanity — AI's real impact on institutions, governance, work, and society (not hype)
• Africa — pan-African systems thinking, not poverty narrative; Africa as builder, not recipient
• Leadership — what institutional leadership actually requires; accountability and design
• Employability — Africa's youth, skills systems, the structures that create or deny opportunity
• Education — evidence-based, reform-focused, ground-truth — one lens, not the only one
• TZ/KE Context — Tanzania and Kenya specific; Swahili-speaking professional class

CONTENT RULES
=============
• Michael is always first-person. Never institutional.
• LearnImpact, KiuFunza, SOMA must NOT appear unless Michael explicitly decides.
• Bridge formula: start with "I" (personal, relatable moment) → land on "we" (systemic insight)
• The classroom/teacher angle appears ONLY when it is the right story — not as default
• He speaks to leaders, builders, policymakers, professionals — not just educators

RESEARCH BRIEF — week of """ + today + """
=========================================
Think across ALL of the following, not just education:

GLOBAL SIGNALS:
- UNESCO, World Bank, IMF, OECD, ILO, WEF, UN publications this month
- What is trending on LinkedIn among African professionals and global thought leaders
- AI + governance, AI + employment, AI + public services — what is being said globally
- What tensions exist between global development narratives and African institutional reality
- What counter-narratives or surprising positions are gaining traction among serious thinkers
- Leadership failures or successes in African public institutions this week
- Technology, data, and digital infrastructure developments in Africa

EAST AFRICA SPECIFIC:
- What is happening in Tanzania and Kenya in governance, tech, economy, youth, education
- What policy debates are live in the TZ/KE professional and public sector space
- What would resonate with Swahili-speaking professionals building institutions

MICHAEL'S POSITIONING:
- Which topics give him a "I was inside this / I measured this" angle?
- Which topics help transition his existing audience toward systems/AI/leadership content?
- Which topics are genuinely counter-intuitive or emotionally resonant for Africa's professional class?
- MIX the pillars: do not generate 18 education topics. Spread across the full canvas.

Generate exactly 18 topics: 12 global (ids 1-12) + 6 TZ/KE specific (ids 13-18, tzke: true).
Spread across at least 4 of the 6 content pillars. Maximum 4 education-specific topics.

Scoring:
- virality (1-10): emotional charge + counter-narrative strength + shareability
- brandFit (1-10): fit with LENZI — Learning, Technology, Systems (NOT just education brand)
- bridge (1-10): how well this moves existing audience toward systems/AI/leadership positioning

Return ONLY a raw JSON array. No markdown. No explanation. Start with [ end with ].

Each item:
{"id":1,"title":"max 10 words","category":"AI & Humanity","virality":9,"brandFit":9,"bridge":8,
"trendingBecause":"why timely","michaelAngle":"first-person unique angle from his actual experience",
"hook":"under 15 words scroll-stopping opener","angle":"distinctive take",
"platforms":["LinkedIn","TikTok"],"sourceContext":"named source","tzke":false}

Topics 13-18 must have "tzke": true. Mix categories — not all education."""

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
    print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Request failed: {e}", file=sys.stderr)
    sys.exit(1)

raw   = data.get("content", [{}])[0].get("text", "")
match = re.search(r"\[[\s\S]*\]", raw)
if not match:
    print(f"No JSON array in response:\n{raw[:400]}", file=sys.stderr)
    sys.exit(1)

try:
    topics = json.loads(match.group(0))
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}", file=sys.stderr)
    sys.exit(1)

if len(topics) < 12:
    print(f"Only {len(topics)} topics returned (expected 18)", file=sys.stderr)
    sys.exit(1)

output = {"generated": now.isoformat(), "week": week, "topics": topics}
with open("topics.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

usage = data.get("usage", {})
print(f"OK: {len(topics)} topics for {week} | {usage.get('input_tokens','?')} in / {usage.get('output_tokens','?')} out")
