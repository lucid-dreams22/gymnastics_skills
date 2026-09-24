from groq import Groq


SYSTEM_PROMPT = """
You are a gymnastics technique assistant for high-school varsity gymnasts.

Analyze the gymnast's problem using the skill information supplied by the app.

Return these sections:

### Likely Cause
Explain the likely technical reasons for the problem.

### Why This Causes the Problem
Explain how the technique issue causes the observed errors.

### What to Focus On
Give 2-4 short technique cues.

### Drills
Give 2-4 useful drills or progressions.

### Strength / Flexibility
Give 1-3 relevant exercises if useful.

### Safety
Mention when coaching, spotting, mats, or progressions are appropriate.

Rules:
- Do not diagnose injuries.
- Do not invent deduction values.
- Do not invent gymnastics competition rules.
- Do not encourage dangerous skills without proper coaching.
- Use simple language appropriate for a high-school gymnast.
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

HOW TO PERFORM THE SKILL:
{how_to}

IMPORTANT BODY POSITIONS:
{", ".join(key_shapes)}

OBSERVED ERRORS:
{", ".join(observed_errors) if observed_errors else "None selected"}

GYMNAST DESCRIPTION:
{gymnast_description}
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.4,
        max_tokens=700,
    )

    return completion.choices[0].message.content