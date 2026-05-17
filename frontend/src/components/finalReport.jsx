function FinalReport({
  behaviorData,
  questionnaireScore,
  userText = "",
}) {

  const detectEmotion = () => {

    const text = userText.toLowerCase().trim();

    /* ================= HAPPY ================= */

    const happyWords = [

      "happy","good","great","awesome","amazing",
      "love","fun","smile","excited","joy",
      "fantastic","wonderful","best","enjoy",
      "peaceful","motivated","celebrate","party",
      "vacation","excellent","perfect","blessed",
      "success","winning","achievement","promotion",
      "salary hike","good marks","passed exam",
      "placement","internship","festival",
      "family happy","parents proud",
      "relationship going good",
      "gift received","trip","travel",
      "music","movie night","shopping",
      "new phone","birthday","dream come true",
      "life is beautiful","feeling positive",
      "today is amazing","good vibes",
      "i feel energetic","everything is good"
    ];

    /* ================= SAD ================= */

    const sadWords = [

      "sad","cry","crying","depressed",
      "lonely","upset","hurt","pain",
      "broken","heartbroken","hopeless",
      "empty","lost","failure","fail",
      "bad day","trauma","regret",
      "emotionally hurt","miserable",
      "down","negative","suffering",
      "breakup","relationship ended",
      "friend ignored me","low marks",
      "failed exam","lost job",
      "family problem","nobody loves me",
      "feeling useless","dark thoughts",
      "disappointed","worthless",
      "life is hard","tired of life",
      "feeling low","emotionally weak"
    ];

    /* ================= STRESSED ================= */

    const stressWords = [

      "stress","stressed","pressure",
      "anxiety","overthinking",
      "panic","worried","fear",
      "nervous","burnout","exhausted",
      "restless","workload",
      "mental pressure","insomnia",
      "cannot sleep","tired",
      "exam pressure","assignment",
      "deadline","office pressure",
      "too much work","headache",
      "confused about future",
      "career tension","financial stress",
      "family stress","panic attack",
      "mental stress","emotionally stressed"
    ];

    /* ================= ANGRY ================= */

    const angryWords = [

      "angry","mad","hate",
      "frustrated","annoyed",
      "irritated","furious",
      "rage","aggressive",
      "fight","revenge",
      "toxic","fake people",
      "betrayed","cheated",
      "lied to me","argument",
      "jealous","disgusted",
      "useless people","worst day",
      "i am pissed","very angry",
      "destroy everything",
      "fed up","i cannot tolerate"
    ];

    /* ================= FEAR ================= */

    const fearWords = [

      "afraid","scared","terrified",
      "fearful","unsafe","nightmare",
      "panic attack","frightened",
      "future fear","fear of failure",
      "fear of losing","horror",
      "phobia","shaking","danger",
      "i am scared","i feel unsafe",
      "fearful situation","worried about future"
    ];

    /* ================= LONELY ================= */

    const lonelyWords = [

      "alone","isolated",
      "ignored","left out",
      "no friends","need someone",
      "nobody talks to me",
      "i feel alone",
      "nobody understands me",
      "emotionally alone",
      "social isolation",
      "missing someone",
      "feeling disconnected"
    ];

    /* ================= EXCITED ================= */

    const excitedWords = [

      "thrilled","super excited",
      "cannot wait","festival",
      "concert","promotion",
      "birthday","vacation",
      "trip","dream achieved",
      "party tonight",
      "adventure","hyped",
      "celebration","ecstatic",
      "new beginning",
      "exciting opportunity"
    ];

    /* ================= BORED ================= */

    const boredWords = [

      "bored","boring","lazy",
      "nothing to do","dull",
      "sleepy","idle",
      "uninterested","same routine",
      "feeling blank","slow day",
      "wasting time","not motivated"
    ];

    /* ================= SUICIDAL ================= */

    const suicidalWords = [

      "i want to die",
      "kill myself",
      "suicide",
      "end my life",
      "i am done",
      "no reason to live",
      "better if i die",
      "self harm",
      "hurt myself",
      "i hate my life",
      "want to disappear",
      "life is meaningless",
      "i give up",
      "i cannot continue",
      "nobody cares about me",
      "i feel dead inside",
      "i don't want to live"
    ];

    /* ================= DETECTION FUNCTION ================= */

    const containsEmotion = (arr) => {

      let score = 0;

      arr.forEach((word) => {

        if (text.includes(word)) {

          score++;

        }

      });

      return score;
    };

    /* ================= EMOTION SCORES ================= */

    const emotionScores = [

      {
        emotion: "Suicidal ⚠",
        score: containsEmotion(suicidalWords),
      },

      {
        emotion: "Sad 😔",
        score: containsEmotion(sadWords),
      },

      {
        emotion: "Stressed 😣",
        score: containsEmotion(stressWords),
      },

      {
        emotion: "Angry 😡",
        score: containsEmotion(angryWords),
      },

      {
        emotion: "Fearful 😨",
        score: containsEmotion(fearWords),
      },

      {
        emotion: "Lonely 💔",
        score: containsEmotion(lonelyWords),
      },

      {
        emotion: "Excited 🤩",
        score: containsEmotion(excitedWords),
      },

      {
        emotion: "Bored 😴",
        score: containsEmotion(boredWords),
      },

      {
        emotion: "Happy 😊",
        score: containsEmotion(happyWords),
      },

    ];

    /* ================= SORT ================= */

    emotionScores.sort(
      (a, b) => b.score - a.score
    );

    /* ================= RETURN BEST MATCH ================= */

    if (emotionScores[0].score > 0) {

      return emotionScores[0].emotion;

    }

    /* ================= FALLBACK ================= */

    if (questionnaireScore >= 20) {

      return "Highly Stressed 😣";

    }

    if (questionnaireScore <= 5) {

      return "Very Happy 😄";

    }

    return "Neutral 😐";
  };

  const finalEmotion = detectEmotion();

  /* ================= MENTAL STATE ================= */

  const getMentalState = () => {

    if (
      finalEmotion.includes("Suicidal")
    ) {
      return "Critical Emotional Condition";
    }

    if (
      finalEmotion.includes("Sad") ||
      finalEmotion.includes("Stressed") ||
      finalEmotion.includes("Fearful")
    ) {
      return "High Emotional Stress";
    }

    if (
      finalEmotion.includes("Happy") ||
      finalEmotion.includes("Excited")
    ) {
      return "Positive Mental State";
    }

    if (
      finalEmotion.includes("Angry")
    ) {
      return "Emotionally Frustrated";
    }

    if (
      finalEmotion.includes("Lonely")
    ) {
      return "Social Isolation Detected";
    }

    return "Moderate Emotional State";
  };

  return (

    <div>

      <h1 className="panel-title">
        Final Emotional Report
      </h1>

      <div className="report-box">

        <div className="big-emotion">
          {finalEmotion}
        </div>

        <div className="stat">
          ⌨ Typing Speed:
          {" "}
          {behaviorData.speed}
          {" "}
          WPM
        </div>

        <div className="stat">
          🎯 Accuracy:
          {" "}
          {behaviorData.accuracy}
          %
        </div>

        <div className="stat">
          ❌ Mistakes:
          {" "}
          {behaviorData.mistakes}
        </div>

        <div className="stat">
          🧠 Questionnaire Score:
          {" "}
          {questionnaireScore}
        </div>

        <div
          className="stat"
          style={{
            marginTop:"30px",
            fontSize:"26px",
            fontWeight:"700",
            color:"#38bdf8"
          }}
        >
          {getMentalState()}
        </div>

      </div>

    </div>
  );
}

export default FinalReport;