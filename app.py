
import html
import streamlit as st

from skills_data_v2 import (
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


# MUST be the first Streamlit command.
st.set_page_config(
    page_title="High School Gymnastics Skill Helper",
    page_icon="🤸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Compact, truly full-width styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Force the app to actually use the browser width. */
    .stApp {
        background: #eef3f1;
        color: #18211f;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: "Aptos", "Segoe UI", Arial, sans-serif !important;
    }

    [data-testid="stMain"] {
        width: 100% !important;
    }

    .block-container {
        width: 96% !important;
        max-width: 1600px !important;
        padding: 0.70rem 1.15rem 1.0rem !important;
        margin: 0 auto !important;
    }

    /* Compact text */
    h1 {
        font-size: 1.82rem !important;
        line-height: 1.05 !important;
        margin: 0 0 0.08rem 0 !important;
        letter-spacing: -0.025em;
    }

    h2 {
        font-size: 1.28rem !important;
        margin: 0.45rem 0 0.24rem !important;
    }

    h3 {
        font-size: 1.02rem !important;
        margin: 0.38rem 0 0.20rem !important;
    }

    p, li, label, .stMarkdown, .stCaption {
        line-height: 1.20 !important;
    }

    [data-testid="stCaptionContainer"] {
        margin-top: -0.15rem !important;
        margin-bottom: 0.20rem !important;
    }

    /* Keep widgets short */
    div[data-testid="stSelectbox"],
    div[data-testid="stMultiSelect"],
    div[data-testid="stTextArea"] {
        margin-bottom: 0.15rem !important;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stTextArea"] label {
        font-size: 0.79rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.04rem !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 2.15rem !important;
        height: 2.15rem !important;
        background: #ffffff !important;
        border-color: #cbd8d3 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span {
        font-size: 0.88rem !important;
    }

    textarea {
        min-height: 82px !important;
        line-height: 1.25 !important;
    }

    /* Tight column gaps. */
    [data-testid="stHorizontalBlock"] {
        gap: 0.65rem !important;
        align-items: flex-start !important;
    }

    hr {
        margin: 0.35rem 0 0.45rem !important;
        border-color: #d7e0dd !important;
    }

    .notice {
        background: #f8fbfa;
        border: 1px solid #d5dfdc;
        border-radius: 8px;
        padding: 0.40rem 0.60rem;
        font-size: 0.76rem;
        color: #5a6763;
        margin: 0.30rem 0 0.45rem;
    }

    .summary-card {
        background: #ffffff;
        border: 1px solid #d3ddda;
        border-radius: 10px;
        padding: 0.55rem 0.70rem;
        min-height: 70px;
    }

    .skill-name {
        font-size: 1.32rem;
        font-weight: 800;
        line-height: 1.08;
        margin-bottom: 0.18rem;
    }

    .skill-meta {
        font-size: 0.77rem;
        color: #67736f;
        line-height: 1.15;
    }

    .difficulty-card {
        background: #dfeae6;
        border: 1px solid #c7d8d2;
        border-radius: 10px;
        padding: 0.52rem 0.70rem;
        min-height: 70px;
    }

    .difficulty-kicker {
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-size: 0.68rem;
        font-weight: 800;
        color: #65716d;
        margin-bottom: 0.10rem;
    }

    .difficulty-full {
        font-size: 1.02rem !important;
        font-weight: 850;
        line-height: 1.12 !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        word-break: normal !important;
    }

    .shape-chip {
        display: inline-block;
        background: #e5eeeb;
        border: 1px solid #cedbd7;
        border-radius: 999px;
        padding: 0.18rem 0.38rem;
        margin: 0.05rem 0.08rem 0.05rem 0;
        font-size: 0.72rem;
        line-height: 1.1;
    }

    .deduction-card {
        background: #ffffff;
        border: 1px solid #d6dfdc;
        border-radius: 7px;
        padding: 0.34rem 0.46rem;
        margin: 0 0 0.22rem 0;
    }

    .deduction-name {
        font-size: 0.79rem;
        font-weight: 730;
        line-height: 1.07;
        margin: 0;
    }

    .deduction-detail {
        font-size: 0.66rem;
        color: #6a7672;
        line-height: 1.05;
        margin-top: 0.08rem;
    }

    .combo-card {
        background: #ffffff;
        border: 1px solid #d6dfdc;
        border-radius: 7px;
        padding: 0.34rem 0.46rem;
        margin: 0 0 0.22rem 0;
    }

    .combo-line {
        font-size: 0.78rem;
        font-weight: 760;
        line-height: 1.08;
    }

    .combo-detail {
        font-size: 0.66rem;
        color: #687470;
        line-height: 1.08;
        margin-top: 0.08rem;
    }

    .section-note {
        font-size: 0.70rem;
        color: #697570;
        line-height: 1.12;
        margin-top: -0.14rem;
        margin-bottom: 0.28rem;
    }

    div[data-testid="stExpander"] {
        border-radius: 8px !important;
    }

    .stButton > button {
        height: 2.25rem;
        border-radius: 8px;
        font-weight: 800;
    }

    /* Prevent Streamlit's usual early column stacking on normal laptop widths. */
    @media (min-width: 700px) {
        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
        }

        [data-testid="column"] {
            min-width: 0 !important;
            flex: 1 1 0 !important;
        }
    }

    @media (max-width: 699px) {
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


def skill_base_name(skill):
    return skill.get("display_alias", skill["name"])


def exact_variation_name(skill, rotation=None):
    """Name one exact variation, not just the skill family."""
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


def merged_deductions(event, skill_id, skill):
    """Skill-specific + researched event/category profiles, deduplicated."""
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

    return result


def render_deductions(event, skill_id, skill):
    items = merged_deductions(event, skill_id, skill)

    st.subheader("Possible deductions / errors")
    st.markdown(
        '<div class="section-note">Skill-specific faults plus relevant form, event, and landing errors.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="small")
    for i, item in enumerate(items):
        target = left if i % 2 == 0 else right
        with target:
            name = html.escape(item["fault"])
            detail = html.escape(deduction_detail(item))
            st.markdown(
                f"""
                <div class="deduction-card">
                    <div class="deduction-name">{name}</div>
                    <div class="deduction-detail">{detail or "Possible execution deduction / error"}</div>
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
    """
    Dance/jump/turn: show every exact rotation combination among the small
    project skill set, including same-skill combinations.
    Acro/bars: use stored realistic connections.
    """
    category = selected_skill.get("category", "").lower()

    if event in {"beam", "floor"} and category in {"jump", "dance", "turn"}:
        allowed_categories = {"jump", "dance", "turn"}
        return [
            sid for sid, data in SKILLS[event].items()
            if data.get("category", "").lower() in allowed_categories
        ]

    ids = list(selected_skill.get("connections", []))

    # Same-skill repetitions are useful for connected dance/jump series.
    if event in {"beam", "floor"} and category in {"acro", "acro flight"}:
        if selected_id in {"back_walkover", "cartwheel", "front_handspring", "back_handspring"}:
            if selected_id not in ids:
                ids.insert(0, selected_id)

    return [sid for sid in ids if sid in SKILLS[event]]


def target_variations(skill):
    rotations = skill.get("rotations", {})
    if rotations:
        return [(rot, diff) for rot, diff in rotations.items()]
    return [(None, skill.get("difficulty", "NA"))]


def render_combinations(event, skill_id, skill, selected_rotation, selected_difficulty):
    st.subheader("Possible combinations")
    st.markdown(
        '<div class="section-note">'
        'Each line is an exact combination. Rotation is shown for both skills when applicable.'
        '</div>',
        unsafe_allow_html=True,
    )

    ids = partner_ids(event, skill_id, skill)
    if not ids:
        st.caption("No combinations are stored for this skill.")
        return

    first_name = exact_variation_name(skill, selected_rotation)
    combos = []

    for target_id in ids:
        target = SKILLS[event][target_id]
        for target_rotation, target_diff in target_variations(target):
            second_name = exact_variation_name(target, target_rotation)

            label = "Direct combination"
            bonus = 0.0

            if event in {"beam", "floor"}:
                label, bonus = combo_bonus(selected_difficulty, target_diff)

                # Beam's selected-project medium acro exceptions.
                exception_key = f"{skill_id}+{target_id}"
                exception = COMBINATION_RULES.get(
                    "beam_medium_acro_series_exceptions", {}
                ).get(exception_key)
                if event == "beam" and exception:
                    label = exception

            combos.append(
                {
                    "name": f"{first_name} → {second_name}",
                    "difficulty": f"{difficulty_text(selected_difficulty)} + {difficulty_text(target_diff)}",
                    "label": label,
                    "bonus": bonus,
                }
            )

    # Two dense columns, all exact options visible.
    left, right = st.columns(2, gap="small")
    for i, combo in enumerate(combos):
        target = left if i % 2 == 0 else right
        bonus_text = (
            f"{combo['label']} · +{combo['bonus']:.2f}"
            if combo["bonus"] > 0
            else combo["label"]
        )
        with target:
            st.markdown(
                f"""
                <div class="combo-card">
                    <div class="combo-line">{html.escape(combo["name"])}</div>
                    <div class="combo-detail">
                        {html.escape(combo["difficulty"])} · {html.escape(bonus_text)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.title("🤸 High School Gymnastics Skill Helper")
st.caption("NFHS-focused reference for selected varsity gymnastics skills")
st.markdown(
    """
    <div class="notice">
    Educational reference only. Technique descriptions are coaching guidance;
    competition rulings should be verified against the current NFHS rules and state association.
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# ONE ROW: event + skill + rotation
# -----------------------------------------------------------------------------
event_col, skill_col, rotation_col = st.columns([1.0, 1.55, 1.0], gap="small")

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
            event, skill_id, selected_rotation
        )
    else:
        selected_rotation = None
        st.selectbox(
            "Rotation",
            ["Not applicable"],
            disabled=True,
        )
        difficulty = skill.get("difficulty", "NA")

st.divider()

# -----------------------------------------------------------------------------
# Compact summary row
# -----------------------------------------------------------------------------
summary_left, summary_right = st.columns([2.35, 1.35], gap="small")

with summary_left:
    exact_name = exact_variation_name(skill, selected_rotation)
    metadata = [EVENT_LABELS[event]]
    if skill.get("display_alias") and skill["display_alias"] != skill["name"]:
        metadata.append(f"Technical: {skill['name']}")

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="skill-name">{html.escape(exact_name)}</div>
            <div class="skill-meta">{html.escape(" · ".join(metadata))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_right:
    st.markdown(
        f"""
        <div class="difficulty-card">
            <div class="difficulty-kicker">Difficulty</div>
            <div class="difficulty-full">{html.escape(difficulty_text(difficulty))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if skill.get("competition_status") == "not_recognized_nfhs_2026_28":
    st.warning(
        "Straddle vault is kept here as a practice/teaching skill, but NFHS 2026–28 "
        "no longer lists the flight/straddle vault as a valued competition vault."
    )

# -----------------------------------------------------------------------------
# How-to + key shapes on one row
# -----------------------------------------------------------------------------
how_col, shape_col = st.columns([1.7, 1.0], gap="small")

with how_col:
    st.subheader("How to perform it")
    st.write(skill.get("how_to", "Description not available."))

    if skill.get("hold_seconds", 0) > 0:
        st.caption(
            f"Expected hold: {skill['hold_seconds']} seconds in the final controlled position."
        )

with shape_col:
    st.subheader("Key positions")
    chips = "".join(
        f'<span class="shape-chip">{html.escape(shape)}</span>'
        for shape in skill.get("key_shapes", [])
    )
    st.markdown(chips or "No key positions stored.", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Deductions and exact combinations
# -----------------------------------------------------------------------------
deductions = render_deductions(event, skill_id, skill)
render_combinations(
    event,
    skill_id,
    skill,
    selected_rotation,
    difficulty,
)

# Rule / safety notes side by side and collapsed.
if skill.get("rule_note") or skill.get("safety"):
    note_a, note_b = st.columns(2, gap="small")
    if skill.get("rule_note"):
        with note_a:
            with st.expander("Rule note"):
                st.write(skill["rule_note"])
    if skill.get("safety"):
        with note_b:
            with st.expander("Safety note"):
                st.write(skill["safety"])

st.divider()

# -----------------------------------------------------------------------------
# AI
# -----------------------------------------------------------------------------
st.subheader("AI Skill Analysis")

ai_left, ai_right = st.columns([1.45, 1.0], gap="small")
with ai_left:
    problem = st.text_area(
        "What is going wrong?",
        placeholder="Example: I get height but start twisting too early and land off balance.",
    )

with ai_right:
    observed = st.multiselect(
        "Observed errors",
        [item["fault"] for item in deductions],
    )

if st.button("Analyze My Skill", type="primary", use_container_width=True):
    if not problem.strip() and not observed:
        st.warning("Describe the problem or choose at least one observed error.")
    elif not AI_AVAILABLE:
        st.info("Add ai_helper.py to enable AI analysis.")
    else:
        try:
            with st.spinner("Analyzing your skill..."):
                result = analyze_skill(
                    api_key=st.secrets["GROQ_API_KEY"],
                    event=EVENT_LABELS[event],
                    skill_name=exact_variation_name(skill, selected_rotation),
                    difficulty=difficulty_text(difficulty),
                    rotation=rotation_dropdown(selected_rotation) if selected_rotation is not None else None,
                    how_to=skill.get("how_to", ""),
                    key_shapes=skill.get("key_shapes", []),
                    observed_errors=observed,
                    gymnast_description=problem.strip(),
                )
            st.subheader("AI Analysis")
            st.markdown(result)
        except KeyError:
            st.error("GROQ_API_KEY is not configured in Streamlit Secrets.")
        except Exception as exc:
            st.error(f"AI analysis failed: {exc}")

st.caption(
    "NFHS rules cycle targeted: 2026–28. State associations may adopt variations."
)
