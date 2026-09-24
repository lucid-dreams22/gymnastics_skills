
import html
import streamlit as st

from skills_data import (
    SKILLS,
    DIFFICULTY_LABELS,
    COMBINATION_RULES,
    DEDUCTION_PROFILES,
    deduction_profiles_for,
    difficulty_for_rotation,
)

try:
    from ai_helper import analyze_skill
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


st.set_page_config(
    page_title="High School Gymnastics Skills",
    page_icon="🤸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------
# Sleek, compact styling
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Hide Streamlit's white top chrome so it doesn't cover the title. */
    [data-testid="stHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        background: transparent !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: "Inter", "Segoe UI", Arial, sans-serif !important;
    }

    .stApp {
        background: #f4f6f5;
        color: #17201d;
    }

    [data-testid="stMain"] {
        width: 100% !important;
    }

    .block-container {
        width: 97% !important;
        max-width: 1700px !important;
        padding: 0.62rem 1.1rem 1rem !important;
        margin: 0 auto !important;
    }

    h1 {
        font-size: 2.15rem !important;
        line-height: 1.02 !important;
        margin: 0 0 0.05rem 0 !important;
        letter-spacing: -0.035em;
        font-weight: 760 !important;
    }

    h2 {
        font-size: 1.36rem !important;
        margin: 0.30rem 0 0.14rem !important;
        font-weight: 720 !important;
    }

    h3 {
        font-size: 1.12rem !important;
        margin: 0.26rem 0 0.12rem !important;
        font-weight: 720 !important;
    }

    p, li, label, .stMarkdown {
        font-size: 1.04rem !important;
        line-height: 1.24 !important;
    }

    [data-testid="stCaptionContainer"] {
        margin-top: -0.08rem !important;
        margin-bottom: 0.16rem !important;
    }

    [data-testid="stCaptionContainer"] p {
        font-size: 0.82rem !important;
        color: #64706c !important;
    }

    [data-testid="stHorizontalBlock"] {
        gap: 0.72rem !important;
        align-items: flex-start !important;
        flex-wrap: nowrap !important;
    }

    [data-testid="column"] {
        min-width: 0 !important;
    }

    div[data-testid="stSelectbox"],
    div[data-testid="stMultiSelect"],
    div[data-testid="stTextArea"] {
        margin-bottom: 0.06rem !important;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stTextArea"] label {
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.03rem !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 2.35rem !important;
        height: 2.35rem !important;
        background: #ffffff !important;
        border: 1px solid #cfd8d4 !important;
        border-radius: 7px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] span {
        font-size: 1.03rem !important;
    }

    textarea {
        min-height: 88px !important;
        line-height: 1.23 !important;
        font-size: 1.02rem !important;
    }

    hr {
        margin: 0.30rem 0 0.38rem !important;
        border-color: #d7dfdc !important;
    }

    .eyebrow {
        font-size: 0.94rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 760;
        color: #6c7773;
        margin-bottom: 0.12rem;
    }

    .intro-note {
        font-size: 0.99rem;
        color: #5d6965;
        border-left: 3px solid #789a8d;
        padding: 0.18rem 0 0.18rem 0.55rem;
        margin: 0.25rem 0 0.38rem;
    }

    .summary-line {
        border-top: 1px solid #d8dfdc;
        border-bottom: 1px solid #d8dfdc;
        padding: 0.48rem 0;
        margin: 0.05rem 0 0.28rem;
    }

    .skill-name {
        font-size: 1.52rem;
        font-weight: 760;
        line-height: 1.06;
        letter-spacing: -0.02em;
    }

    .skill-meta {
        font-size: 0.99rem;
        color: #65706c;
        margin-top: 0.10rem;
    }

    .difficulty-panel {
        border-left: 1px solid #cfd8d4;
        padding-left: 0.78rem;
        min-height: 58px;
    }

    .difficulty-title {
        font-size: 0.91rem;
        color: #65706c;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-weight: 780;
    }

    .difficulty-value {
        font-size: 1.15rem;
        line-height: 1.1;
        font-weight: 780;
        margin-top: 0.08rem;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }

    .point-value {
        font-size: 1.00rem;
        color: #4f5c57;
        margin-top: 0.16rem;
        line-height: 1.10;
    }

    .point-detail {
        font-size: 0.88rem;
        color: #6c7773;
        margin-top: 0.05rem;
        line-height: 1.08;
    }

    .section-note {
        font-size: 0.95rem;
        color: #69746f;
        line-height: 1.15;
        margin: -0.08rem 0 0.22rem;
    }

    .shape-list {
        font-size: 0.97rem;
        line-height: 1.30;
        color: #24302c;
    }

    /* Deductions: intentionally NOT big cards. */
    .deduction-item {
        border-bottom: 1px solid #dce3e0;
        padding: 0.16rem 0.12rem 0.17rem;
        margin: 0;
        min-height: 1.95rem;
    }

    .deduction-name {
        font-size: 1.03rem;
        font-weight: 680;
        line-height: 1.07;
    }

    .deduction-detail {
        font-size: 0.97rem;
        color: #6a7571;
        line-height: 1.05;
        margin-top: 0.06rem;
    }

    .combo-item {
        border-bottom: 1px solid #dce3e0;
        padding: 0.17rem 0.12rem 0.18rem;
        margin: 0;
    }

    .combo-name {
        font-size: 1.03rem;
        font-weight: 700;
        line-height: 1.08;
    }

    .combo-detail {
        font-size: 0.97rem;
        color: #68736f;
        line-height: 1.08;
        margin-top: 0.06rem;
    }

    div[data-testid="stAlert"] {
        padding-top: 0.42rem !important;
        padding-bottom: 0.42rem !important;
    }

    div[data-testid="stExpander"] {
        border-radius: 7px !important;
        margin-top: 0.18rem !important;
    }

    .stButton > button {
        height: 2.35rem;
        border-radius: 7px;
        font-size: 1.00rem;
        font-weight: 720;
    }


    /* Theme-colored primary action button */
    button[data-testid="stBaseButton-primary"],
    .stButton > button[kind="primary"] {
        background: #58786d !important;
        border: 1px solid #58786d !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    button[data-testid="stBaseButton-primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        background: #47655b !important;
        border-color: #47655b !important;
        color: #ffffff !important;
    }

    button[data-testid="stBaseButton-primary"]:focus,
    .stButton > button[kind="primary"]:focus {
        box-shadow: 0 0 0 0.16rem rgba(88, 120, 109, 0.22) !important;
    }

    @media (max-width: 760px) {
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }

        .block-container {
            width: 100% !important;
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


EVENT_LABELS = {
    "vault": "Vault",
    "bars": "Uneven Bars",
    "beam": "Balance Beam",
    "floor": "Floor Exercise",
}

ROTATION_SHORT = {
    "0": "No turn",
    "0.5": "½",
    "0.75": "¾",
    "1.0": "Full",
    "1.5": "1½",
    "2.0": "Double full",
    "2.5": "2½",
    "3.0": "Triple",
}


def rotation_short(value):
    return ROTATION_SHORT.get(str(value), f"{value} turn")


def rotation_dropdown(value):
    labels = {
        "0": "No turn",
        "0.5": "½ turn",
        "0.75": "¾ turn",
        "1.0": "1 full turn",
        "1.5": "1½ turns",
        "2.0": "2 full turns",
        "2.5": "2½ turns",
        "3.0": "3 full turns",
    }
    return labels.get(str(value), f"{value} turn(s)")


def difficulty_text(code):
    label = DIFFICULTY_LABELS.get(code, code)
    if code in {"M", "S", "HS", "AHS"}:
        return f"{label} ({code})"
    return label


def scoring_display(event, skill_id, difficulty):
    """
    Keep vault start values separate from bars/beam/floor routine difficulty credit.
    """
    if event == "vault":
        if skill_id == "front_handspring":
            return {
                "label": "Start value",
                "value": "8.60",
                "detail": "",
            }
        if skill_id == "straddle_vault":
            return {
                "label": "Start value",
                "value": "No current NFHS value",
                "detail": "",
            }
        return {
            "label": "Start value",
            "value": "See current vault table",
            "detail": "",
        }

    mapping = {
        "M": {
            "label": "Routine difficulty contribution",
            "value": "0.30",
            "detail": "",
        },
        "S": {
            "label": "Routine difficulty contribution",
            "value": "0.50",
            "detail": "",
        },
        "HS": {
            "label": "Routine difficulty contribution",
            "value": "0.30",
            "detail": "",
        },
        "AHS": {
            "label": "Routine difficulty contribution",
            "value": "0.30",
            "detail": "Potential AHS bonus: +0.20",
        },
        "NONE": {
            "label": "Routine difficulty contribution",
            "value": "0.00",
            "detail": "",
        },
        "NR": {
            "label": "Routine difficulty contribution",
            "value": "No current NFHS value",
            "detail": "",
        },
        "NA": {
            "label": "Routine difficulty contribution",
            "value": "—",
            "detail": "",
        },
    }

    return mapping.get(
        difficulty,
        {
            "label": "Routine difficulty contribution",
            "value": "—",
            "detail": "",
        },
    )


def skill_base_name(skill):
    return skill.get("display_alias", skill["name"])


def exact_variation_name(skill, rotation=None):
    base = skill_base_name(skill)

    if rotation is None or not skill.get("rotations"):
        return base

    alias = skill.get("rotation_aliases", {}).get(str(rotation))
    if alias:
        return f"{base} {rotation_short(rotation)} ({alias})"

    if str(rotation) == "0":
        return base

    return f"{base} {rotation_short(rotation)}"


def deduction_detail(item):
    bits = []
    if "value" in item:
        bits.append(f"{item['value']:.2f}")
    elif "max" in item:
        bits.append(f"up to {item['max']:.2f}")
    elif "range" in item:
        bits.append(f"{item['range'][0]:.2f}–{item['range'][1]:.2f}")
    if item.get("note"):
        bits.append(str(item["note"]))
    return " · ".join(bits)


def deduction_sort_value(item):
    """Highest possible numerical deduction first; unscored faults last."""
    if "value" in item:
        return float(item["value"])
    if "max" in item:
        return float(item["max"])
    if "range" in item and item["range"]:
        return float(max(item["range"]))
    return -1.0


def merged_deductions(event, skill_id, skill):
    result = []
    seen = set()

    def add(items):
        for raw in items:
            item = {"fault": raw} if isinstance(raw, str) else dict(raw)
            fault = item.get("fault", "").strip()
            key = fault.lower()

            if fault and key not in seen:
                result.append(item)
                seen.add(key)

    add(skill.get("deductions", []))

    for profile_name in deduction_profiles_for(event, skill_id, skill):
        add(DEDUCTION_PROFILES.get(profile_name, []))

    return sorted(
        result,
        key=lambda item: (
            deduction_sort_value(item),
            item.get("fault", "").lower(),
        ),
        reverse=True,
    )


def render_deductions(event, skill_id, skill):
    items = merged_deductions(event, skill_id, skill)

    st.subheader("Possible deductions / errors")

    cols = st.columns(3, gap="small")

    for i, item in enumerate(items):
        with cols[i % 3]:
            name = html.escape(item["fault"])
            detail = html.escape(deduction_detail(item))

            st.markdown(
                f"""
                <div class="deduction-item">
                    <div class="deduction-name">{name}</div>
                    <div class="deduction-detail">
                        {detail or "Possible execution deduction / error"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    return items


def combo_bonus(first_diff, second_diff):
    key = f"{first_diff}+{second_diff}"
    rule = COMBINATION_RULES["beam_or_floor_bbs"].get(key)

    if rule:
        return rule["label"], rule["bonus"]

    return "No BBS bonus in simplified NFHS logic", 0.0


def partner_ids(event, selected_id, selected_skill):
    category = selected_skill.get("category", "").lower()

    if event in {"beam", "floor"} and category in {"jump", "dance", "turn"}:
        return [
            sid
            for sid, data in SKILLS[event].items()
            if data.get("category", "").lower() in {"jump", "dance", "turn"}
        ]

    ids = list(selected_skill.get("connections", []))

    if event in {"beam", "floor"} and selected_id in {
        "back_walkover",
        "cartwheel",
        "front_handspring",
        "back_handspring",
    }:
        if selected_id not in ids:
            ids.insert(0, selected_id)

    return [sid for sid in ids if sid in SKILLS[event]]


def target_variations(skill):
    rotations = skill.get("rotations", {})

    if rotations:
        return list(rotations.items())

    return [(None, skill.get("difficulty", "NA"))]


def render_combinations(event, skill_id, skill, selected_rotation, selected_difficulty):
    st.subheader("Possible combinations")

    ids = partner_ids(event, skill_id, skill)

    if not ids:
        st.caption("No combinations stored for this skill.")
        return

    combo_skill_col, combo_rotation_col = st.columns([1.45, 1.0], gap="small")

    with combo_skill_col:
        target_id = st.selectbox(
            "Second skill",
            ids,
            format_func=lambda sid: skill_base_name(SKILLS[event][sid]),
            key=f"combo_skill_{event}_{skill_id}",
        )

    target = SKILLS[event][target_id]
    target_rots = target.get("rotations", {})

    with combo_rotation_col:
        if target_rots:
            target_rotation = st.selectbox(
                "Second-skill rotation",
                list(target_rots.keys()),
                format_func=rotation_dropdown,
                key=f"combo_rotation_{event}_{skill_id}_{target_id}",
            )
            target_diff = target_rots[target_rotation]
        else:
            target_rotation = None
            target_diff = target.get("difficulty", "NA")
            st.selectbox(
                "Second-skill rotation",
                ["Not applicable"],
                disabled=True,
                key=f"combo_rotation_na_{event}_{skill_id}_{target_id}",
            )

    first_name = exact_variation_name(skill, selected_rotation)
    second_name = exact_variation_name(target, target_rotation)

    label = "Direct combination"
    bonus = 0.0

    if event in {"beam", "floor"}:
        label, bonus = combo_bonus(selected_difficulty, target_diff)

        exception_key = f"{skill_id}+{target_id}"
        exception = COMBINATION_RULES.get(
            "beam_medium_acro_series_exceptions", {}
        ).get(exception_key)

        if event == "beam" and exception:
            label = exception

    bonus_text = (
        f"{label} · +{bonus:.2f}"
        if bonus > 0
        else label
    )

    st.markdown(
        f"""
        <div class="combo-item">
            <div class="combo-name">
                {html.escape(first_name)} → {html.escape(second_name)}
            </div>
            <div class="combo-detail">
                {html.escape(difficulty_text(selected_difficulty))}
                + {html.escape(difficulty_text(target_diff))}
                · {html.escape(bonus_text)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------
st.title("High School Gymnastics Skill Helper")

# ---------------------------------------------------------------------
# Event / Skill / Rotation: same row
# ---------------------------------------------------------------------
event_col, skill_col, rotation_col = st.columns(
    [1.0, 1.45, 1.0],
    gap="small",
)

with event_col:
    event = st.selectbox(
        "Event",
        list(EVENT_LABELS.keys()),
        format_func=lambda x: EVENT_LABELS[x],
    )

skills_for_event = SKILLS[event]

with skill_col:
    skill_id = st.selectbox(
        "Skill",
        list(skills_for_event.keys()),
        format_func=lambda x: skill_base_name(skills_for_event[x]),
    )

skill = skills_for_event[skill_id]
rotations = skill.get("rotations", {})

with rotation_col:
    if rotations:
        selected_rotation = st.selectbox(
            "Rotation",
            list(rotations.keys()),
            format_func=rotation_dropdown,
        )

        difficulty = difficulty_for_rotation(
            event,
            skill_id,
            selected_rotation,
        )
    else:
        selected_rotation = None

        st.selectbox(
            "Rotation",
            ["Not applicable"],
            disabled=True,
        )

        difficulty = skill.get("difficulty", "NA")

# ---------------------------------------------------------------------
# Summary / Difficulty
# ---------------------------------------------------------------------
summary_left, summary_right = st.columns([2.25, 1.25], gap="small")

with summary_left:
    exact_name = exact_variation_name(skill, selected_rotation)

    meta = [EVENT_LABELS[event]]
    if skill.get("display_alias") and skill["display_alias"] != skill["name"]:
        meta.append(f"Technical name: {skill['name']}")

    st.markdown(
        f"""
        <div class="summary-line">
            <div class="skill-name">{html.escape(exact_name)}</div>
            <div class="skill-meta">{html.escape(" · ".join(meta))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_right:
    scoring = scoring_display(event, skill_id, difficulty)

    detail_html = (
        f'<div class="point-detail">{html.escape(scoring["detail"])}</div>'
        if scoring["detail"]
        else ""
    )

    difficulty_html = f"""
    <div class="summary-line difficulty-panel">
        <div class="difficulty-title">Difficulty</div>
        <div class="difficulty-value">{html.escape(difficulty_text(difficulty))}</div>
        <div class="point-value">
            {html.escape(scoring["label"])}:
            <strong>{html.escape(scoring["value"])}</strong>
        </div>
        {detail_html}
    </div>
    """

    st.markdown(difficulty_html, unsafe_allow_html=True)

if skill.get("competition_status") == "not_recognized_nfhs_2026_28":
    st.warning(
        "This vault is kept as a teaching reference, but NFHS 2026–28 "
        "does not list the straddle/flight vault as a valued competition vault."
    )

# ---------------------------------------------------------------------
# How-to and form
# ---------------------------------------------------------------------
how_col, key_col = st.columns([1.7, 1.0], gap="small")

with how_col:
    st.subheader("How to perform it")
    st.write(skill.get("how_to", "Description not available."))

    if skill.get("hold_seconds", 0) > 0:
        st.caption(
            f"Expected hold: {skill['hold_seconds']} seconds in the final controlled position."
        )

with key_col:
    st.subheader("Key positions")

    if skill.get("key_shapes"):
        key_text = "<br>".join(
            f"• {html.escape(shape)}"
            for shape in skill["key_shapes"]
        )
        st.markdown(
            f'<div class="shape-list">{key_text}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption("No key positions stored.")

# ---------------------------------------------------------------------
# Deductions / combinations
# ---------------------------------------------------------------------
deductions = render_deductions(event, skill_id, skill)

render_combinations(
    event,
    skill_id,
    skill,
    selected_rotation,
    difficulty,
)

if skill.get("rule_note"):
    with st.expander("Rule note"):
        st.write(skill["rule_note"])

st.divider()

# ---------------------------------------------------------------------
# AI
# ---------------------------------------------------------------------
st.subheader("Skill analysis")

ai_left, ai_right = st.columns([1.4, 1.0], gap="small")

with ai_left:
    problem = st.text_area(
        "What is going wrong?",
        placeholder="Example: I get height but start twisting early and land off balance.",
    )

with ai_right:
    observed = st.multiselect(
        "Observed errors",
        [item["fault"] for item in deductions],
    )

if st.button("Analyze skill", type="primary", use_container_width=True):
    if not problem.strip() and not observed:
        st.warning("Describe the problem or choose at least one observed error.")

    elif not AI_AVAILABLE:
        st.info("Add ai_helper.py to enable analysis.")

    else:
        try:
            with st.spinner("Analyzing..."):
                result = analyze_skill(
                    api_key=st.secrets["GROQ_API_KEY"],
                    event=EVENT_LABELS[event],
                    skill_name=exact_variation_name(
                        skill,
                        selected_rotation,
                    ),
                    difficulty=difficulty_text(difficulty),
                    rotation=(
                        rotation_dropdown(selected_rotation)
                        if selected_rotation is not None
                        else None
                    ),
                    how_to=skill.get("how_to", ""),
                    key_shapes=skill.get("key_shapes", []),
                    observed_errors=observed,
                    gymnast_description=problem.strip(),
                )

            st.subheader("Analysis")
            st.markdown(result)

        except KeyError:
            st.error("GROQ_API_KEY is not configured in Streamlit Secrets.")

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")

