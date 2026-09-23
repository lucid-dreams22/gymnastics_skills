
import streamlit as st
from skills_data import (
    SKILLS,
    DIFFICULTY_LABELS,
    GENERAL_DEDUCTIONS,
    difficulty_for_rotation,
)

st.set_page_config(
    page_title="High School Gymnastics Skill Helper",
    page_icon="🤸",
    layout="centered",
)

EVENT_LABELS = {
    "vault": "Vault",
    "bars": "Uneven Bars",
    "beam": "Balance Beam",
    "floor": "Floor Exercise",
}

def pretty_rotation(value):
    labels = {
        "0": "No turn",
        "0.5": "½ turn",
        "0.75": "¾ turn",
        "1.0": "1 full turn",
        "1.5": "1½ turns",
        "2.0": "2 turns",
        "3.0": "3 turns",
    }
    return labels.get(str(value), f"{value} turn(s)")

def show_difficulty(code):
    full = DIFFICULTY_LABELS.get(code, code)
    if code in {"M", "S", "HS", "AHS"}:
        st.metric("Difficulty", f"{full} ({code})")
    else:
        st.metric("Difficulty", full)

def show_deductions(skill, event):
    st.subheader("Possible deductions / errors")
    items = skill.get("deductions", [])
    if not items:
        st.info("No deduction list is stored for this entry.")
        return

    for item in items:
        if isinstance(item, str):
            st.write(f"• {item}")
            continue

        fault = item.get("fault", "Execution error")
        suffix = ""

        if "value" in item:
            suffix = f" — {item['value']:.2f}"
        elif "max" in item:
            suffix = f" — up to {item['max']:.2f}"
        elif "range" in item:
            low, high = item["range"]
            suffix = f" — {low:.2f} to {high:.2f}"

        note = item.get("note")
        if note:
            suffix += f" ({note})"

        st.write(f"• **{fault}**{suffix}")

    # Keep general rules visually separate from skill-specific issues.
    if event in GENERAL_DEDUCTIONS:
        with st.expander("Common event-wide execution deductions"):
            for item in GENERAL_DEDUCTIONS[event]:
                fault = item.get("fault", "Execution error")
                suffix = ""
                if "value" in item:
                    suffix = f" — {item['value']:.2f}"
                elif "max" in item:
                    suffix = f" — up to {item['max']:.2f}"
                elif "range" in item:
                    suffix = f" — {item['range'][0]:.2f} to {item['range'][1]:.2f}"
                st.write(f"• {fault}{suffix}")

st.title("🤸 High School Gymnastics Skill Helper")
st.caption("NFHS-focused reference for selected varsity gymnastics skills")

st.warning(
    "This is an educational reference, not a substitute for an official judge, "
    "coach, state association, or current NFHS rulebook."
)

event = st.selectbox(
    "1. Choose an event",
    options=list(EVENT_LABELS.keys()),
    format_func=lambda x: EVENT_LABELS[x],
)

skills_for_event = SKILLS[event]

skill_id = st.selectbox(
    "2. Choose a skill",
    options=list(skills_for_event.keys()),
    format_func=lambda x: skills_for_event[x]["name"],
)

skill = skills_for_event[skill_id]

rotation_options = skill.get("rotations", {})
selected_rotation = None

if rotation_options:
    selected_rotation = st.selectbox(
        "3. Choose rotation",
        options=list(rotation_options.keys()),
        format_func=pretty_rotation,
    )
    difficulty = difficulty_for_rotation(event, skill_id, selected_rotation)
else:
    difficulty = skill.get("difficulty", "NA")

st.divider()

left, right = st.columns([2, 1])
with left:
    display_name = skill["name"]
    alias = skill.get("display_alias")
    st.header(alias or display_name)
    if alias and alias != display_name:
        st.caption(f"Official/technical name in database: {display_name}")

    rotation_alias = skill.get("rotation_aliases", {}).get(str(selected_rotation))
    if rotation_alias:
        st.success(f"This variation is commonly called **{rotation_alias}**.")

with right:
    show_difficulty(difficulty)

status = skill.get("competition_status")
if status == "not_recognized_nfhs_2026_28":
    st.error(
        "Current NFHS status: this vault is not recognized as a valued vault "
        "for the 2026–28 rules cycle."
    )

st.subheader("How to perform it")
st.write(skill.get("how_to", "Description not available."))

if skill.get("hold_seconds") is not None and skill.get("hold_seconds", 0) > 0:
    st.info(
        f"**Expected hold:** {skill['hold_seconds']} seconds in a controlled final position."
    )

key_shapes = skill.get("key_shapes", [])
if key_shapes:
    st.subheader("What the skill should look like")
    for shape in key_shapes:
        st.write(f"• {shape}")

show_deductions(skill, event)

connections = skill.get("connections", [])
st.subheader("Possible combinations")
if connections:
    for connection_id in connections:
        if connection_id in skills_for_event:
            other = skills_for_event[connection_id]
            st.write(
                f"• {skill.get('display_alias', skill['name'])} → "
                f"{other.get('display_alias', other['name'])} "
                f"({DIFFICULTY_LABELS.get(other.get('difficulty'), other.get('difficulty'))})"
            )
        else:
            st.write(f"• {connection_id.replace('_', ' ').title()}")
else:
    st.write("No combinations are stored for this skill yet.")

if skill.get("rule_note"):
    with st.expander("Rule note"):
        st.write(skill["rule_note"])

if skill.get("safety"):
    with st.expander("Safety note"):
        st.write(skill["safety"])

st.divider()

st.subheader("AI Skill Analysis")
st.write(
    "Describe what is happening when you attempt the skill. "
    "The final version can use this together with the selected skill and deductions "
    "to suggest likely causes, drills, and technique cues."
)

problem = st.text_area(
    "What is going wrong?",
    placeholder=(
        "Example: My legs bend during my back handspring and I land with my chest low."
    ),
)

observed = st.multiselect(
    "Which problems do you notice?",
    options=[
        item["fault"] if isinstance(item, dict) else item
        for item in skill.get("deductions", [])
    ],
)

if st.button("Analyze My Skill", type="primary"):
    if not problem.strip() and not observed:
        st.warning("Describe the problem or select at least one observed error first.")
    else:
        st.info(
            "The interface is working. The next development step is connecting this "
            "button to an AI model so it can generate individualized analysis."
        )
        st.write("**Information that would be sent to the AI:**")
        st.write(f"- Event: {EVENT_LABELS[event]}")
        st.write(f"- Skill: {skill['name']}")
        if selected_rotation is not None:
            st.write(f"- Rotation: {pretty_rotation(selected_rotation)}")
        st.write(f"- Difficulty: {DIFFICULTY_LABELS.get(difficulty, difficulty)}")
        if observed:
            st.write("- Observed errors: " + ", ".join(observed))
        if problem.strip():
            st.write("- Gymnast's description: " + problem.strip())

st.divider()
st.caption(
    "Rules can vary by season and state association. Always verify competition questions "
    "against the current official rules used by your school."
)
