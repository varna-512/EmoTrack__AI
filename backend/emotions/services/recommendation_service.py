def generate_recommendations(
    final_probs,
    stress_score,
    questionnaire=None,
    wellness_dimensions=None,
    pulse=None,
    face_result=None,
    voice_result=None,
    text_result=None,
    selected_profile=None,
):
    questionnaire = questionnaire or {}
    wellness_dimensions = wellness_dimensions or []
    face_probs = (face_result or {}).get("emotion_probs", {})
    voice_probs = (voice_result or {}).get("emotion_probs", {})
    text_probs = (text_result or {}).get("emotion_probs", {})
    dimension_map = {
        item.get("label"): int(item.get("value") or 0)
        for item in wellness_dimensions
    }

    candidates = []

    def add(category, title, description, reason, weight):
        candidates.append({
            "category": category,
            "title": title,
            "description": description,
            "reason": reason,
            "weight": weight,
        })

    sleep = questionnaire.get("sleep_quality")
    energy = int(questionnaire.get("energy_level") or 0)
    motivation = questionnaire.get("motivation_level")
    connectedness = questionnaire.get("social_connectedness")
    stress_level = questionnaire.get("stress_level")
    pulse_value = _safe_int(pulse, 76)

    if selected_profile == "Workload Pressure Profile" or stress_score >= 55:
        add(
            "Stress Management",
            "Create a Pressure Map",
            "List the three highest-pressure demands, then mark one action that can be deferred, delegated, or reduced.",
            f"Stress score is {stress_score}/100 and self-reported stress is {stress_level}.",
            stress_score + 20,
        )
        add(
            "Planning",
            "Define a Stop Point",
            "Choose a realistic stopping point for the day before starting the next demanding task.",
            "Workload pressure profiles benefit from clear boundaries around effort and recovery.",
            stress_score + 8,
        )


    if selected_profile == "Stress Accumulation Profile":
        add(
            "Recovery Planning",
            "Schedule Recovery Before Productivity",
            "Block recovery periods into your schedule before adding new tasks or commitments.",
            "Stress accumulation profiles benefit from rebuilding recovery capacity before increasing workload.",
            90,
        )

        add(
            "Stress Management",
            "Reduce One Recurring Pressure Source",
            "Identify one recurring source of pressure and create a concrete plan to reduce its impact this week.",
            "Persistent pressure indicators were detected across multiple assessment channels.",
            88,
        )

    if selected_profile == "Cognitive Fatigue Profile":
        add(
            "Energy Management",
            "Reduce Cognitive Load",
            "Break demanding tasks into smaller segments and avoid multitasking during periods of low energy.",
            "Recovery and engagement indicators suggest mental fatigue.",
            92,
        )

        add(
            "Recovery",
            "Protect Mental Recovery Time",
            "Create dedicated periods without demanding work, studying, or prolonged screen exposure.",
            "Cognitive fatigue often improves when recovery is protected consistently.",
            86,
        )

    if selected_profile == "Social Disconnection Profile":
        add(
            "Social Engagement",
            "Reconnect With a Trusted Person",
            "Schedule a brief conversation or message exchange with someone you trust.",
            "Social support is an important protective factor for wellbeing.",
            84,
        )

        add(
            "Support Building",
            "Increase Positive Interaction Opportunities",
            "Look for one opportunity this week to engage in a shared activity or meaningful conversation.",
            "Reduced connectedness was identified during the assessment.",
            80,
        )

    if selected_profile == "Recovery Deficit Profile" or sleep in ["Poor", "Very Poor"] or energy <= 4:
        add(
            "Recovery",
            "Protect a Recovery Block",
            "Schedule a 30-minute low-stimulation recovery block today and keep it free from work, study, and scrolling.",
            f"Sleep quality is {sleep} and energy is {energy}/10.",
            85 - energy * 4,
        )
        add(
            "Energy",
            "Lower the Activation Cost",
            "Move one nonessential demand to another day and keep the next task physically easy to start.",
            "Recovery indicators suggest reduced restoration capacity.",
            69,
        )

    if motivation in ["Low", "Very Low"]:
        add(
            "Motivation",
            "Use a Two-Step Start",
            "Choose one task, define the first two visible steps, and stop after ten minutes if momentum has not improved.",
            f"Motivation is reported as {motivation}.",
            78,
        )

    if connectedness in ["Disconnected", "Very Disconnected"]:
        add(
            "Social Wellness",
            "Send One Low-Pressure Check-In",
            "Contact one trusted person with a short message that does not require a long conversation.",
            f"Social connectedness is reported as {connectedness}.",
            72,
        )

    if pulse_value >= 92 or final_probs.get("anxious", 0) > 0.32:
        add(
            "Nervous System Regulation",
            "Downshift With Paced Breathing",
            "Use five rounds of slow breathing with a longer exhale than inhale before returning to demanding tasks.",
            f"Pulse is {pulse_value} BPM and the fused strain signal is {round(final_probs.get('anxious', 0), 2)}.",
            70,
        )

    if voice_probs.get("sad", 0) > 0.25 or text_probs.get("sad", 0) > 0.25:
        add(
            "Reflection",
            "Name the Main Concern",
            "Write one sentence naming the concern, one sentence naming what is controllable, and one next step.",
            "Voice or text signals indicate a heavier reflective tone.",
            66,
        )

    if face_probs.get("neutral", 0) > 0.45 and voice_probs.get("anxious", 0) > 0.25:
        add(
            "Self Awareness",
            "Check for Masked Strain",
            "Pause twice today to rate tension, focus, and fatigue from 1 to 10 before choosing the next activity.",
            "Facial signals appear steady while voice signals suggest internal pressure.",
            64,
        )

    if selected_profile == "High Engagement Profile":
        add(
            "Positive Momentum",
            "Channel Momentum Intentionally",
            "Use the current engagement to complete one meaningful priority, then deliberately stop before overextending.",
            "The assessment shows strong energy and positive engagement.",
            76,
        )
        add(
            "Sustainability",
            "Add a Recovery Buffer",
            "Place a short break after your highest-value activity so strong engagement does not turn into overextension.",
            "High energy is useful, but the profile benefits from pacing.",
            62,
        )

    if selected_profile == "Balanced Wellness Profile":
        add(
            "Maintenance",
            "Keep the Stable Pattern Visible",
            "Repeat one habit that supported today and note what helped keep stress manageable.",
            "The wellness profile is balanced with no dominant concern area.",
            68,
        )
        add(
            "Prevention",
            "Track One Early Signal",
            "Pick one early signal, such as sleep timing or afternoon energy, and check it once tomorrow.",
            "Balanced profiles are best supported by light monitoring rather than heavy intervention.",
            58,
        )

    if selected_profile == "Mixed Signal Profile":
        add(
            "Signal Check",
            "Compare Inside and Outside State",
            "Write down what you appeared to be feeling and what you privately felt, then note any gap.",
            "The selected profile indicates meaningful variation across assessment channels.",
            73,
        )

    if not candidates:
        add(
            "Wellness",
            "Complete a Brief Reset",
            "Take a short walk, hydrate, and identify the next manageable task for the day.",
            "No single risk signal dominated the assessment.",
            50,
        )

    recommendations = []
    used_titles = set()
    used_categories = set()
    for item in sorted(candidates, key=lambda rec: rec["weight"], reverse=True):
        if item["title"] in used_titles:
            continue
        if len(recommendations) >= 5:
            break
        clean_item = {
            "category": item["category"],
            "title": item["title"],
            "description": item["description"],
            "reason": item["reason"],
        }
        recommendations.append(clean_item)
        used_titles.add(item["title"])
        used_categories.add(item["category"])

    return recommendations


def generate_wellness_report(
    final_probs,
    stress_score,
    questionnaire=None,
    pulse=None,
    face_result=None,
    voice_result=None,
    text_result=None,
):
    questionnaire = questionnaire or {}
    wellness_dimensions = _wellness_dimensions(
        final_probs,
        stress_score,
        questionnaire,
        pulse,
        face_result,
        voice_result,
        text_result,
    )
    profile_name, profile_reason = _select_profile(
        final_probs,
        stress_score,
        questionnaire,
        pulse,
        wellness_dimensions,
        face_result,
        voice_result,
        text_result,
    )
    priority = _priority_level(stress_score, wellness_dimensions)
    recommendations = generate_recommendations(
        final_probs,
        stress_score,
        questionnaire,
        wellness_dimensions,
        pulse,
        face_result,
        voice_result,
        text_result,
        profile_name,
    )
    overall = _overall_assessment(
        profile_name,
        stress_score,
        questionnaire,
        wellness_dimensions,
        pulse,
        face_result,
        voice_result,
        text_result,
    )
    observations = _key_observations(
        profile_name,
        final_probs,
        stress_score,
        questionnaire,
        pulse,
        face_result,
        voice_result,
        text_result,
        wellness_dimensions,
    )
    attention = _attention_areas(
        profile_name,
        stress_score,
        questionnaire,
        wellness_dimensions,
        pulse,
        face_result,
        voice_result,
        text_result,
    )
    print("\n" + "=" * 60)
    print("WELLNESS REPORT GENERATION")
    print("=" * 60)

    print("Selected Profile:")
    print(profile_name)

    print("\nProfile Reason:")
    print(profile_reason)

    print("\nWellness Dimensions:")
    for item in wellness_dimensions:
        print(
            f"{item['label']}: {item['value']}"
        )

    print("\nPriority:")
    print(priority)

    print("\nObservations:")
    for obs in observations:
        print("-", obs)

    print("\nRecommendations:")
    for rec in recommendations:
        print("-", rec["title"])

    print("=" * 60)
    return {
        "wellness_score": _wellness_score(wellness_dimensions),
        "overall_assessment": overall,
        "key_observations": observations,
        "areas_requiring_attention": attention,
        "wellness_dimensions": wellness_dimensions,
        "personalized_recommendations": recommendations,
        "recommendations": recommendations,
        "priority_level": priority,
        "selected_profile": profile_name,
        "profile_selection_reason": profile_reason,
    }


def _wellness_dimensions(
    final_probs,
    stress_score,
    questionnaire,
    pulse,
    face_result,
    voice_result,
    text_result,
):
    pulse_value = _safe_int(pulse, 76)

    energy = _safe_int(
        questionnaire.get("energy_level"),
        5
    )

    sleep = questionnaire.get("sleep_quality")
    motivation = questionnaire.get("motivation_level")

    face_probs = (
        face_result or {}
    ).get("emotion_probs", {})

    voice_probs = (
        voice_result or {}
    ).get("emotion_probs", {})

    text_probs = (
        text_result or {}
    ).get("emotion_probs", {})

    face_conf = float(
        (face_result or {}).get("confidence") or 0
    )

    voice_conf = float(
        (voice_result or {}).get("confidence") or 0
    )

    text_conf = float(
        (text_result or {}).get("confidence") or 0
    )

    # --------------------------------------------------
    # Stress & Pressure Management
    # --------------------------------------------------

    stress_management = max(
        0,
        min(
            100,
            100
            - (stress_score * 0.8)
            - max(0, pulse_value - 85)
        )
    )

    # --------------------------------------------------
    # Energy & Recovery
    # --------------------------------------------------

    sleep_score = _dimension_score(
        sleep,
        [
            "Very Poor",
            "Poor",
            "Average",
            "Good",
            "Excellent",
        ]
    )

    recovery = round(
        (sleep_score * 0.6)
        +
        (energy * 10 * 0.4)
    )

    # --------------------------------------------------
    # Engagement & Motivation
    # --------------------------------------------------

    motivation_score = _dimension_score(
        motivation,
        [
            "Very Low",
            "Low",
            "Moderate",
            "High",
            "Very High",
        ]
    )

    engagement = round(
        (motivation_score * 0.6)
        +
        (energy * 10 * 0.4)
    )

    # --------------------------------------------------
    # Communication Confidence
    # --------------------------------------------------

    communication = round(
        (
            voice_conf * 100 * 0.4
        )
        +
        (
            text_conf * 100 * 0.4
        )
        +
        (
            face_conf * 100 * 0.2
        )
    )

    # --------------------------------------------------
    # Emotional Consistency
    # --------------------------------------------------

    consistency = round(
        100
        -
        min(
            60,
            abs(face_conf - voice_conf) * 80
            +
            abs(voice_conf - text_conf) * 80
        )
    )

    return [
        {
            "label":
            "Stress & Pressure Management",
            "value":
            int(stress_management)
        },
        {
            "label":
            "Energy & Recovery",
            "value":
            int(recovery)
        },
        {
            "label":
            "Engagement & Motivation",
            "value":
            int(engagement)
        },
        {
            "label":
            "Communication Confidence",
            "value":
            int(communication)
        },
        {
            "label":
            "Emotional Consistency",
            "value":
            int(consistency)
        }
    ]

def _select_profile(
    final_probs,
    stress_score,
    questionnaire,
    pulse,
    dimensions,
    face_result,
    voice_result,
    text_result,
):
    dim = {item["label"]: item["value"] for item in dimensions}
    energy = _safe_int(questionnaire.get("energy_level"), 5)
    stress_level = questionnaire.get("stress_level")
    sleep = questionnaire.get("sleep_quality")
    motivation = questionnaire.get("motivation_level")
    pulse_value = _safe_int(pulse, 76)
    face_probs = (face_result or {}).get("emotion_probs", {})
    voice_probs = (voice_result or {}).get("emotion_probs", {})
    text_probs = (text_result or {}).get("emotion_probs", {})

    # Stress Accumulation Profile
    if (
        stress_score >= 65
        and pulse_value >= 90
        and dim.get("Energy & Recovery", 100) < 55
    ):
        return (
            "Stress Accumulation Profile",
            f"Selected because stress score is {stress_score}, pulse is {pulse_value} BPM, and recovery is {dim.get('Energy & Recovery')}/100."
        )

    # Social Disconnection Profile
    if questionnaire.get("social_connectedness") in [
        "Disconnected",
        "Very Disconnected"
    ]:
        return (
            "Social Disconnection Profile",
            f"Selected because questionnaire responses indicate reduced social connectedness."
        )

    # Cognitive Fatigue Profile
    if (
        dim.get("Energy & Recovery", 100) < 45
        and dim.get("Engagement & Motivation", 100) < 45
    ):
        return (
            "Cognitive Fatigue Profile",
            f"Selected because recovery is {dim.get('Energy & Recovery')}/100 and engagement is {dim.get('Engagement & Motivation')}/100."
        )

    # Workload Pressure Profile
    if (
        stress_score >= 55
        or stress_level in ["Very", "Extremely"]
        or pulse_value >= 94
    ):
        return (
            "Workload Pressure Profile",
            f"Selected because stress score is {stress_score}, reported stress is {stress_level}, and pulse is {pulse_value} BPM."
        )

    # Recovery Deficit Profile
    if (
        sleep in ["Poor", "Very Poor"]
        or dim.get("Energy & Recovery", 100) < 50
    ):
        return (
            "Recovery Deficit Profile",
            f"Selected because sleep quality is {sleep} and recovery score is {dim.get('Recovery')}/100."
        )

    # Motivation Concern Profile
    if (
        motivation in ["Low", "Very Low"]
    ):
        return (
            "Motivation Concern Profile",
            f"Selected because motivation was reported as {motivation}."
        )

    # High Engagement Profile
    if (
        energy >= 8
        and questionnaire.get("day_so_far") in ["Excellent", "Good"]
        and stress_score < 40
    ):
        return (
            "High Engagement Profile",
            f"Selected because energy is {energy}/10, day rating is {questionnaire.get('day_so_far')}, and stress score is {stress_score}."
        )

    # Mixed Signal Profile
    if (
        dim.get("Emotional Consistency", 100) < 60
        or _signal_spread(face_probs, voice_probs, text_probs) > 0.45
    ):
        return (
            "Mixed Signal Profile",
            f"Selected because emotional consistency is {dim.get('Emotional Consistency')} and modality outputs vary significantly."
        )

    # Balanced Wellness Profile
    return (
        "Balanced Wellness Profile",
        f"Selected because stress score is {stress_score} and wellness indicators remain stable."
    )

def _overall_assessment(profile, stress_score, questionnaire, dimensions,
                        pulse=None,
                        face_result=None,
                        voice_result=None,
                        text_result=None):

    dim = {item["label"]: item["value"] for item in dimensions}

    pulse_value = _safe_int(pulse, 76)

    face_probs = (face_result or {}).get("emotion_probs", {})
    voice_probs = (voice_result or {}).get("emotion_probs", {})
    text_probs = (text_result or {}).get("emotion_probs", {})

    findings = []

    # Stress
    if stress_score >= 70:
        findings.append(
            "significant pressure indicators across multiple assessment channels"
        )
    elif stress_score >= 50:
        findings.append(
            "moderate pressure patterns associated with current demands"
        )

    # Pulse
    if pulse_value >= 95:
        findings.append(
            "elevated physiological activation"
        )

    # Recovery
    if dim.get("Energy & Recovery", 100) < 45:
        findings.append(
            "reduced recovery capacity"
        )

    # Engagement
    if dim.get("Engagement & Motivation", 100) > 75:
        findings.append(
            "strong engagement and task involvement"
        )

    # Voice
    if voice_probs.get("stress", 0) > 0.60:
        findings.append(
            "consistent vocal stress markers"
        )

    if voice_probs.get("sad", 0) > 0.40:
        findings.append(
            "reflective emotional tone in speech"
        )

    # Text
    if text_probs.get("sad", 0) > 0.40:
        findings.append(
            "emotionally heavy language patterns"
        )

    if text_probs.get("happy", 0) > 0.50:
        findings.append(
            "positive future-oriented thinking"
        )

    # Face
    if face_probs.get("neutral", 0) > 0.60:
        findings.append(
            "stable outward presentation"
        )

    if face_probs.get("sad", 0) > 0.40:
        findings.append(
            "visible signs of emotional strain"
        )

    if not findings:
        findings.append(
            "generally balanced wellness indicators"
        )

    summary = ", ".join(findings)

    profile_context = {
        "Workload Pressure Profile":
            "Current demands appear to be consuming a substantial portion of available mental and emotional resources.",

        "Recovery Deficit Profile":
            "Recovery opportunities may not be fully offsetting ongoing workload and daily responsibilities.",

        "Stress Accumulation Profile":
            "Stress appears to have accumulated over time rather than resulting from a single isolated event.",

        "Motivation Concern Profile":
            "Reduced activation and momentum may be affecting progress on important activities.",

        "Social Disconnection Profile":
            "Lower levels of perceived social connection may be reducing access to emotional support and recovery.",

        "Cognitive Fatigue Profile":
            "Mental fatigue indicators suggest the need for additional recovery and workload pacing.",

        "High Engagement Profile":
            "Strong engagement is present and can be leveraged productively when balanced with recovery.",

        "Mixed Signal Profile":
            "Different assessment channels are showing varying patterns, suggesting a gap between internal and external experiences.",

        "Balanced Wellness Profile":
            "Current wellness indicators remain relatively stable across assessment channels."
    }

    return (
        f"The assessment identified {summary}. "
        f"{profile_context.get(profile, '')} "
        f"Based on the combined analysis of questionnaire responses, physiological indicators, "
        f"and multimodal wellness signals, the current profile suggests that attention should "
        f"be directed toward maintaining sustainable performance while supporting overall wellbeing."
    )

def _key_observations(
    profile,
    final_probs,
    stress_score,
    questionnaire,
    pulse,
    face_result,
    voice_result,
    text_result,
    dimensions,
):
    dim = {item["label"]: item["value"] for item in dimensions}

    pulse_value = _safe_int(pulse, 76)

    face_probs = (face_result or {}).get("emotion_probs", {})
    voice_probs = (voice_result or {}).get("emotion_probs", {})
    text_probs = (text_result or {}).get("emotion_probs", {})

    observations = []

    # Profile
    observations.append(
        f"Wellness profile classified as {profile}."
    )

    # Stress
    if stress_score >= 70:
        observations.append(
            "Sustained pressure indicators were detected across multiple assessment channels."
        )
    elif stress_score >= 50:
        observations.append(
            "Moderate workload-related pressure patterns were observed."
        )

    # Pulse
    if pulse_value >= 95:
        observations.append(
            "Elevated physiological activation was observed through pulse measurements."
        )

    # Recovery
    if dim.get("Energy & Recovery", 100) < 50:
        observations.append(
            "Recovery indicators suggest insufficient restoration between demanding activities."
        )

    # Engagement
    if dim.get("Engagement & Motivation", 0) >= 75:
        observations.append(
            "Strong engagement and goal-directed behavior remain present."
        )

    

    # Social
    if questionnaire.get("social_connectedness") in [
        "Disconnected",
        "Very Disconnected"
    ]:
                observations.append(
            "Lower perceived social connectedness may be limiting access to support resources."
        )

    # Voice
    if voice_probs.get("stress", 0) > 0.60:
        observations.append(
            "Speech patterns contained consistent vocal strain markers."
        )

    if voice_probs.get("sad", 0) > 0.40:
        observations.append(
            "Speech characteristics reflected a reflective or emotionally heavy tone."
        )

    # Text
    if text_probs.get("sad", 0) > 0.40:
        observations.append(
            "Written language contained themes associated with emotional burden or concern."
        )

    if text_probs.get("happy", 0) > 0.50:
        observations.append(
            "Text responses reflected positive future-oriented thinking."
        )

    # Face
    if face_probs.get("neutral", 0) > 0.60:
        observations.append(
            "Facial indicators remained relatively composed and stable."
        )

    if face_probs.get("sad", 0) > 0.40:
        observations.append(
            "Facial indicators suggested signs of emotional strain."
        )

    # Alignment
    if dim.get("Emotional Consistency", 100) < 60:
        observations.append(
            "Meaningful variation was observed across assessment modalities."
        )

    # Wellness summary
    observations.append(
        f"Overall wellness score: {_wellness_score(dimensions)}/100."
    )

    return observations[:10]

def _attention_areas(
    profile,
    stress_score,
    questionnaire,
    dimensions,
    pulse=None,
    face_result=None,
    voice_result=None,
    text_result=None,
):
    dim = {item["label"]: item["value"] for item in dimensions}

    pulse_value = _safe_int(pulse, 76)

    face_probs = (face_result or {}).get("emotion_probs", {})
    voice_probs = (voice_result or {}).get("emotion_probs", {})
    text_probs = (text_result or {}).get("emotion_probs", {})

    attention = []

    # Stress
    if stress_score >= 55:
        attention.append({
            "area": "Stress & Pressure Management",
            "description":
                "Assessment results indicate sustained pressure indicators that may affect concentration, recovery, and overall wellbeing if maintained over extended periods."
        })

    # Recovery
    if dim.get("Energy & Recovery", 100) < 50:
        attention.append({
            "area": "Energy & Recovery",
            "description":
                "Recovery indicators suggest that current rest and restoration patterns may not be fully compensating for ongoing demands, increasing the likelihood of fatigue accumulation."
        })

        #Motivation
    if questionnaire.get("motivation_level") in [
        "Low",
        "Very Low"
    ]:
        attention.append({
            "area": "Engagement & Motivation",
            "description":
                "Lower motivation indicators may be reducing task initiation, persistence, and confidence when approaching responsibilities."
        })


   
    # Pulse
    if pulse_value >= 95:
        attention.append({
            "area": "Physiological Activation",
            "description":
                "Elevated pulse measurements suggest increased physiological arousal that may reflect accumulated pressure or reduced recovery opportunities."
        })

    # Voice Stress
    if voice_probs.get("stress", 0) > 0.65:
        attention.append({
            "area": "Vocal Stress Indicators",
            "description":
                "Speech analysis identified vocal patterns associated with elevated strain and internal pressure."
        })

    # Text Sadness
    if text_probs.get("sad", 0) > 0.40:
        attention.append({
            "area": "Emotional Processing",
            "description":
                "Written responses contained themes associated with concern, burden, or emotional heaviness that may benefit from reflection and support."
        })

    # Mixed Signals
    if profile == "Mixed Signal Profile":
        attention.append({
            "area": "Signal Consistency",
            "description":
                "Different assessment channels are reporting varying patterns, suggesting that outward presentation and internal experiences may not be fully aligned."
        })

    if not attention:
        attention.append({
            "area": "Preventive Wellness",
            "description":
                "No major concern areas were identified. Maintaining current wellness habits and monitoring for early changes is recommended."
        })

    return attention
def _priority_level(stress_score, dimensions):
    dim = {
        item["label"]: item["value"]
        for item in dimensions
    }

    risk_score = (
        stress_score * 0.5
        +
        (100 - dim.get("Energy & Recovery", 100)) * 0.3
        +
        (100 - dim.get("Emotional Consistency", 100)) * 0.2
    )

    if risk_score >= 70:
        return "High"

    if risk_score >= 40:
        return "Moderate"

    return "Low"
def _wellness_score(dimensions):
    if isinstance(dimensions, dict):
        values = list(dimensions.values())
    else:
        values = [int(item.get("value") or 0) for item in dimensions]
    if not values:
        return 0
    return round(sum(values) / len(values))


def _dimension_score(value, ordered_values):
    if value not in ordered_values:
        return 50
    return round((ordered_values.index(value) / (len(ordered_values) - 1)) * 100)


def _signal_spread(*probability_sets):
    dominant_scores = []
    for probs in probability_sets:
        if probs:
            dominant_scores.append(max(probs.values()))
    if len(dominant_scores) < 2:
        return 0
    return max(dominant_scores) - min(dominant_scores)


def _safe_int(value, default):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default
