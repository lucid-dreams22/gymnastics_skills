from groq import Groq


SYSTEM_PROMPT = """
You are a gymnastics technique assistant for high-school varsity gymnasts.

Analyze the gymnast's problem using the supplied skill information.

Keep the answer practical and concise. Use these exact sections:

### Likely Cause
Explain the most likely technical causes based on the gymnast's description
and selected execution errors.

### Technique Fixes
Give 2-4 specific cues the gymnast can think about while performing the skill.

### Possible Strength or Mobility Weaknesses
List only plausible physical contributors that actually relate to this skill.
Do NOT diagnose the gymnast. Phrase them as possibilities, such as:
"Limited shoulder flexion may contribute to..."
For each possible weakness, name the main muscle group(s) involved.

### Simple Exercises
Give 2-4 simple exercises targeting the most important muscles or mobility
limitations you identified. Prefer exercises that can be done with bodyweight,
a resistance band, light dumbbells, or common gym equipment.
For each exercise, state what it targets and give a simple set/rep suggestion.

### Drills
Give 2-4 gymnastics drills or progressions that address the specific problem.

Rules:
- Do not diagnose injuries or medical conditions.
- Do not claim a muscle is definitely weak from text alone.
- Do not invent gymnastics rules or deduction values.
- Competition deductions must come only from the information supplied by the app.
- Do not recommend advanced progressions that should be attempted without a coach.
- Keep explanations understandable for a high-school gymnast.
- Avoid filler, motivational language, and generic advice.
"""


def analyze_skill(
    api_key,
    event,
    skill_name,
    difficulty,
    rotation,
    how_to,
    key_shapes,
    observed_errors,
    gymnast_description,
):
    client = Groq(api_key=api_key)

    prompt = f"""
EVENT:
{event}

SKILL:
{skill_name}

DIFFICULTY:
{difficulty}

ROTATION:
{rotation or "None"}

CORRECT TECHNIQUE:
{how_to}

KEY POSITIONS:
{", ".join(key_shapes)}

OBSERVED ERRORS / DEDUCTIONS:
{", ".join(observed_errors) if observed_errors else "None selected"}

GYMNAST DESCRIPTION:
{gymnast_description}

Focus especially on:
1. What part of the movement is likely breaking down.
2. Which strength or mobility limitations could plausibly contribute.
3. Which major muscles are most relevant.
4. Simple exercises and gymnastics drills that directly target those issues.
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=900,
    )

    return completion.choices[0].message.content
