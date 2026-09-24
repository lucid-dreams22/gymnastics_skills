"""
High School Gymnastics Skill Helper
Core skill database for a short NFHS-focused project.

Rules target:
    NFHS Girls Gymnastics, 2026-2028 rules cycle.

Important design choice:
    - "difficulty" is NFHS value-part difficulty: M, S, HS, AHS.
    - Vault does not use the same M/S/HS/AHS element system, so vault entries use
      competition_status/start-value notes instead.
    - Technique text below is plain-language coaching guidance, NOT quoted NFHS language.
    - Deductions combine NFHS execution concepts with skill-specific observable faults.
    - The selected skill list is intentionally limited to the project scope requested.

Before public deployment:
    State associations can adopt adaptations. Add a state selector later if needed.
"""

DIFFICULTY_LABELS = {
    "M": "Medium",
    "S": "Superior",
    "HS": "High Superior",
    "AHS": "Advanced High Superior",
    "NONE": "No standalone NFHS value part",
    "NA": "Not applicable",
    "NR": "Not recognized for current NFHS competition",
}

# General NFHS-style execution deductions useful across beam/floor/bar skills.
# These are stored separately so the UI can combine general + skill-specific faults.
GENERAL_DEDUCTIONS = {
    "form": [
        {"fault": "Bent legs/knees", "max": 0.30},
        {"fault": "Leg or knee separation when legs should be together", "max": 0.20},
        {"fault": "Incorrect foot form / relaxed feet", "max": 0.10},
        {"fault": "Incorrect body alignment or posture", "max": 0.20},
    ],
    "landing": [
        {"fault": "Slight hop / small adjustment / staggered feet", "max": 0.10},
        {"fault": "Small or medium step", "range": [0.10, 0.15], "note": "per step, subject to event maximum"},
        {"fault": "Large step or jump", "value": 0.20},
        {"fault": "Additional trunk movement to maintain balance", "max": 0.20},
        {"fault": "Squat on landing with hips lower than knees", "max": 0.30},
        {"fault": "Fall", "value": 0.50},
    ],
    "beam": [
        {"fault": "Balance error / wobble", "max": 0.30},
        {"fault": "Insufficient height on jump/leap/hop", "max": 0.20},
        {"fault": "Insufficient split when 180° is required", "max": 0.20},
    ],
    "floor": [
        {"fault": "Insufficient height on jump/leap/hop", "max": 0.20},
        {"fault": "Insufficient split when 180° is required", "max": 0.20},
    ],
    "bars": [
        {"fault": "Poor rhythm / hesitation in an element or connection", "max": 0.10},
        {"fault": "Extra swing", "value": 0.30},
        {"fault": "Bent arms in support", "max": 0.30},
        {"fault": "Bent legs", "max": 0.30},
        {"fault": "Leg or knee separation", "max": 0.20},
        {"fault": "Incorrect body shape / arch / pike", "max": 0.20},
    ],
}

# Connection-credit helper for the selected project scope.
# This lets the program compute a combo label instead of hard-coding every pair.
COMBINATION_RULES = {
    "beam_or_floor_bbs": {
        "S+S": {"label": "Low-level Back-to-Back Superior", "bonus": 0.10},
        "S+HS": {"label": "Low-level Back-to-Back Superior", "bonus": 0.10},
        "S+AHS": {"label": "Low-level Back-to-Back Superior", "bonus": 0.10},
        "HS+S": {"label": "Low-level Back-to-Back Superior", "bonus": 0.10},
        "AHS+S": {"label": "Low-level Back-to-Back Superior", "bonus": 0.10},
        "HS+HS": {"label": "High-level Back-to-Back Superior", "bonus": 0.20},
        "HS+AHS": {"label": "High-level Back-to-Back Superior", "bonus": 0.20},
        "AHS+HS": {"label": "High-level Back-to-Back Superior", "bonus": 0.20},
        "AHS+AHS": {"label": "High-level Back-to-Back Superior", "bonus": 0.20},
    },
    "beam_medium_acro_series_exceptions": {
        "cartwheel+cartwheel": "Series receives Superior difficulty",
        "back_walkover+back_walkover": "Series receives Superior difficulty",
        "cartwheel+back_walkover": "Series receives Superior difficulty",
        "back_walkover+cartwheel": "Series receives Superior difficulty",
    },
    "connection_breaks": [
        "A pause between directly connected elements can break the series.",
        "Pivoting on both feet between directly connected elements breaks the series.",
        "An extra step, hop, or repositioning that is not part of the next element can break the series.",
    ],
}


SKILLS = {
    # -------------------------------------------------------------------------
    # VAULT
    # -------------------------------------------------------------------------
    "vault": {
        "front_handspring": {
            "name": "Front Handspring Vault",
            "category": "vault",
            "competition_status": "recognized",
            "difficulty": "NA",
            "rotations": {},
            "how_to": (
                "Run with controlled speed into a hurdle and two-foot takeoff from the springboard. "
                "Reach long toward the table, contact with straight arms, and drive the shoulders open "
                "so the body passes through an extended inverted position. Block strongly through the "
                "shoulders and hands to create a distinct second flight, then keep the body tight and "
                "prepare to land on both feet with the chest controlled."
            ),
            "key_shapes": [
                "Two-foot board takeoff",
                "Straight arms on table contact",
                "Open shoulder angle",
                "Body passes through vertical",
                "Visible repulsion/block from the table",
                "Controlled two-foot landing",
            ],
            "deductions": [
                {"fault": "Legs crossed in flight", "max": 0.10},
                {"fault": "Leg separation", "max": 0.20},
                {"fault": "Bent knees", "max": 0.30},
                {"fault": "Piked hip angle in first flight", "max": 0.30},
                {"fault": "Bent arms during repulsion", "max": 0.50},
                {"fault": "Shoulder angle on table", "max": 0.20},
                {"fault": "Does not pass through vertical", "max": 0.30},
                {"fault": "Too long in support on table", "max": 0.50},
                {"fault": "Insufficient height in second flight", "max": 0.50},
                {"fault": "Insufficient distance in second flight", "max": 0.30},
                {"fault": "Direction error", "max": 0.30},
            ],
            "connections": [],
            "safety": "Train vault progressions only with a qualified gymnastics coach and appropriate matting."
        },
        "straddle_vault": {
            "name": "Straddle Vault",
            "category": "vault",
            "competition_status": "not_recognized_nfhs_2026_28",
            "difficulty": "NR",
            "rotations": {},
            "how_to": (
                "For practice only in programs that still teach it: approach the board, take off from "
                "two feet, place the hands on the apparatus, lift the hips and open the legs into a "
                "wide straddle as the body passes over, then bring the legs together for landing. "
                "This entry is retained in the app because it was specifically requested, but it is "
                "not a valued NFHS vault in the 2026-28 rules cycle."
            ),
            "key_shapes": ["Two-foot takeoff", "Straight-arm support", "Clear straddle over apparatus", "Controlled landing"],
            "deductions": [],
            "connections": [],
            "rule_note": "NFHS 2026 interpretation: flight/straddle vaults are no longer listed as valued vaults.",
            "safety": "Do not use this as a competition recommendation under current NFHS rules."
        },
    },

    # -------------------------------------------------------------------------
    # UNEVEN BARS
    # -------------------------------------------------------------------------
    "bars": {
        "pullover": {
            "name": "Pullover",
            "category": "support/circle",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Begin hanging from the bar. Lift the legs and hips toward the bar while pulling with "
                "straight-to-slightly-bent arms only as needed to keep the body close. Continue rotating "
                "the hips around the bar until the body arrives in a controlled front support with the "
                "arms straight and chest lifted away from the bar."
            ),
            "key_shapes": ["Hips stay close to bar", "Legs together", "Finish in straight-arm front support"],
            "deductions": [
                {"fault": "Bent knees"},
                {"fault": "Leg separation"},
                {"fault": "Resting chin/neck on bar"},
                {"fault": "Failure to finish in extended front support"},
                {"fault": "Poor rhythm or extra effort before support"},
            ],
            "connections": ["back_hip_circle", "squat_on"],
        },
        "back_hip_circle": {
            "name": "Back Hip Circle",
            "category": "hip circle",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Start in front support. Cast slightly away from the bar, return the hips to the bar, "
                "and rotate backward around it while keeping the body tight and the hips or upper thighs "
                "in contact. Shift the wrists as the body rises and finish again in a controlled front support."
            ),
            "key_shapes": ["Tight hollow body", "Neutral head", "Hips/upper thighs stay in contact", "Continuous circle"],
            "deductions": [
                {"fault": "Head thrown backward"},
                {"fault": "Piked or arched body"},
                {"fault": "Bent knees"},
                {"fault": "Loss of hip/upper-thigh contact"},
                {"fault": "Lack of continuity / stop in the circle"},
                {"fault": "Extra swing before the next skill", "value": 0.30},
            ],
            "connections": ["squat_on", "pullover"],
        },
        "squat_on": {
            "name": "Squat-On",
            "category": "transition",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "From front support, cast so the hips move away from the bar. As the body returns, bring "
                "both feet onto the bar together between or near the hands, bending the knees into a compact "
                "squat. Keep the weight controlled through the hands until the feet are securely placed, "
                "then rise or jump to the next action."
            ),
            "key_shapes": ["Controlled cast", "Both feet arrive together", "Weight controlled through hands", "No extra swing"],
            "deductions": [
                {"fault": "Feet arrive separately"},
                {"fault": "Bent-arm collapse"},
                {"fault": "Loss of balance on the bar"},
                {"fault": "Pause before initiating the squat-on", "max": 0.10},
                {"fault": "Extra swing before squat-on", "value": 0.30},
            ],
            "connections": ["tap_swing", "glide_kip"],
        },
        "glide_kip": {
            "name": "Glide Kip",
            "category": "kip",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Start from a hang and glide forward with the shoulders open and legs extended. At the end "
                "of the glide, bring the feet toward the bar while the shoulders begin to move behind it. "
                "Pull the bar toward the thighs as the hips rise, shift the wrists over the bar, and finish "
                "in a tall front support with straight arms."
            ),
            "key_shapes": ["Long glide", "Legs together", "Feet lead the closing action", "Bar stays close to legs", "Finish in support"],
            "deductions": [
                {"fault": "Insufficient extension at the end of the glide"},
                {"fault": "Bent knees"},
                {"fault": "Leg separation"},
                {"fault": "Early arm pull that shortens the glide"},
                {"fault": "Failure to finish in controlled front support"},
                {"fault": "Poor rhythm / hesitation", "max": 0.10},
            ],
            "connections": ["back_hip_circle", "squat_on"],
            "rule_note": "Low-bar kip is treated as Medium; long-hang kip on high bar is Superior."
        },
        "tap_swing": {
            "name": "Tap Swing",
            "category": "swing",
            "difficulty": "NONE",
            "rotations": {},
            "how_to": (
                "Hang with straight arms and allow the body to swing. Move through a controlled hollow-to-arch-to-hollow "
                "shape change so the tap happens through the bottom of the swing rather than by bending the knees or "
                "pulling with the arms. Keep the head neutral and the legs together so the swing remains long and efficient."
            ),
            "key_shapes": ["Straight arms", "Long body line", "Controlled hollow/arch timing", "Legs together", "Neutral head"],
            "deductions": [
                {"fault": "Bent knees"},
                {"fault": "Leg separation"},
                {"fault": "Excessive pike or arch"},
                {"fault": "Poor rhythm"},
                {"fault": "Extra forward-and-back tap swing not required for the next element", "value": 0.30},
            ],
            "connections": ["glide_kip"],
            "rule_note": "A plain tap swing is useful technique but should not be displayed as a standalone NFHS value part."
        },
    },

    # -------------------------------------------------------------------------
    # BALANCE BEAM
    # -------------------------------------------------------------------------
    "beam": {
        "tuck_jump": {
            "name": "Tuck Jump",
            "category": "jump",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "S",
                "0.75": "HS",
                "1.0": "AHS",
            },
            "how_to": (
                "Start tall with feet aligned on the beam. Bend through the ankles, knees, and hips, swing the arms, "
                "and jump upward from both feet. Lift both knees toward the chest while keeping the torso controlled. "
                "Open before landing and return both feet to the beam with the knees softly bent."
            ),
            "key_shapes": ["Two-foot takeoff", "Clear tuck shape", "Adequate height", "Complete rotation before landing"],
            "deductions": [
                {"fault": "Insufficient tuck shape"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Rotation incomplete"},
                {"fault": "Feet pivot on beam before takeoff", "note": "Can reduce credited rotation/value"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["tuck_jump", "straight_jump", "split_jump", "wolf_jump"],
        },
        "straight_jump": {
            "name": "Straight Jump",
            "category": "jump",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "M",
                "0.75": "S",
                "1.0": "HS",
                "1.5": "AHS",
            },
            "how_to": (
                "Stand tall with the body stacked over the feet. Use a small plié and arm swing to jump vertically. "
                "Keep the hips open, knees straight, legs together, and toes pointed in the air. Complete any selected "
                "turn in the air and land with the body centered over the beam."
            ),
            "key_shapes": ["Stretched body", "Legs together", "Pointed toes", "Turn completed in air"],
            "deductions": [
                {"fault": "Pike or arch instead of stretched position"},
                {"fault": "Bent knees"},
                {"fault": "Leg separation"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["tuck_jump", "split_jump", "wolf_jump"],
        },
        "split_jump": {
            "name": "Split Jump",
            "category": "jump",
            "difficulty": "S",
            "rotations": {
                "0": "S",
                "0.5": "HS",
                "0.75": "AHS",
            },
            "how_to": (
                "Take off from two feet and lift into a front-back split position. The front and back legs should be "
                "straight with pointed toes and the hips as square as possible. For the standard Superior version, "
                "show a 180° split. Rejoin the legs before landing with control."
            ),
            "key_shapes": ["Two-foot takeoff", "180° split for standard S value", "Straight knees", "Square hips"],
            "deductions": [
                {"fault": "Insufficient split angle", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Hips not square"},
                {"fault": "Incomplete turn"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["straight_jump", "tuck_jump", "wolf_jump", "straddle_jump"],
        },
        "straddle_jump": {
            "name": "Straddle Pike Jump",
            "display_alias": "Straddle Jump",
            "category": "jump",
            "difficulty": "HS",
            "rotations": {
                "0": "HS",
                "0.5": "AHS",
            },
            "how_to": (
                "Jump upward from two feet and open both straight legs sideways into a straddle while sharply closing "
                "at the hips into a pike. On beam, the straddle-pike expectation uses a wide split with the legs near "
                "horizontal. Reclose the legs before landing. A half-turn version is a higher-value variation."
            ),
            "key_shapes": ["Wide straddle", "Pike at hips", "Straight knees", "Legs near horizontal", "Controlled landing"],
            "deductions": [
                {"fault": "Insufficient straddle angle", "max": 0.20},
                {"fault": "Thighs too far below horizontal", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["split_jump", "tuck_jump", "straight_jump"],
        },
        "cat_leap": {
            "name": "Cat Leap",
            "category": "dance",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "S",
                "1.0": "HS",
                "1.5": "AHS",
            },
            "how_to": (
                "Travel from one foot to the other while lifting the knees one at a time in a cat-like action. "
                "The legs pass through bent positions rather than a split. Keep the torso lifted, point the toes, "
                "and complete any selected rotation before settling the landing."
            ),
            "key_shapes": ["Alternating bent-leg action", "Lifted torso", "Pointed toes", "Controlled landing"],
            "deductions": [
                {"fault": "Low knee lift"},
                {"fault": "Relaxed feet"},
                {"fault": "Poor body posture"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["straight_jump", "tuck_jump", "split_jump"],
        },
        "wolf_jump": {
            "name": "Wolf Jump",
            "category": "jump",
            "difficulty": "S",
            "rotations": {
                "0": "S",
                "0.5": "HS",
                "0.75": "AHS",
            },
            "how_to": (
                "Jump upward with one leg extended forward and the other leg bent underneath. Show the wolf shape "
                "clearly in the air, keeping the chest controlled and the extended leg high. Reclose the legs and "
                "land centered over the beam."
            ),
            "key_shapes": ["One leg extended forward", "Other leg bent", "Clear wolf shape", "Adequate height"],
            "deductions": [
                {"fault": "Extended leg too low"},
                {"fault": "Bent-leg thigh too low"},
                {"fault": "Poor body posture"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["tuck_jump", "straight_jump", "split_jump"],
        },
        "full_turn": {
            "name": "Full Turn",
            "category": "turn",
            "difficulty": "M",
            "rotations": {"1.0": "M"},
            "how_to": (
                "Stand on one foot with the body tall and the supporting leg controlled. Rise through the foot, spot "
                "the end of the beam, and rotate a full 360° on the supporting leg. Keep the free leg controlled and "
                "finish facing the original direction without stepping off line."
            ),
            "key_shapes": ["360° on one foot", "Tall posture", "Controlled free leg", "Finish without extra step"],
            "deductions": [
                {"fault": "Incomplete 360° turn"},
                {"fault": "Heel drops / turn travels"},
                {"fault": "Poor posture"},
                {"fault": "Free leg uncontrolled"},
                {"fault": "Balance check or extra step"},
            ],
            "connections": ["straight_jump", "split_jump"],
        },
        "handstand": {
            "name": "Handstand",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Start in a lunge, reach forward to place the hands in line on the beam, and kick one leg followed by "
                "the other to vertical. Stack wrists, shoulders, hips, and feet, keep the arms straight and push tall "
                "through the shoulders. Step down one foot at a time with control."
            ),
            "key_shapes": ["Hands aligned on beam", "Straight arms", "Vertical body line", "Tight core"],
            "deductions": [
                {"fault": "Does not reach vertical"},
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Arched or piked body"},
                {"fault": "Hands/feet not aligned with beam"},
                {"fault": "Balance error on step-down"},
            ],
            "connections": ["front_walkover", "back_walkover", "cartwheel"],
            "hold_seconds": 0,
            "hold_note": "For this app's basic handstand skill, no hold is required unless a specific rule/variation requires one."
        },
        "front_walkover": {
            "name": "Front Walkover",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Start in a lunge and reach to the beam while kicking the back leg overhead. Pass through a split "
                "handstand position, then continue the leading leg toward the beam. Push through the shoulders and "
                "hands as the second leg follows, lifting the chest to finish standing. A full 180° split should be "
                "shown during the walkover action."
            ),
            "key_shapes": ["Straight arms", "Passes through vertical", "180° split", "Controlled rise to stand"],
            "deductions": [
                {"fault": "Insufficient split", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Bent arms"},
                {"fault": "Does not pass through vertical"},
                {"fault": "Poor shoulder flexibility / closed shoulders"},
                {"fault": "Balance error on finish"},
            ],
            "connections": ["cartwheel", "back_walkover"],
        },
        "back_walkover": {
            "name": "Back Walkover",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Begin standing with one leg prepared to lift. Reach backward into a controlled arch as the free leg "
                "kicks overhead. Place the hands on the beam, pass through a split handstand with straight arms and "
                "a 180° split, then lower one foot and then the other to finish standing."
            ),
            "key_shapes": ["Controlled backward reach", "Straight arms", "180° split", "Passes through vertical"],
            "deductions": [
                {"fault": "Insufficient split", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Bent arms"},
                {"fault": "Hands miss beam centerline"},
                {"fault": "Does not pass through vertical"},
                {"fault": "Balance error on finish"},
            ],
            "connections": ["back_walkover", "cartwheel"],
        },
        "cartwheel": {
            "name": "Cartwheel",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Begin in a lunge. Reach one hand and then the other onto the beam as the legs kick overhead in a "
                "sideward plane. Pass through vertical with the legs separated and knees straight. Place the first "
                "foot and then the second foot back onto the beam and finish under control."
            ),
            "key_shapes": ["Sideward action", "Sequential hand placement", "Pass through vertical", "Straight legs"],
            "deductions": [
                {"fault": "Does not pass through vertical"},
                {"fault": "Bent knees"},
                {"fault": "Bent arms"},
                {"fault": "Poor hand placement"},
                {"fault": "Legs do not separate clearly"},
                {"fault": "Balance error on landing"},
            ],
            "connections": ["cartwheel", "back_walkover", "roundoff_dismount"],
        },

        # Four simple balance/hold skills. These are intentionally basic user-facing entries.
        "arabesque": {
            "name": "Arabesque Hold",
            "category": "balance",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Stand on one leg and extend the free leg straight behind the body while keeping the torso lifted. "
                "Keep the hips as square as possible, point the back foot, and hold the position without stepping."
            ),
            "hold_seconds": 2,
            "key_shapes": ["One-leg balance", "Free leg extended behind", "Square hips", "Still 2-second hold"],
            "deductions": [
                {"fault": "Hold shorter than 2 seconds"},
                {"fault": "Free leg drops"},
                {"fault": "Support foot moves"},
                {"fault": "Bent free leg"},
                {"fault": "Large torso adjustment"},
            ],
            "connections": [],
            "note": "Simple app-level balance entry; exact NFHS VP depends on the recognized balance position/amplitude."
        },
        "scale": {
            "name": "Scale",
            "category": "balance",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Balance on one leg while extending the free leg backward and lifting it to at least horizontal. "
                "Lengthen through the standing leg and torso, keep the free knee straight, and hold the final "
                "position steadily for two seconds."
            ),
            "hold_seconds": 2,
            "key_shapes": ["Free leg at/above horizontal", "Straight knees", "Controlled torso", "2-second hold"],
            "deductions": [
                {"fault": "Hold shorter than 2 seconds"},
                {"fault": "Free leg below required height"},
                {"fault": "Bent knees"},
                {"fault": "Support foot moves"},
                {"fault": "Balance check"},
            ],
            "connections": [],
        },
        "knee_scale": {
            "name": "Knee Scale",
            "category": "balance",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Lower into a controlled kneeling balance with one knee supported on the beam and extend the other leg "
                "to create a clear line. Keep the torso lifted, hips controlled, and hold the final position for two seconds."
            ),
            "hold_seconds": 2,
            "key_shapes": ["Controlled kneeling support", "Extended free leg", "Still torso", "2-second hold"],
            "deductions": [
                {"fault": "Hold shorter than 2 seconds"},
                {"fault": "Bent or relaxed free leg"},
                {"fault": "Poor posture"},
                {"fault": "Hands touch beam for balance when not part of variation"},
                {"fault": "Loss of balance"},
            ],
            "connections": [],
            "note": "Kept as a beginner-friendly project skill; verify exact state/NFHS recognition before treating as a competition VP."
        },
        "leg_hold": {
            "name": "Leg Hold Balance",
            "category": "balance",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Stand on one leg and lift the free leg forward or to the side. Hold the raised leg with the hand if "
                "needed for the selected recognized variation, keep the support leg tall, and maintain the final "
                "position for two seconds without hopping or turning."
            ),
            "hold_seconds": 2,
            "key_shapes": ["One-leg support", "Raised free leg", "Tall posture", "2-second hold"],
            "deductions": [
                {"fault": "Hold shorter than 2 seconds"},
                {"fault": "Raised leg too low"},
                {"fault": "Support foot moves or hops"},
                {"fault": "Bent support leg"},
                {"fault": "Loss of balance"},
            ],
            "connections": [],
        },

        "roundoff_dismount": {
            "name": "Roundoff Dismount",
            "category": "dismount",
            "difficulty": "S",
            "rotations": {},
            "how_to": (
                "Approach the end of the beam with a controlled step or lunge, place the hands onto the beam as in a "
                "cartwheel, turn the body so the legs snap together through vertical, and push through the shoulders "
                "to leave the beam. Land on two feet facing back toward the beam or according to the recognized variation."
            ),
            "key_shapes": ["Pass through vertical", "Legs snap together", "Strong shoulder push", "Two-foot landing"],
            "deductions": [
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Legs fail to join"},
                {"fault": "Insufficient push/flight"},
                {"fault": "Direction error"},
                {"fault": "Landing step/hop/fall"},
            ],
            "connections": [],
        },
        "front_tuck_dismount": {
            "name": "Front Tuck Dismount",
            "category": "dismount",
            "difficulty": "S",
            "rotations": {},
            "how_to": (
                "Take off from the end of the beam with the chest lifted and arms driving upward. Create height first, "
                "then pull into a compact tuck and rotate forward. Open before the floor, prepare the feet underneath "
                "the body, and land with the chest controlled."
            ),
            "key_shapes": ["Upward lift before tuck", "Compact tuck", "Adequate rotation", "Open before landing"],
            "deductions": [
                {"fault": "Insufficient height"},
                {"fault": "Loose/incorrect tuck position"},
                {"fault": "Bent or separated legs beyond tuck shape"},
                {"fault": "Insufficient opening before landing"},
                {"fault": "Under/over-rotation"},
                {"fault": "Landing step/hop/fall"},
            ],
            "connections": [],
            "safety": "Salto dismounts require qualified coaching and appropriate landing mats."
        },
        "back_tuck_dismount": {
            "name": "Back Tuck Dismount",
            "category": "dismount",
            "difficulty": "S",
            "rotations": {},
            "how_to": (
                "From a stable takeoff at the end of the beam, jump upward and slightly away from the beam. Keep the "
                "chest lifted as the hips and knees close into a tuck, rotate backward, then open in time to see and "
                "absorb the landing on both feet."
            ),
            "key_shapes": ["Lift upward first", "Compact tuck", "Clearance from beam", "Open for landing"],
            "deductions": [
                {"fault": "Insufficient height or distance"},
                {"fault": "Loose tuck"},
                {"fault": "Early head throw"},
                {"fault": "Insufficient opening before landing"},
                {"fault": "Under/over-rotation"},
                {"fault": "Landing step/hop/fall"},
            ],
            "connections": [],
            "safety": "Salto dismounts require qualified coaching and appropriate landing mats."
        },
    },

    # -------------------------------------------------------------------------
    # FLOOR EXERCISE
    # -------------------------------------------------------------------------
    "floor": {
        "tuck_jump": {
            "name": "Tuck Jump",
            "category": "jump",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "M",
                "1.0": "S",
                "1.5": "HS",
                "2.0": "AHS",
            },
            "how_to": (
                "Jump vertically from two feet. Lift both knees toward the chest to show a clear tuck while keeping "
                "the torso controlled. Complete any selected twist in the air, then open the hips and knees before "
                "landing softly on both feet."
            ),
            "key_shapes": ["Two-foot takeoff", "Clear tuck", "Adequate height", "Rotation finished before landing"],
            "deductions": [
                {"fault": "Insufficient tuck shape"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
                {"fault": "Poor landing control"},
            ],
            "connections": ["straight_jump", "split_jump", "straddle_jump", "wolf_jump"],
        },
        "straight_jump": {
            "name": "Straight / Stretched Jump",
            "category": "jump",
            "difficulty": "M",
            "rotations": {
                "1.0": "M",
                "1.5": "S",
                "2.0": "HS",
                "3.0": "AHS",
            },
            "how_to": (
                "Jump upward from two feet with the body fully stretched, legs together, knees straight, and toes pointed. "
                "For twisting versions, keep the body tight around the vertical axis and finish the rotation before landing."
            ),
            "key_shapes": ["Stretched body", "Legs together", "Pointed toes", "Controlled twist"],
            "deductions": [
                {"fault": "Pike or arch in stretched position"},
                {"fault": "Bent knees"},
                {"fault": "Leg separation"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
            ],
            "connections": ["tuck_jump", "split_jump", "straddle_jump"],
        },
        "split_jump": {
            "name": "Split Jump",
            "category": "jump",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "S",
                "1.0": "HS",
                "1.5": "AHS",
            },
            "how_to": (
                "Take off from two feet and open into a 180° front-back split in the air. Keep both knees straight, "
                "point the toes, and keep the hips square. Complete any selected rotation in the air and rejoin the "
                "legs before landing."
            ),
            "key_shapes": ["180° split", "Straight knees", "Square hips", "Pointed toes"],
            "deductions": [
                {"fault": "Insufficient split", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
                {"fault": "Poor landing control"},
            ],
            "connections": ["straight_jump", "straddle_jump", "wolf_jump"],
        },
        "straddle_jump": {
            "name": "Straddle Pike Jump",
            "display_alias": "Straddle Jump",
            "category": "jump",
            "difficulty": "S",
            "rotations": {
                "0": "S",
                "0.5": "S",
                "1.0": "HS",
                "1.5": "AHS",
            },
            "rotation_aliases": {
                "1.0": "Popa",
            },
            "how_to": (
                "Jump from two feet, lift the legs sideways into a wide straddle, and close the hips into a clear pike "
                "while keeping the knees straight and toes pointed. Bring the legs back together before landing. "
                "The full-turn version is commonly called a Popa."
            ),
            "key_shapes": ["Wide straddle", "Clear pike", "Straight knees", "Pointed toes"],
            "deductions": [
                {"fault": "Insufficient straddle angle"},
                {"fault": "Legs too low"},
                {"fault": "Bent knees"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Incomplete turn"},
            ],
            "connections": ["split_jump", "straight_jump", "tuck_jump"],
        },
        "cat_leap": {
            "name": "Cat Leap",
            "category": "dance",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "M",
                "1.0": "S",
                "1.5": "HS",
                "2.0": "AHS",
            },
            "how_to": (
                "Travel from one foot to the other while lifting the knees sequentially in bent positions. Keep the "
                "upper body tall, point the toes, and make the leg action clear rather than allowing it to look like "
                "ordinary running steps."
            ),
            "key_shapes": ["Alternating bent legs", "Lifted torso", "Pointed toes", "Visible flight"],
            "deductions": [
                {"fault": "Low knee lift"},
                {"fault": "Insufficient height"},
                {"fault": "Relaxed feet"},
                {"fault": "Poor posture"},
                {"fault": "Incomplete turn"},
            ],
            "connections": ["straight_jump", "split_jump"],
        },
        "wolf_jump": {
            "name": "Wolf Jump",
            "category": "jump",
            "difficulty": "M",
            "rotations": {
                "0": "M",
                "0.5": "S",
                "1.0": "HS",
                "1.5": "AHS",
            },
            "how_to": (
                "Jump upward with one leg extended forward and the other leg bent underneath. Lift the legs high enough "
                "to show a recognizable wolf shape while keeping the torso controlled. Rejoin the legs and prepare for "
                "a balanced landing."
            ),
            "key_shapes": ["One leg straight forward", "Other leg bent", "Clear wolf position", "Adequate height"],
            "deductions": [
                {"fault": "Extended leg too low"},
                {"fault": "Bent-leg thigh too low"},
                {"fault": "Insufficient height", "max": 0.20},
                {"fault": "Poor posture"},
                {"fault": "Incomplete turn"},
            ],
            "connections": ["tuck_jump", "split_jump", "straight_jump"],
        },

        "turn_1_5": {
            "name": "1½ Turn",
            "category": "turn",
            "difficulty": "S",
            "rotations": {"1.5": "S"},
            "how_to": (
                "Rise onto one supporting foot, keep the body vertically stacked, and rotate 540° around the body's "
                "vertical axis. Keep the free leg controlled and finish the turn without hopping, traveling, or taking "
                "an extra corrective step."
            ),
            "key_shapes": ["540° rotation", "One-foot support", "Tall axis", "Controlled finish"],
            "deductions": [
                {"fault": "Incomplete rotation"},
                {"fault": "Traveling turn"},
                {"fault": "Hopping on support foot"},
                {"fault": "Poor posture"},
                {"fault": "Extra step on finish"},
            ],
            "connections": [],
        },
        "double_turn": {
            "name": "Double Turn",
            "category": "turn",
            "difficulty": "HS",
            "rotations": {"2.0": "HS"},
            "how_to": (
                "Rise onto one supporting foot and rotate two complete turns, or 720°, around a tall vertical axis. "
                "Spot the direction of travel, keep the free leg and arms controlled, and finish without an extra hop "
                "or step."
            ),
            "key_shapes": ["720° rotation", "One-foot support", "Tall posture", "Controlled finish"],
            "deductions": [
                {"fault": "Incomplete rotation"},
                {"fault": "Traveling or hopping"},
                {"fault": "Poor body alignment"},
                {"fault": "Free leg uncontrolled"},
                {"fault": "Extra step on finish"},
            ],
            "connections": [],
        },

        "handstand": {
            "name": "Handstand",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Begin in a lunge, reach to the floor, and kick through to a vertical upside-down position with the "
                "hands shoulder-width apart. Push tall through straight arms, stack the hips over the shoulders, keep "
                "the legs together and toes pointed, then step down under control."
            ),
            "key_shapes": ["Vertical line", "Straight arms", "Tight core", "Legs together"],
            "deductions": [
                {"fault": "Does not reach vertical"},
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Arched or piked body"},
                {"fault": "Leg separation"},
            ],
            "connections": ["handstand_forward_roll", "front_walkover", "cartwheel"],
        },
        "handstand_forward_roll": {
            "name": "Handstand Forward Roll",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Kick to a controlled handstand. From vertical, lean the shoulders slightly forward, bend the arms "
                "gradually, tuck the chin, and round the upper back so the body rolls smoothly over the shoulders. "
                "Keep the movement continuous and finish standing without collapsing onto the head."
            ),
            "key_shapes": ["Controlled handstand", "Chin tucked", "Rounded roll", "Continuous finish"],
            "deductions": [
                {"fault": "Handstand does not reach vertical"},
                {"fault": "Head contacts floor heavily"},
                {"fault": "Bent knees"},
                {"fault": "Loss of control entering roll"},
                {"fault": "Extra hands/steps to stand"},
            ],
            "connections": [],
        },
        "cartwheel": {
            "name": "Cartwheel",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Start in a lunge, place one hand and then the other on the floor, and kick the legs over the body in "
                "a sideward plane. Pass through an inverted position with straight legs separated, then land one foot "
                "and then the other in a controlled lunge."
            ),
            "key_shapes": ["Sideward plane", "Sequential hands", "Straight legs", "Passes through vertical"],
            "deductions": [
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Does not pass through vertical"},
                {"fault": "Poor hand/foot line"},
                {"fault": "Loss of control on finish"},
            ],
            "connections": ["roundoff", "back_walkover", "front_walkover"],
        },
        "roundoff": {
            "name": "Roundoff",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Hurdle into a cartwheel-like entry. Place the hands on the floor, turn the body as the legs snap "
                "together overhead, and push strongly through the shoulders. Land on both feet together facing the "
                "direction you came from, ideally with rebound available for a following skill."
            ),
            "key_shapes": ["Fast hurdle", "Legs snap together", "Strong block", "Two-foot landing"],
            "deductions": [
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Legs join late"},
                {"fault": "Poor shoulder block"},
                {"fault": "Landing feet apart or with poor direction"},
            ],
            "connections": ["back_handspring"],
        },
        "front_walkover": {
            "name": "Front Walkover",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Step into a lunge, reach to the floor, and kick the back leg overhead. Pass through a split handstand "
                "with straight arms and a 180° split, then lower the lead foot and push through the shoulders to lift "
                "the chest as the second foot finishes the walkover."
            ),
            "key_shapes": ["Straight arms", "180° split", "Passes through vertical", "Controlled finish"],
            "deductions": [
                {"fault": "Insufficient split", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Bent arms"},
                {"fault": "Poor shoulder flexibility"},
                {"fault": "Loss of control on finish"},
            ],
            "connections": ["front_handspring", "cartwheel"],
        },
        "back_walkover": {
            "name": "Back Walkover",
            "category": "acro",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Lift one leg and reach backward into a bridge-like position as the free leg kicks overhead. Place the "
                "hands on the floor, pass through a split handstand with straight arms and a 180° split, then step one "
                "foot and then the other down to finish standing."
            ),
            "key_shapes": ["Controlled back reach", "Straight arms", "180° split", "Passes through vertical"],
            "deductions": [
                {"fault": "Insufficient split", "max": 0.20},
                {"fault": "Bent knees"},
                {"fault": "Bent arms"},
                {"fault": "Poor shoulder opening"},
                {"fault": "Loss of control on finish"},
            ],
            "connections": ["back_handspring", "cartwheel"],
        },
        "front_handspring": {
            "name": "Front Handspring",
            "category": "acro flight",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Hurdle or step into a strong forward lunge, reach to the floor, and kick through a fast handstand. "
                "Block through straight arms and open shoulders so the hands leave the floor before the feet land. "
                "Keep the body extended through the flight and land with the chest rising."
            ),
            "key_shapes": ["Fast entry", "Straight arms", "Shoulder block", "Clear flight after hand support"],
            "deductions": [
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Insufficient flight"},
                {"fault": "Closed shoulder angle"},
                {"fault": "Pike/arch error"},
                {"fault": "Poor landing control"},
            ],
            "connections": ["front_handspring"],
        },
        "back_handspring": {
            "name": "Back Handspring",
            "category": "acro flight",
            "difficulty": "M",
            "rotations": {},
            "how_to": (
                "Sit the hips slightly while swinging the arms, then jump backward rather than straight down. Reach "
                "through the shoulders to place the hands on the floor with straight arms. Snap the legs and hips over "
                "the hands, push through the shoulders, and bring the feet down together to finish or rebound."
            ),
            "key_shapes": ["Backward jump", "Open shoulders", "Straight arms", "Fast snap-down", "Two-foot landing"],
            "deductions": [
                {"fault": "Sits too low before takeoff"},
                {"fault": "Jumps upward instead of backward"},
                {"fault": "Bent arms"},
                {"fault": "Bent knees"},
                {"fault": "Insufficient flight"},
                {"fault": "Pike/arch error"},
                {"fault": "Feet land apart"},
            ],
            "connections": ["back_handspring"],
        },
        "front_aerial": {
            "name": "Front Aerial",
            "category": "acro flight",
            "difficulty": "HS",
            "rotations": {},
            "how_to": (
                "Drive forward from a strong step or lunge and kick the back leg aggressively overhead while the torso "
                "reaches forward. The movement resembles a front walkover but the hands do not touch the floor. Pass "
                "through a split position in the air and land one foot at a time with the chest lifting."
            ),
            "key_shapes": ["No hand support", "Strong split action", "Adequate height", "One-foot-at-a-time landing"],
            "deductions": [
                {"fault": "Hands touch floor"},
                {"fault": "Insufficient split"},
                {"fault": "Bent knees"},
                {"fault": "Insufficient height"},
                {"fault": "Low chest / poor landing control"},
            ],
            "connections": ["cartwheel", "front_walkover"],
            "safety": "Aerial skills require qualified coaching and appropriate progressions."
        },
        "side_aerial": {
            "name": "Side Aerial",
            "category": "acro flight",
            "difficulty": "HS",
            "rotations": {},
            "how_to": (
                "Enter as for a powerful cartwheel, but drive the legs and hips fast enough that the body rotates "
                "sideways without the hands touching the floor. Keep the legs straight and separated through the "
                "inverted phase, then land one foot followed by the other."
            ),
            "key_shapes": ["Sideward rotation", "No hand support", "Straight separated legs", "Controlled one-two landing"],
            "deductions": [
                {"fault": "Hands touch floor"},
                {"fault": "Bent knees"},
                {"fault": "Insufficient height"},
                {"fault": "Poor leg separation"},
                {"fault": "Low chest / loss of control on landing"},
            ],
            "connections": ["cartwheel", "back_walkover"],
            "safety": "Aerial skills require qualified coaching and appropriate progressions."
        },
    },
}



# -------------------------------------------------------------------------
# V2 deduction profiles and data corrections
# -------------------------------------------------------------------------
# These profiles are intentionally separated from each skill's own list:
# they let the UI build a more comprehensive "possible deductions/errors"
# list without copy/pasting identical judging faults into every element.
#
# Numerical values are only included when the NFHS material used for this
# project supports a general deduction value/range. Other entries are kept
# as observable faults without inventing a number.

DEDUCTION_PROFILES = {
    "universal_form": [
        {"fault": "Bent knees / legs", "max": 0.30},
        {"fault": "Leg or knee separation when legs should be together", "max": 0.20},
        {"fault": "Relaxed / incorrect foot form", "max": 0.10},
        {"fault": "Incorrect body alignment / posture", "max": 0.20},
        {"fault": "Insufficient extension / amplitude"},
        {"fault": "Poor control at completion"},
    ],
    "jump_dance": [
        {"fault": "Insufficient height / amplitude", "max": 0.20},
        {"fault": "Incomplete turn / twist"},
        {"fault": "Turn begins before takeoff is complete"},
        {"fault": "Incorrect body shape for the named jump"},
        {"fault": "Poor arm position / uncontrolled arms"},
        {"fault": "Landing with feet apart when together is expected"},
    ],
    "split_shape": [
        {"fault": "Insufficient split angle", "max": 0.20},
        {"fault": "Bent knees in split position"},
        {"fault": "Uneven / unsquare hips"},
        {"fault": "Back leg or front leg below required position"},
    ],
    "straddle_shape": [
        {"fault": "Insufficient straddle width / split angle", "max": 0.20},
        {"fault": "Legs below required horizontal position", "max": 0.20},
        {"fault": "Insufficient pike at hips"},
        {"fault": "Bent knees in straddle"},
        {"fault": "Asymmetrical leg height"},
    ],
    "wolf_shape": [
        {"fault": "Extended leg too low"},
        {"fault": "Bent leg does not show clear wolf position"},
        {"fault": "Torso drops excessively"},
        {"fault": "Loss of body shape during turn"},
    ],
    "turn": [
        {"fault": "Incomplete rotation"},
        {"fault": "Turn travels away from starting point"},
        {"fault": "Supporting heel drops early"},
        {"fault": "Hop on supporting foot"},
        {"fault": "Free leg changes position / is uncontrolled"},
        {"fault": "Extra step at completion"},
        {"fault": "Poor vertical body alignment"},
    ],
    "hand_support_acro": [
        {"fault": "Bent arms during hand support", "max": 0.30},
        {"fault": "Shoulders not fully open"},
        {"fault": "Does not pass through vertical when required"},
        {"fault": "Head out / poor head position"},
        {"fault": "Hands placed too wide, crooked, or off line"},
        {"fault": "Legs bend during inversion", "max": 0.30},
        {"fault": "Leg separation incorrect for skill"},
        {"fault": "Pike / arch error through inversion"},
        {"fault": "Loss of rhythm / hesitation"},
    ],
    "walkover": [
        {"fault": "Insufficient split through handstand", "max": 0.20},
        {"fault": "Shoulders close during support"},
        {"fault": "Hands or feet land off line"},
        {"fault": "Pause in the middle of the walkover"},
        {"fault": "Chest remains low on finish"},
    ],
    "handspring": [
        {"fault": "Insufficient flight"},
        {"fault": "Weak / late shoulder block"},
        {"fault": "Hands remain on floor too long"},
        {"fault": "Feet land too close to hands"},
        {"fault": "Body pikes during snap-down / landing"},
        {"fault": "Insufficient rebound / continuation when connected"},
    ],
    "aerial": [
        {"fault": "Hands touch floor"},
        {"fault": "Insufficient height / flight"},
        {"fault": "Bent knees", "max": 0.30},
        {"fault": "Insufficient leg separation"},
        {"fault": "Low chest on landing"},
        {"fault": "Direction / alignment error"},
    ],
    "balance": [
        {"fault": "Hold shorter than required time"},
        {"fault": "Supporting foot moves / pivots"},
        {"fault": "Free leg drops during hold"},
        {"fault": "Bent support or free leg"},
        {"fault": "Large arm / torso correction"},
        {"fault": "Loss of balance / step off"},
    ],
    "beam_execution": [
        {"fault": "Balance error / wobble", "max": 0.30},
        {"fault": "Extra step / foot adjustment"},
        {"fault": "Pause that breaks a directly connected series"},
        {"fault": "Pivot on both feet that breaks a directly connected series"},
        {"fault": "Fall", "value": 0.50},
    ],
    "floor_execution": [
        {"fault": "Poor landing control"},
        {"fault": "Out-of-control step / lunge after landing"},
        {"fault": "Fall", "value": 0.50},
    ],
    "landing": [
        {"fault": "Slight hop / small adjustment / staggered feet", "max": 0.10},
        {"fault": "Small or medium step", "range": [0.10, 0.15], "note": "per step, subject to event maximum"},
        {"fault": "Large step or jump", "value": 0.20},
        {"fault": "Additional trunk movement to maintain balance", "max": 0.20},
        {"fault": "Squat landing with hips lower than knees", "max": 0.30},
        {"fault": "Fall", "value": 0.50},
    ],
    "bars_execution": [
        {"fault": "Poor rhythm / hesitation", "max": 0.10},
        {"fault": "Extra swing not needed for the next element", "value": 0.30},
        {"fault": "Bent arms in support", "max": 0.30},
        {"fault": "Bent legs", "max": 0.30},
        {"fault": "Leg / knee separation", "max": 0.20},
        {"fault": "Incorrect arch / hollow / pike body shape", "max": 0.20},
        {"fault": "Insufficient swing amplitude"},
        {"fault": "Head thrown out of neutral"},
        {"fault": "Loss of grip / fall", "value": 0.50},
    ],
    "vault_handspring": [
        {"fault": "Incorrect hurdle / board contact"},
        {"fault": "Takeoff not from two feet"},
        {"fault": "Legs crossed in first or second flight", "max": 0.10},
        {"fault": "Leg separation", "max": 0.20},
        {"fault": "Bent knees", "max": 0.30},
        {"fault": "Piked hip angle in first flight", "max": 0.30},
        {"fault": "Bent arms during support / repulsion", "max": 0.50},
        {"fault": "Closed shoulder angle on table", "max": 0.20},
        {"fault": "Does not pass through vertical", "max": 0.30},
        {"fault": "Prolonged support / insufficient block", "max": 0.50},
        {"fault": "Insufficient second-flight height", "max": 0.50},
        {"fault": "Insufficient second-flight distance", "max": 0.30},
        {"fault": "Direction / alignment error", "max": 0.30},
        {"fault": "Touches table with only one hand", "value": 1.00},
    ],
    # The straddle/flight vault is retained only because this project wants
    # to teach it. NFHS 2026-28 no longer gives it a vault value.
    "straddle_vault_practice": [
        {"fault": "Incorrect hurdle / board contact"},
        {"fault": "Takeoff not from two feet"},
        {"fault": "Bent arms in support"},
        {"fault": "Hands placed unevenly / off center"},
        {"fault": "Hips do not rise sufficiently above the apparatus"},
        {"fault": "Insufficient straddle width"},
        {"fault": "Bent knees during straddle"},
        {"fault": "Uneven / asymmetrical legs"},
        {"fault": "Feet or legs contact the apparatus"},
        {"fault": "Insufficient push away from the apparatus"},
        {"fault": "Legs do not rejoin before landing"},
        {"fault": "Direction / alignment error"},
        {"fault": "Poor landing control"},
        {"fault": "Small / medium landing step"},
        {"fault": "Large landing step / jump"},
        {"fault": "Deep squat on landing"},
        {"fault": "Fall"},
    ],
    "dismount": [
        {"fault": "Insufficient height"},
        {"fault": "Insufficient distance from beam"},
        {"fault": "Incomplete rotation"},
        {"fault": "Poor body shape in flight"},
        {"fault": "Late opening before landing"},
        {"fault": "Under-rotation / over-rotation"},
        {"fault": "Direction error"},
    ],
}


def deduction_profiles_for(event: str, skill_id: str, skill: dict):
    """Return profile names relevant to this exact skill."""
    profiles = []
    category = skill.get("category", "").lower()

    if event == "vault":
        if skill_id == "straddle_vault":
            return ["straddle_vault_practice", "landing"]
        return ["vault_handspring", "landing"]

    profiles.append("universal_form")

    if event == "bars":
        profiles.append("bars_execution")
        return profiles

    if event == "beam":
        profiles.append("beam_execution")
    elif event == "floor":
        profiles.append("floor_execution")

    if category in {"jump", "dance"}:
        profiles.append("jump_dance")
    if "turn" in category:
        profiles.append("turn")
    if "balance" in category:
        profiles.append("balance")
    if category in {"acro", "acro flight", "dismount"}:
        profiles.append("hand_support_acro")
    if "walkover" in skill_id:
        profiles.append("walkover")
    if "handspring" in skill_id:
        profiles.append("handspring")
    if "aerial" in skill_id:
        profiles.append("aerial")
    if "dismount" in skill_id:
        profiles.append("dismount")

    if skill_id == "split_jump":
        profiles.append("split_shape")
    if skill_id == "straddle_jump":
        profiles.append("straddle_shape")
    if skill_id == "wolf_jump":
        profiles.append("wolf_shape")

    if event in {"beam", "floor"} and category not in {"balance"}:
        profiles.append("landing")

    return profiles


# Make the retained straddle-vault entry useful in the app while making
# its current competition status unmistakable.
SKILLS["vault"]["straddle_vault"]["deductions"] = DEDUCTION_PROFILES["straddle_vault_practice"]
SKILLS["vault"]["straddle_vault"]["rule_note"] = (
    "Practice reference only: NFHS 2026-28 no longer lists the straddle/flight "
    "vault as a valued vault, so these are technique faults rather than a current "
    "NFHS competition deduction table for that vault."
)

SOURCE_NOTES = {
    "rules_cycle": "NFHS Girls Gymnastics 2026-2028",
    "official_sources": [
        "NFHS 2026-2028 Cue Sheets",
        "NFHS Girls Gymnastics Rules Changes - 2026-28",
        "NFHS Girls Gymnastics Rules Interpretations - 2026",
        "NFHS 2024-26 Judges Manual / Cue Sheets where 2026-28 public change notices did not alter the selected element",
        "NFHS 2024-2026 Supplemental Explanations",
    ],
    "important_current_rules": [
        "Vault takeoff must be from two feet under the 2026-28 rule change.",
        "Straddle/flight vault is no longer a valued NFHS vault in 2026-28.",
        "A pivot or pause can break a directly connected series.",
        "A tuck jump 3/4 on beam is HS; if the feet pivot before takeoff and only 1/2 is completed, it is credited as S.",
        "A plain tap swing can create an extra-swing deduction if it is not required for the next element.",
    ],
}


def get_skill(event: str, skill_id: str):
    return SKILLS[event][skill_id]


def difficulty_for_rotation(event: str, skill_id: str, rotations: float | str | None = None):
    skill = get_skill(event, skill_id)
    if rotations is None or not skill.get("rotations"):
        return skill["difficulty"]

    key = str(rotations)
    # normalize "1" -> "1.0"
    if key not in skill["rotations"]:
        try:
            f = float(rotations)
            key = str(f)
        except (TypeError, ValueError):
            pass
    return skill["rotations"].get(key)


def combo_credit(difficulty_a: str, difficulty_b: str):
    key = f"{difficulty_a}+{difficulty_b}"
    return COMBINATION_RULES["beam_or_floor_bbs"].get(
        key,
        {"label": "No BBS bonus in simplified rule set", "bonus": 0.0},
    )


def list_skill_options(event: str):
    return [(skill_id, data["name"]) for skill_id, data in SKILLS[event].items()]


# =========================================================================
# 2026-28 DIFFICULTY AUDIT + SELECTED SKILL EXPANSION
# =========================================================================
# Audit basis:
# - NFHS 2026-28 rules changes state that the only element-table changes are
#   Vault Boxes 6.6.1/6.6.3 and Beam Box 8.6.1 (mounts).
# - Therefore the 2024-26 NFHS element tables remain applicable to the
#   selected non-mount bars/beam/floor elements unless a 2026 interpretation
#   says otherwise.
# - Generic practice balances that are not tied to one uniquely identified
#   NFHS value-part illustration are NOT assigned a made-up difficulty.

# ---- Corrections to existing skills -------------------------------------

# Bars
SKILLS["bars"]["pullover"]["difficulty"] = "M"
SKILLS["bars"]["back_hip_circle"]["difficulty"] = "M"

# A cast squat-on is treated as Superior in current NFHS routine examples
# tied to the NFHS cue sheet.
SKILLS["bars"]["squat_on"]["difficulty"] = "S"

# Keep low-bar glide kip separate from the explicitly Superior long-hang kip.
SKILLS["bars"]["glide_kip"]["difficulty"] = "M"
SKILLS["bars"]["tap_swing"]["difficulty"] = "NONE"

# Beam dance values: audited against NFHS beam cue sheet / 2026 interpretation.
SKILLS["beam"]["tuck_jump"]["difficulty"] = "M"
SKILLS["beam"]["tuck_jump"]["rotations"] = {
    "0": "M", "0.5": "S", "0.75": "HS", "1.0": "AHS"
}
SKILLS["beam"]["straight_jump"]["difficulty"] = "M"
SKILLS["beam"]["straight_jump"]["rotations"] = {
    "0": "M", "0.5": "M", "0.75": "S", "1.0": "HS", "1.5": "AHS"
}
SKILLS["beam"]["split_jump"]["difficulty"] = "S"
SKILLS["beam"]["split_jump"]["rotations"] = {
    "0": "S", "0.5": "HS", "0.75": "AHS"
}
SKILLS["beam"]["straddle_jump"]["difficulty"] = "HS"
SKILLS["beam"]["straddle_jump"]["rotations"] = {
    "0": "HS", "0.5": "AHS"
}
SKILLS["beam"]["cat_leap"]["difficulty"] = "M"
SKILLS["beam"]["cat_leap"]["rotations"] = {
    "0": "M", "0.5": "S", "1.0": "HS", "1.5": "AHS"
}
SKILLS["beam"]["wolf_jump"]["difficulty"] = "S"
SKILLS["beam"]["wolf_jump"]["rotations"] = {
    "0": "S", "0.5": "HS", "0.75": "AHS"
}
SKILLS["beam"]["full_turn"]["difficulty"] = "M"

# Basic non-flight acro.
for _id in ["handstand", "front_walkover", "back_walkover", "cartwheel"]:
    SKILLS["beam"][_id]["difficulty"] = "M"

# These four were intentionally added as beginner practice balances earlier.
# The names are not specific enough to guarantee one unique NFHS value-part
# illustration, so do not pretend they have an official M/S/HS/AHS value.
for _id in ["arabesque", "scale", "knee_scale", "leg_hold"]:
    SKILLS["beam"][_id]["difficulty"] = "NONE"
    SKILLS["beam"][_id]["note"] = (
        "Practice balance reference. This generic name is not mapped to a single "
        "verified NFHS value-part illustration."
    )

# Selected dismounts retained in this short project.
SKILLS["beam"]["roundoff_dismount"]["difficulty"] = "S"
SKILLS["beam"]["front_tuck_dismount"]["difficulty"] = "S"
SKILLS["beam"]["back_tuck_dismount"]["difficulty"] = "S"

# Floor dance values: audited against the NFHS floor difficulty table.
SKILLS["floor"]["tuck_jump"]["difficulty"] = "M"
SKILLS["floor"]["tuck_jump"]["rotations"] = {
    "0": "M", "0.5": "M", "1.0": "S", "1.5": "HS", "2.0": "AHS"
}
SKILLS["floor"]["straight_jump"]["difficulty"] = "M"
SKILLS["floor"]["straight_jump"]["rotations"] = {
    "1.0": "M", "1.5": "S", "2.0": "HS", "3.0": "AHS"
}
SKILLS["floor"]["split_jump"]["difficulty"] = "M"
SKILLS["floor"]["split_jump"]["rotations"] = {
    "0": "M", "0.5": "S", "1.0": "HS", "1.5": "AHS"
}
SKILLS["floor"]["straddle_jump"]["difficulty"] = "S"
SKILLS["floor"]["straddle_jump"]["rotations"] = {
    "0": "S", "0.5": "S", "1.0": "HS", "1.5": "AHS"
}
SKILLS["floor"]["cat_leap"]["difficulty"] = "M"
SKILLS["floor"]["cat_leap"]["rotations"] = {
    "0": "M", "0.5": "M", "1.0": "S", "1.5": "HS", "2.0": "AHS"
}
SKILLS["floor"]["wolf_jump"]["difficulty"] = "M"
SKILLS["floor"]["wolf_jump"]["rotations"] = {
    "0": "M", "0.5": "S", "1.0": "HS", "1.5": "AHS"
}
SKILLS["floor"]["turn_1_5"]["difficulty"] = "S"
SKILLS["floor"]["double_turn"]["difficulty"] = "HS"

for _id in [
    "handstand", "handstand_forward_roll", "cartwheel", "roundoff",
    "front_walkover", "back_walkover", "front_handspring", "back_handspring"
]:
    SKILLS["floor"][_id]["difficulty"] = "M"

# Directly connected aerial examples in NFHS guidance are S + S, so each
# selected aerial is Superior, not High Superior.
SKILLS["floor"]["front_aerial"]["difficulty"] = "S"
SKILLS["floor"]["side_aerial"]["difficulty"] = "S"


# ---- Five additional UNEVEN BARS skills --------------------------------

SKILLS["bars"].update({
    "long_hang_kip": {
        "name": "Long-Hang Kip",
        "category": "kip",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Begin in a long hang on the high bar. Swing forward with a long body line, "
            "bring the toes toward the bar as the swing returns, then pull the bar toward "
            "the thighs while shifting the wrists over it. Finish in a controlled clear "
            "support with straight arms."
        ),
        "key_shapes": [
            "Long forward swing", "Legs together", "Feet close toward bar",
            "Bar stays close to thighs", "Straight-arm finish"
        ],
        "deductions": [
            {"fault": "Insufficient extension in the long swing"},
            {"fault": "Bent knees"},
            {"fault": "Leg separation"},
            {"fault": "Early arm pull"},
            {"fault": "Failure to finish in controlled support"},
        ],
        "connections": ["clear_hip_circle", "cast_handstand", "giant", "tuck_flyaway"],
    },
    "cast_handstand": {
        "name": "Cast to Handstand",
        "category": "cast",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "From front support, push the hips away from the bar and drive the legs upward "
            "while keeping the arms straight. Open the shoulders and hips as the body rises "
            "to a straight handstand line over the bar. Control the return or continue "
            "directly into the next element."
        ),
        "key_shapes": [
            "Straight arms", "Open shoulders", "Tight body line",
            "Legs together", "Handstand within required vertical range"
        ],
        "deductions": [
            {"fault": "Cast does not rise close enough to vertical"},
            {"fault": "Bent arms"},
            {"fault": "Bent knees"},
            {"fault": "Leg separation"},
            {"fault": "Piked or arched body"},
        ],
        "connections": ["giant", "clear_hip_circle", "squat_on"],
        "rule_note": "A cast reaching within 20° of vertical can receive Superior credit."
    },
    "clear_hip_circle": {
        "name": "Clear Hip Circle",
        "category": "clear circle",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "From support or a cast, allow the body to circle backward around the bar while "
            "keeping the hips clear of contact. Maintain straight arms and a tight body line, "
            "then open the shoulders and hips to finish in clear support or handstand."
        ),
        "key_shapes": [
            "Hips remain clear of bar", "Straight arms", "Continuous backward circle",
            "Open shoulders on finish", "Finish in clear support or handstand"
        ],
        "deductions": [
            {"fault": "Hips contact the bar"},
            {"fault": "Insufficient amplitude"},
            {"fault": "Bent arms"},
            {"fault": "Bent knees"},
            {"fault": "Pike / arch error"},
            {"fault": "Failure to finish in clear support"},
        ],
        "connections": ["long_hang_kip", "cast_handstand", "giant"],
    },
    "giant": {
        "name": "Backward Giant",
        "category": "giant",
        "difficulty": "HS",
        "rotations": {},
        "how_to": (
            "From a handstand or long swing, rotate completely around the high bar with "
            "straight arms. Use a controlled hollow-to-arch-to-hollow tap through the bottom "
            "and keep the body extended as the shoulders rise back toward handstand."
        ),
        "key_shapes": [
            "Straight arms throughout", "Long body line", "Controlled tap",
            "Body returns close to vertical", "Legs together"
        ],
        "deductions": [
            {"fault": "Does not finish within required range of vertical"},
            {"fault": "Bent arms"},
            {"fault": "Bent knees"},
            {"fault": "Leg separation"},
            {"fault": "Excessive pike / arch"},
            {"fault": "Poor rhythm through the bottom"},
        ],
        "connections": ["giant", "tuck_flyaway", "cast_handstand"],
    },
    "tuck_flyaway": {
        "name": "Tuck Flyaway",
        "category": "dismount",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Use the final high-bar swing to create height away from the bar. Release after "
            "the body has risen, bring the knees toward the chest into a compact tuck, rotate "
            "backward, then open before landing on both feet."
        ),
        "key_shapes": [
            "Adequate release height", "Clear distance from bar",
            "Compact tuck", "Open before landing", "Two-foot landing"
        ],
        "deductions": [
            {"fault": "Release too early or too late"},
            {"fault": "Insufficient height"},
            {"fault": "Insufficient distance from bar"},
            {"fault": "Loose tuck shape"},
            {"fault": "Late opening"},
            {"fault": "Under- or over-rotation"},
        ],
        "connections": [],
    },
})


# ---- Five additional BALANCE BEAM skills -------------------------------

SKILLS["beam"].update({
    "back_handspring": {
        "name": "Back Handspring",
        "category": "acro flight",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "From a controlled standing position, sit slightly through the hips and jump "
            "backward along the beam. Reach for the beam with straight arms, pass through "
            "an inverted position, then snap the legs down to land in line on the beam."
        ),
        "key_shapes": [
            "Backward flight", "Straight arms", "Open shoulders",
            "Tight inverted line", "Feet return to beam centerline"
        ],
        "deductions": [
            {"fault": "Insufficient flight"},
            {"fault": "Bent arms"},
            {"fault": "Bent knees"},
            {"fault": "Hands placed off line"},
            {"fault": "Pike / arch error"},
            {"fault": "Feet land off beam centerline"},
        ],
        "connections": ["back_handspring", "back_walkover", "back_tuck_dismount"],
        "rule_note": (
            "A single back handspring is Superior. Under the NFHS beam special connection "
            "rule, its value can increase when it is the first element directly connected "
            "to another qualifying acro element."
        )
    },
    "front_handspring": {
        "name": "Front Handspring",
        "category": "acro flight",
        "difficulty": "HS",
        "rotations": {},
        "how_to": (
            "Step or hurdle into a long lunge, place the hands in line on the beam, and kick "
            "through vertical. Block strongly through straight arms and open shoulders so "
            "there is visible flight before the feet return to the beam."
        ),
        "key_shapes": [
            "Hands aligned on beam", "Straight arms", "Pass through vertical",
            "Visible flight", "Controlled landing"
        ],
        "deductions": [
            {"fault": "Insufficient flight"},
            {"fault": "Bent arms"},
            {"fault": "Bent knees"},
            {"fault": "Does not pass through vertical"},
            {"fault": "Closed shoulder angle"},
            {"fault": "Landing off line"},
        ],
        "connections": ["front_walkover", "cartwheel", "front_tuck_dismount"],
    },
    "front_aerial": {
        "name": "Front Aerial",
        "category": "acro flight",
        "difficulty": "AHS",
        "rotations": {},
        "how_to": (
            "Drive from a strong step or lunge and kick the back leg aggressively overhead "
            "as the torso reaches forward. Pass through a split position without placing "
            "the hands on the beam, then land one foot at a time in line."
        ),
        "key_shapes": [
            "No hand support", "Strong split action", "Adequate flight",
            "Straight legs", "Controlled one-two landing"
        ],
        "deductions": [
            {"fault": "Hands touch the beam"},
            {"fault": "Insufficient flight"},
            {"fault": "Insufficient split"},
            {"fault": "Bent knees"},
            {"fault": "Landing off line"},
        ],
        "connections": ["front_walkover", "cartwheel"],
    },
    "side_aerial": {
        "name": "Side Aerial",
        "category": "acro flight",
        "difficulty": "AHS",
        "rotations": {},
        "how_to": (
            "Enter with a strong sideward cartwheel action and drive the legs fast enough "
            "to rotate over the beam without hand support. Keep the legs straight and "
            "separated through inversion, then place the feet back onto the beam one at a time."
        ),
        "key_shapes": [
            "No hand support", "Sideward flight", "Straight separated legs",
            "Body passes inverted", "Feet land in line"
        ],
        "deductions": [
            {"fault": "Hands touch the beam"},
            {"fault": "Insufficient flight"},
            {"fault": "Bent knees"},
            {"fault": "Poor leg separation"},
            {"fault": "Direction error / landing off line"},
        ],
        "connections": ["cartwheel", "back_walkover"],
    },
    "switch_leap": {
        "name": "Switch Leap 180°",
        "category": "dance",
        "difficulty": "HS",
        "rotations": {
            "0": "HS",
            "0.5": "AHS",
        },
        "how_to": (
            "Take off from one foot after swinging the lead leg forward. Switch the legs "
            "in the air so the opposite leg becomes the front leg, and show a full 180° "
            "split before landing on one foot. Keep the torso lifted and knees straight."
        ),
        "key_shapes": [
            "Clear leg switch", "180° split", "Straight knees",
            "Lifted torso", "Controlled one-foot landing"
        ],
        "deductions": [
            {"fault": "Insufficient initial lead-leg swing"},
            {"fault": "Insufficient split", "max": 0.20},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height", "max": 0.20},
            {"fault": "Incomplete turn"},
            {"fault": "Balance error on landing"},
        ],
        "connections": ["split_jump", "wolf_jump", "tuck_jump", "switch_leap"],
    },
})


# ---- Five additional FLOOR EXERCISE skills -----------------------------

SKILLS["floor"].update({
    "pike_jump": {
        "name": "Pike Jump 90°",
        "category": "jump",
        "difficulty": "M",
        "rotations": {
            "0": "M", "0.5": "S", "1.0": "HS", "1.5": "AHS"
        },
        "how_to": (
            "Jump upward from two feet and lift both straight legs together in front while "
            "closing at the hips to about 90°. Keep the knees straight and toes pointed, "
            "then open the hips before landing."
        ),
        "key_shapes": [
            "Two-foot takeoff", "About 90° hip closure",
            "Straight together legs", "Pointed toes", "Controlled landing"
        ],
        "deductions": [
            {"fault": "Insufficient pike closure"},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height", "max": 0.20},
            {"fault": "Leg separation"},
            {"fault": "Incomplete turn"},
        ],
        "connections": ["tuck_jump", "split_jump", "straddle_jump", "wolf_jump"],
    },
    "split_leap": {
        "name": "Split Leap 180°",
        "category": "dance",
        "difficulty": "M",
        "rotations": {
            "0": "M", "0.5": "S", "1.0": "HS"
        },
        "how_to": (
            "Take off from one foot and travel forward while opening the legs into a 180° "
            "front-back split. Keep both knees straight, toes pointed, and the torso lifted, "
            "then land on the opposite foot with control."
        ),
        "key_shapes": [
            "One-foot takeoff", "180° split", "Straight knees",
            "Square hips", "One-foot landing"
        ],
        "deductions": [
            {"fault": "Insufficient split", "max": 0.20},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height", "max": 0.20},
            {"fault": "Hips not square"},
            {"fault": "Incomplete turn"},
        ],
        "connections": ["switch_leap", "split_jump", "straddle_jump", "wolf_jump"],
    },
    "switch_leap": {
        "name": "Switch Leap 180°",
        "category": "dance",
        "difficulty": "S",
        "rotations": {
            "0": "S", "0.5": "HS", "1.0": "AHS"
        },
        "how_to": (
            "Swing the lead leg forward, take off from the opposite foot, then switch the "
            "legs in the air so the other leg becomes the front leg. Show a full 180° split "
            "after the switch and land on one foot without breaking the travel."
        ),
        "key_shapes": [
            "Clear switch action", "180° split", "Straight knees",
            "Lifted torso", "Continuous travel"
        ],
        "deductions": [
            {"fault": "Lead leg does not swing clearly before switch"},
            {"fault": "Insufficient split", "max": 0.20},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height", "max": 0.20},
            {"fault": "Incomplete turn"},
        ],
        "connections": ["split_leap", "split_jump", "switch_leap"],
    },
    "stag_split_jump": {
        "name": "Stag Split Jump 180°",
        "category": "jump",
        "difficulty": "M",
        "rotations": {
            "0": "M", "0.5": "S"
        },
        "how_to": (
            "Jump from two feet and open into a split position with one leg bent in a clear "
            "stag shape while the other leg extends. Show the required split amplitude, "
            "keep the shape deliberate, then reclose the legs for landing."
        ),
        "key_shapes": [
            "Clear stag shape", "180° split line", "Controlled torso",
            "Pointed toes", "Two-foot landing"
        ],
        "deductions": [
            {"fault": "Stag shape is unclear"},
            {"fault": "Insufficient split", "max": 0.20},
            {"fault": "Insufficient height", "max": 0.20},
            {"fault": "Poor leg form"},
            {"fault": "Incomplete turn"},
        ],
        "connections": ["split_jump", "split_leap", "straddle_jump"],
    },
    "double_stag_jump": {
        "name": "Double Stag Jump",
        "category": "jump",
        "difficulty": "M",
        "rotations": {
            "0": "M", "0.5": "M", "1.0": "S"
        },
        "how_to": (
            "Jump from two feet and bend both legs into a clear double-stag position while "
            "maintaining height through the torso. Keep the shape controlled and symmetrical, "
            "then open the legs before landing."
        ),
        "key_shapes": [
            "Two-foot takeoff", "Both legs show stag shape",
            "Adequate height", "Controlled torso", "Stable landing"
        ],
        "deductions": [
            {"fault": "Double-stag shape is unclear"},
            {"fault": "Leg positions are asymmetrical"},
            {"fault": "Insufficient height", "max": 0.20},
            {"fault": "Poor foot form"},
            {"fault": "Incomplete turn"},
        ],
        "connections": ["tuck_jump", "split_jump", "stag_split_jump"],
    },
})


# Compact audit metadata for UI/debugging and future maintenance.
DIFFICULTY_AUDIT = {
    "rules_cycle": "NFHS 2026-28",
    "notes": [
        "2026-28 element changes affect selected vault boxes and Beam Box 8.6.1 (mounts); this project does not include beam mounts.",
        "Beam tuck jump 3/4 is HS; tuck jump 1/2 is S per 2026 NFHS interpretation.",
        "Floor front and side aerials corrected from HS to S.",
        "Generic beam practice balances are no longer assigned invented NFHS difficulty values.",
        "Straddle/flight vault remains in the app only as a practice reference and has no current NFHS value.",
    ],
}


# =========================================================================
# FLOOR SALTOS — VERIFIED / HIGH-SCHOOL-RELEVANT SET
# =========================================================================
# Difficulty references:
# - Basic front/back saltos are Superior in NFHS high-school routine examples.
# - Stretched forward salto (front layout) is explicitly Superior in the
#   2026 NFHS interpretation.
# - Back layout 1/2 is explicitly Superior in NFHS supplemental evaluation.
# - Back salto 1/1 = HS (9.301).
# - Front salto 1/1 or more = AHS (8.401).
# - Back salto 1 1/2 or more = AHS (9.401).
# - Double front = AHS (8.403).
# - Double back = AHS (9.403).

# A salto-specific profile. These are observable execution faults; numerical
# deductions are only attached where a general NFHS value is already used.
DEDUCTION_PROFILES["salto"] = [
    {"fault": "Insufficient height / amplitude", "max": 0.20},
    {"fault": "Takeoff is not fully extended before rotation"},
    {"fault": "Head thrown backward / forward to initiate rotation"},
    {"fault": "Loose or incorrect body position"},
    {"fault": "Bent knees when a straight or piked shape is required", "max": 0.30},
    {"fault": "Leg separation when legs should remain together", "max": 0.20},
    {"fault": "Relaxed / incorrect foot form", "max": 0.10},
    {"fault": "Body position changes too early"},
    {"fault": "Insufficient opening before landing"},
    {"fault": "Under-rotation"},
    {"fault": "Over-rotation"},
    {"fault": "Low chest on landing"},
    {"fault": "Poor direction / travels off line"},
]


SKILLS["floor"].update({

    # ------------------------------------------------------------------
    # FORWARD SALTOS
    # ------------------------------------------------------------------
    "front_tuck": {
        "name": "Front Tuck",
        "category": "salto",
        "direction": "forward",
        "body_position": "tuck",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Use a controlled run and hurdle into a two-foot punch. Drive upward through "
            "the legs and arms before beginning the forward rotation. Bring the knees toward "
            "the chest into a compact tuck while keeping the chest lifted through takeoff. "
            "Open the tuck before the floor and prepare to land on both feet."
        ),
        "key_shapes": [
            "Two-foot punch",
            "Upward lift before rotation",
            "Compact tuck",
            "Knees together",
            "Open before landing",
        ],
        "deductions": [
            {"fault": "Rotation begins before full takeoff"},
            {"fault": "Insufficient height"},
            {"fault": "Loose tuck"},
            {"fault": "Knees separate"},
            {"fault": "Late opening"},
            {"fault": "Low chest on landing"},
        ],
        "connections": [
            "front_tuck", "front_pike", "front_layout",
            "roundoff", "front_handspring"
        ],
    },

    "front_pike": {
        "name": "Front Pike",
        "category": "salto",
        "direction": "forward",
        "body_position": "pike",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Punch from two feet and create height before rotating forward. Keep the knees "
            "straight and close the hips into a clear pike while the legs stay together. "
            "Maintain the pike through the main part of the rotation, then open the hips "
            "early enough to prepare for a controlled landing."
        ),
        "key_shapes": [
            "Two-foot punch",
            "Straight knees",
            "Clear pike at hips",
            "Legs together",
            "Visible opening before landing",
        ],
        "deductions": [
            {"fault": "Insufficient pike position"},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height"},
            {"fault": "Pike opens too early"},
            {"fault": "Late opening"},
            {"fault": "Low chest on landing"},
        ],
        "connections": [
            "front_tuck", "front_layout", "roundoff", "front_handspring"
        ],
    },

    "front_layout": {
        "name": "Front Layout",
        "category": "salto",
        "direction": "forward",
        "body_position": "stretched",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Punch upward from two feet and maintain a stretched body line while rotating "
            "forward. Keep the hips open, core tight, legs together, and knees straight. "
            "Avoid folding at the hips to create the rotation. Prepare the feet underneath "
            "the body for landing as the rotation finishes."
        ),
        "key_shapes": [
            "Strong upward punch",
            "Open hips",
            "Straight body line",
            "Straight knees",
            "Legs together",
        ],
        "deductions": [
            {"fault": "Piked hips instead of stretched position", "max": 0.30},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height"},
            {"fault": "Body shape breaks during rotation"},
            {"fault": "Low chest on landing"},
        ],
        "connections": [
            "front_tuck", "front_pike", "roundoff", "front_handspring"
        ],
        "rule_note": (
            "NFHS 2026 interpretation explicitly identifies a stretched forward salto "
            "as Superior."
        ),
    },

    "front_full": {
        "name": "Front Layout Full",
        "category": "salto",
        "direction": "forward",
        "body_position": "stretched",
        "difficulty": "AHS",
        "rotations": {"1.0": "AHS"},
        "how_to": (
            "Create a high stretched front salto first, then add one full longitudinal twist "
            "while keeping the body tight and extended. The takeoff should rise before the "
            "twist begins. Complete the twist and forward rotation before preparing for a "
            "two-foot landing."
        ),
        "key_shapes": [
            "Stretched front salto",
            "Full 360° twist",
            "Twist begins after lift",
            "Tight vertical axis",
            "Rotation complete before landing",
        ],
        "deductions": [
            {"fault": "Twist begins too early"},
            {"fault": "Incomplete twist"},
            {"fault": "Piked hips"},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height"},
            {"fault": "Off-axis rotation"},
            {"fault": "Under-rotation on landing"},
        ],
        "connections": [
            "front_tuck", "front_layout", "roundoff", "front_handspring"
        ],
    },

    # ------------------------------------------------------------------
    # BACKWARD SALTOS
    # ------------------------------------------------------------------
    "back_tuck": {
        "name": "Back Tuck",
        "category": "salto",
        "direction": "backward",
        "body_position": "tuck",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Take off vertically from both feet with the chest lifted and arms driving upward. "
            "Finish the upward extension before pulling the knees toward the chest. Rotate "
            "backward in a compact tuck, then open the hips and knees before landing on both feet."
        ),
        "key_shapes": [
            "Vertical takeoff",
            "Chest lifted",
            "Compact tuck",
            "Knees together",
            "Open before landing",
        ],
        "deductions": [
            {"fault": "Throws head backward on takeoff"},
            {"fault": "Insufficient height"},
            {"fault": "Loose tuck"},
            {"fault": "Knees separate"},
            {"fault": "Opens too late"},
            {"fault": "Under-rotation"},
        ],
        "connections": [
            "back_tuck", "back_pike", "back_layout",
            "back_full", "roundoff", "back_handspring"
        ],
    },

    "back_pike": {
        "name": "Back Pike",
        "category": "salto",
        "direction": "backward",
        "body_position": "pike",
        "difficulty": "S",
        "rotations": {},
        "how_to": (
            "Jump vertically from both feet and finish the takeoff before rotating backward. "
            "Keep the knees straight and close sharply at the hips into a pike. Maintain the "
            "pike through the main part of the salto, then open the hips in time to land upright."
        ),
        "key_shapes": [
            "Vertical takeoff",
            "Straight knees",
            "Clear hip pike",
            "Legs together",
            "Open before landing",
        ],
        "deductions": [
            {"fault": "Insufficient pike position"},
            {"fault": "Bent knees"},
            {"fault": "Head thrown backward"},
            {"fault": "Insufficient height"},
            {"fault": "Late opening"},
            {"fault": "Under-rotation"},
        ],
        "connections": [
            "back_tuck", "back_layout", "roundoff", "back_handspring"
        ],
    },

    "back_layout": {
        "name": "Back Layout",
        "category": "salto",
        "direction": "backward",
        "body_position": "stretched",
        "difficulty": "S",
        "rotations": {
            "0": "S",
            "0.5": "S",
            "1.0": "HS",
            "1.5": "AHS",
            "2.0": "AHS",
        },
        "rotation_aliases": {
            "0.5": "Back half",
            "1.0": "Back full",
            "1.5": "Back 1½",
            "2.0": "Double full",
        },
        "how_to": (
            "Take off upward with the body extended, then rotate backward while keeping the "
            "hips open and the body stretched. For twisting versions, establish the salto "
            "and a tight body axis before adding the twist. Complete the selected twist "
            "before landing."
        ),
        "key_shapes": [
            "Vertical set",
            "Stretched hips",
            "Straight knees",
            "Legs together",
            "Tight twisting axis when applicable",
        ],
        "deductions": [
            {"fault": "Piked hips instead of stretched position", "max": 0.30},
            {"fault": "Bent knees"},
            {"fault": "Insufficient height"},
            {"fault": "Twist begins too early"},
            {"fault": "Incomplete twist"},
            {"fault": "Off-axis rotation"},
        ],
        "connections": [
            "back_tuck", "back_pike", "back_layout",
            "roundoff", "back_handspring"
        ],
        "rule_note": (
            "NFHS specifically identifies back layout 1/2 as Superior; back full is HS; "
            "back 1½ or more is AHS."
        ),
    },

    # Separate searchable alias because gymnasts commonly look for "back full".
    "back_full": {
        "name": "Back Full",
        "category": "salto",
        "direction": "backward",
        "body_position": "stretched",
        "difficulty": "HS",
        "rotations": {"1.0": "HS"},
        "how_to": (
            "Set a stretched back salto upward, then complete one full 360° twist while "
            "maintaining a tight body line. Keep the twist centered around the body's long "
            "axis and finish it before preparing for the landing."
        ),
        "key_shapes": [
            "High vertical set",
            "Stretched body",
            "Full 360° twist",
            "Legs together",
            "Controlled landing",
        ],
        "deductions": [
            {"fault": "Twist starts before the set is complete"},
            {"fault": "Incomplete full twist"},
            {"fault": "Piked hips"},
            {"fault": "Bent knees"},
            {"fault": "Off-axis rotation"},
            {"fault": "Insufficient height"},
        ],
        "connections": [
            "back_tuck", "back_layout", "roundoff", "back_handspring"
        ],
    },

    "back_one_half": {
        "name": "Back 1½ Twist",
        "category": "salto",
        "direction": "backward",
        "body_position": "stretched",
        "difficulty": "AHS",
        "rotations": {"1.5": "AHS"},
        "how_to": (
            "Create a high stretched backward salto and then complete one and a half twists. "
            "Keep the hips open and body tight while twisting, and finish facing the opposite "
            "direction from takeoff before landing."
        ),
        "key_shapes": [
            "High set",
            "Stretched body",
            "1½ twists",
            "Tight axis",
            "Forward-facing landing",
        ],
        "deductions": [
            {"fault": "Twist begins too early"},
            {"fault": "Incomplete 1½ twist"},
            {"fault": "Insufficient height"},
            {"fault": "Piked hips"},
            {"fault": "Off-axis rotation"},
            {"fault": "Poor landing control"},
        ],
        "connections": [
            "front_tuck", "front_layout", "roundoff", "back_handspring"
        ],
    },

    # ------------------------------------------------------------------
    # DOUBLE SALTOS
    # ------------------------------------------------------------------
    "double_back_tuck": {
        "name": "Double Back Tuck",
        "category": "salto",
        "direction": "backward",
        "body_position": "tuck",
        "difficulty": "AHS",
        "rotations": {},
        "how_to": (
            "Generate a powerful vertical takeoff and complete two backward salto rotations "
            "in a compact tuck. Maintain height and a tight tuck through the rotations, then "
            "open early enough to identify and absorb the landing."
        ),
        "key_shapes": [
            "Powerful vertical set",
            "Two backward rotations",
            "Compact tuck",
            "Knees together",
            "Visible opening for landing",
        ],
        "deductions": [
            {"fault": "Insufficient height"},
            {"fault": "Loose tuck"},
            {"fault": "Knees separate"},
            {"fault": "Opens too late"},
            {"fault": "Under-rotation"},
            {"fault": "Low chest on landing"},
        ],
        "connections": ["roundoff", "back_handspring"],
    },

    "double_front_tuck": {
        "name": "Double Front Tuck",
        "category": "salto",
        "direction": "forward",
        "body_position": "tuck",
        "difficulty": "AHS",
        "rotations": {},
        "how_to": (
            "Use a powerful two-foot punch to create height, then complete two forward salto "
            "rotations in a compact tuck. Keep the body centered over the takeoff, maintain "
            "the tuck through both rotations, and open early enough to prepare for landing."
        ),
        "key_shapes": [
            "Powerful two-foot punch",
            "Two forward rotations",
            "Compact tuck",
            "Centered rotation",
            "Visible opening for landing",
        ],
        "deductions": [
            {"fault": "Insufficient height"},
            {"fault": "Rotation begins too early"},
            {"fault": "Loose tuck"},
            {"fault": "Knees separate"},
            {"fault": "Late opening"},
            {"fault": "Under-rotation"},
        ],
        "connections": ["front_handspring", "roundoff"],
    },
})


# Override profile selection so saltos get salto deductions rather than
# hand-support deductions.
def deduction_profiles_for(event: str, skill_id: str, skill: dict):
    profiles = []
    category = skill.get("category", "").lower()

    if event == "vault":
        if skill_id == "straddle_vault":
            return ["straddle_vault_practice", "landing"]
        return ["vault_handspring", "landing"]

    profiles.append("universal_form")

    if event == "bars":
        profiles.append("bars_execution")
        return profiles

    if event == "beam":
        profiles.append("beam_execution")
    elif event == "floor":
        profiles.append("floor_execution")

    if category in {"jump", "dance"}:
        profiles.append("jump_dance")
    if category == "turn":
        profiles.append("turn")
    if category == "balance":
        profiles.append("balance")
    if category == "salto":
        profiles.append("salto")
    elif category in {"acro", "acro flight", "dismount"}:
        profiles.append("hand_support_acro")

    if "walkover" in skill_id:
        profiles.append("walkover")
    if "handspring" in skill_id:
        profiles.append("handspring")
    if "aerial" in skill_id:
        profiles.append("aerial")
    if "dismount" in skill_id:
        profiles.append("dismount")

    if skill_id == "split_jump":
        profiles.append("split_shape")
    if skill_id == "straddle_jump":
        profiles.append("straddle_shape")
    if skill_id == "wolf_jump":
        profiles.append("wolf_shape")

    if event in {"beam", "floor"} and category != "balance":
        profiles.append("landing")

    return profiles
