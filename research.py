#!/usr/bin/env python3
"""Weekly topic research for Sekunde 30 / LENZI — Michael Kamukulu."""
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

PROMPT = """You are generating the weekly Sekunde 30 content brief for Michael Kamukulu's personal brand LENZI.

Today is """ + today + """.

WHO MICHAEL IS — complete picture
==================================
Michael Kamukulu is a systems builder, institutional leader, philosopher, and founder
based in Dar es Salaam, Tanzania. He operates two distinct organizations:

LEARNIMPACT (Executive Director): Learning Systems Architecture organization.
Partners with Tanzania's government to design and scale complete learning systems.
10+ years RCT evidence published in the Quarterly Journal of Economics. USD 7/child/year.
Aligned with Tanzania's presidential KKK Scientific Strategic Plan 2026-2030.
[LearnImpact does NOT appear in LENZI content unless Michael decides.]

TIMAMU FOUNDATION (Founder, 2026): Philosophy foundation.
Mission: "Timamu enables persons with disabilities to own a share in the economy — through technology."
Philosophy: "When every person is complete, the world is complete."
Timamu = complete, whole, exact (Swahili).
Phase 1: creator economy + assistive technology. Tanzania first, East Africa next.
800,000 young Tanzanians enter job market yearly. Fewer than 40,000 formal jobs exist.
Tanzania: est. 9-10 million people live with a disability (WHO).
[Timamu content appears at Michael's discretion. The philosophy is freely usable across all LENZI content.]

PERSONAL BRAND: LENZI. Learning. Technology. Systems. Personal reach: ~500K.

THE UNIFYING PHILOSOPHY:
Systems exclude people not because of who they are, but because of how systems were designed.
Children who cannot read, persons with disabilities locked out of the digital economy,
African youth trained for jobs that don't exist — same diagnosis, different domains.
The problem is never the person. It is the design. And design can be changed.

HIS SELF-DESCRIPTION:
"At my best I speak about: the future, emerging technologies, productivity, visibility,
systems alignment, serving everyone, income generation, youth."
"I want in conversation with: top leaders, super-intelligent people, creators, change makers."
"Beyond education: creative industry, technology, data, youth empowerment as life coach."
"What most people get wrong about institutions: misalignment between education and after-school
systems. Systems need to evolve fast. Systems are shaped by culture. Systems are invisible —
we feel them. They are sometimes the unwritten rules."

CONTENT CANVAS — all of these are valid topic domains
=====================================================
1.  AI and emerging technology — any system: governance, health, work, economy, education
2.  Systems thinking — invisible architecture, unwritten rules, cultural alignment, evolution
3.  Leadership and accountability — what institutional change actually requires
4.  Youth and economic opportunity — income generation, school-to-earning gap
5.  Productivity and personal effectiveness — for Africa's professional class
6.  Visibility — who gets seen, who doesn't, and why systems decide that
7.  Creator economy and digital income — who gets to earn online and who is locked out
8.  Disability inclusion and the digital economy (Timamu domain)
9.  Education and learning — ONE domain, not the defining frame
10. Africa's builders — designing the continent's institutions and future
11. Future of work in Africa — AI, automation, 800K youth enter market yearly
12. Institution building — what makes organizations last; what makes reform fail

CONTENT PILLARS (spread across — max 4 education-specific):
AI & Humanity | Africa | Leadership | Employability & Income | Education | TZ/KE Context

CONTENT RULES:
Michael is always first-person. LearnImpact/KiuFunza/SOMA must NOT appear.
Bridge: personal "I" moment → systemic insight → "we can change it."
Classroom/teacher angle only when it is the right story — not the default.
Timamu philosophy ("you arrived complete, systems are the problem") can be applied to ANY topic.

RESEARCH BRIEF — week of """ + today + """
==========================================
Think across ALL domains, not just education:

GLOBAL SIGNALS:
- UNESCO, World Bank, IMF, OECD, ILO, WEF, WHO publications this week
- AI + governance, AI + employment, AI + digital inclusion — global conversation
- Creator economy, digital income, platform inclusion — who is being left out and why
- Disability and technology — what is the world getting right or wrong
- Youth, employment, economic opportunity — emerging data or narratives
- Surprising counter-narratives in leadership, institutions, or systems design
- Technology as a tool for inclusion vs. exclusion — any sector
- Productivity, visibility, income generation for Africa's professional class

EAST AFRICA SPECIFIC:
- Tanzania and Kenya across governance, tech, economy, youth, education
- Tanzania's creator economy (TZS 2 billion committed July 2026)
- What Swahili-speaking professionals are building, debating, or navigating

MICHAEL'S POSITIONING:
- Topics giving him "I was inside this / I built this / I measured this" angle
- Topics applying his core philosophy — "the problem is the design, not the person"
- Topics bridging his existing audience (mindset/relationships) toward systems/AI/tech
- VARY the pillars: DO NOT produce education-heavy list
- Include at least one topic on income, productivity, or visibility
- Include at least one topic where the Timamu philosophy angle works powerfully

Generate exactly 18 topics: 12 global (ids 1-12) + 6 TZ/KE specific (ids 13-18, tzke: true).
Spread across at least 5 of the 6 content pillars. Maximum 4 education-specific topics.

Scoring:
- virality (1-10): emotional charge + counter-narrative strength + shareability
- brandFit (1-10): alignment with LENZI — systems, tech, youth, income, leadership
- bridge (1-10): bridges personal-growth audience toward systems/AI/leadership content

Return ONLY a raw JSON array. No markdown. No explanation. Start with [ end with ].
Each: {"id":1,"title":"max 10 words","category":"AI & Humanity","virality":9,"brandFit":9,"bridge":8,
"trendingBecause":"why timely","michaelAngle":"first-person from his specific experience",
"hook":"under 15 words scroll-stopping","angle":"distinctive take",
"platforms":["LinkedIn","TikTok"],"sourceContext":"named source","tzke":false}
Topics 13-18: "tzke":true. Mix categories across full canvas."""

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
    print(f"No JSON array:\n{raw[:400]}", file=sys.stderr)
    sys.exit(1)

try:
    topics = json.loads(match.group(0))
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}", file=sys.stderr)
    sys.exit(1)

if len(topics) < 12:
    print(f"Only {len(topics)} topics (expected 18)", file=sys.stderr)
    sys.exit(1)

output = {"generated": now.isoformat(), "week": week, "topics": topics}
with open("topics.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

usage = data.get("usage", {})
print(f"OK: {len(topics)} topics for {week} | {usage.get('input_tokens','?')} in / {usage.get('output_tokens','?')} out")
