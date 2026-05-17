import { useState } from "react";

import "./App.css";

function App() {

  const [started, setStarted] =
    useState(false);

  const [text, setText] =
    useState("");

  const [emotion, setEmotion] =
    useState("Neutral 😐");

  const [typingSpeed, setTypingSpeed] =
    useState(0);

  const [mistakes, setMistakes] =
    useState(0);

  const [backspaces, setBackspaces] =
    useState(0);

  const [showQuestions, setShowQuestions] =
    useState(false);

  const [showReport, setShowReport] =
    useState(false);

  const [aiQuestions, setAiQuestions] =
    useState([]);

  const [answers, setAnswers] =
    useState(["","","","",""]);

  /* ================= DETECT EMOTION ================= */

  const detectEmotion = (input) => {

    const text =
      input.toLowerCase();

    /* SAD */

    if (
      text.includes("sad") ||
      text.includes("cry") ||
      text.includes("depressed") ||
      text.includes("alone")
    ) {

      setEmotion("Sad 😔");

      setAiQuestions([

        "Why do you think you feel sad today?",

        "Did something happen recently that hurt you emotionally?",

        "Do you feel lonely or unsupported?",

        "Are studies or relationships affecting your mood?",

        "What usually helps you feel emotionally better?"
      ]);

      return;
    }

    /* HAPPY */

    if (
      text.includes("happy") ||
      text.includes("excited") ||
      text.includes("great") ||
      text.includes("love")
    ) {

      setEmotion("Happy 😊");

      setAiQuestions([

        "What made you feel happy today?",

        "Did someone special make your day better?",

        "What achievement are you proud of recently?",

        "How do you usually celebrate happy moments?",

        "What motivates you the most in life?"
      ]);

      return;
    }

    /* STRESS */

    if (
      text.includes("stress") ||
      text.includes("tired") ||
      text.includes("pressure") ||
      text.includes("anxiety")
    ) {

      setEmotion("Stressed 😣");

      setAiQuestions([

        "What is causing the most stress in your life?",

        "Do academic pressure or deadlines affect you?",

        "How often do you feel mentally exhausted?",

        "Do you get enough sleep and rest?",

        "What helps you reduce stress usually?"
      ]);

      return;
    }

    /* ANGRY */

    if (
      text.includes("angry") ||
      text.includes("hate") ||
      text.includes("mad")
    ) {

      setEmotion("Angry 😡");

      setAiQuestions([

        "What made you angry recently?",

        "Do people around you frustrate you often?",

        "How do you usually control anger?",

        "Does stress increase your anger levels?",

        "What makes you calm again?"
      ]);

      return;
    }

    /* DEFAULT */

    setEmotion("Neutral 😐");

    setAiQuestions([

      "How are you feeling emotionally today?",

      "What is currently on your mind?",

      "Do you feel mentally peaceful?",

      "What is your biggest daily challenge?",

      "What improves your mood usually?"
    ]);
  };

  /* ================= HANDLE TEXT ================= */

  const handleTyping = (e) => {

    const value = e.target.value;

    setText(value);

    const words =
      value.trim().split(" ").filter(Boolean);

    setTypingSpeed(words.length * 7);

    const errorCount =
      (value.match(/[0-9@#$%^&*]/g) || []).length;

    setMistakes(errorCount);

    detectEmotion(value);
  };

  /* ================= BACKSPACE ================= */

  const handleKeyDown = (e) => {

    if (e.key === "Backspace") {

      setBackspaces((prev) => prev + 1);
    }
  };

  /* ================= FINAL SCORES ================= */

  const stressLevel =

    emotion.includes("Stressed")
    ? 85

    : emotion.includes("Sad")
    ? 70

    : emotion.includes("Angry")
    ? 75

    : 25;

  const happinessLevel =

    emotion.includes("Happy")
    ? 90

    : 40;

  const anxietyLevel =

    backspaces > 10
    ? 80

    : 20;

  /* ================= SUMMARY ================= */

  const getSummary = () => {

    if (
      emotion.includes("Happy")
    ) {
      return "AI analysis indicates a positive emotional state.";
    }

    if (
      emotion.includes("Sad")
    ) {
      return "AI detected emotional sadness and low mood patterns.";
    }

    if (
      emotion.includes("Stressed")
    ) {
      return "Behavioral analysis suggests mental pressure and stress.";
    }

    if (
      emotion.includes("Angry")
    ) {
      return "AI detected frustration and emotional irritation.";
    }

    return "Emotional condition appears balanced.";
  };

  return (

    <div className="app">

      {/* START SCREEN */}

      {!started ? (

        <div className="start-card">

          <h1 className="main-title">
            EmoTrack AI
          </h1>

          <p className="subtitle">
            AI Powered Emotional &
            Behavioral Analysis
          </p>

          <button
            className="start-btn"
            onClick={() => setStarted(true)}
          >
            Start Analysis
          </button>

        </div>

      ) : !showQuestions && !showReport ? (

        /* LIVE ANALYSIS */

        <div className="analysis-screen">

          <h1 className="analysis-title">
            Live Behavior Analysis
          </h1>

          <div className="stats-grid">

            <div className="stat-card">
              <h2>Emotion</h2>
              <p>{emotion}</p>
            </div>

            <div className="stat-card">
              <h2>Typing Speed</h2>
              <p>{typingSpeed} WPM</p>
            </div>

            <div className="stat-card">
              <h2>Mistakes</h2>
              <p>{mistakes}</p>
            </div>

            <div className="stat-card">
              <h2>Backspaces</h2>
              <p>{backspaces}</p>
            </div>

          </div>

          <div className="chatbot-box">

            <h2 className="chatbot-title">
              Emotion AI Chatbot
            </h2>

            <div className="chat-message">

              🤖 Start typing so AI can analyze your emotions...

            </div>

          </div>

          <textarea
            className="typing-box"
            placeholder="Start typing your thoughts here..."
            value={text}
            onChange={handleTyping}
            onKeyDown={handleKeyDown}
          />

          <button
            className="analyze-btn"
            onClick={() => setShowQuestions(true)}
          >
            Continue To AI Questions
          </button>

        </div>

      ) : !showReport ? (

        /* AI QUESTIONS */

        <div className="analysis-screen">

          <h1 className="analysis-title">
            AI Emotional Questionnaire
          </h1>

          <div className="chatbot-box">

            {aiQuestions.map((question,index)=>(

              <div
                key={index}
                style={{marginBottom:"20px"}}
              >

                <p
                  style={{
                    color:"white",
                    marginBottom:"10px",
                    fontSize:"20px"
                  }}
                >
                  🤖 {question}
                </p>

                <textarea
                  className="typing-box"
                  style={{height:"80px"}}
                  value={answers[index]}
                  onChange={(e)=>{

                    const updated =
                    [...answers];

                    updated[index] =
                    e.target.value;

                    setAnswers(updated);
                  }}
                />

              </div>

            ))}

          </div>

          <button
            className="analyze-btn"
            onClick={() => setShowReport(true)}
          >
            Generate Final Emotional Report
          </button>

        </div>

      ) : (

        /* FINAL REPORT */

        <div className="report-screen">

          <h1 className="report-title">
            Final Emotional Dashboard
          </h1>

          <div className="report-grid">

            <div className="report-card">
              <h2>Main Emotion</h2>
              <p>{emotion}</p>
            </div>

            <div className="report-card">
              <h2>Stress Level</h2>
              <p>{stressLevel}%</p>
            </div>

            <div className="report-card">
              <h2>Happiness Level</h2>
              <p>{happinessLevel}%</p>
            </div>

            <div className="report-card">
              <h2>Anxiety Level</h2>
              <p>{anxietyLevel}%</p>
            </div>

            <div className="report-card">
              <h2>Typing Speed</h2>
              <p>{typingSpeed} WPM</p>
            </div>

            <div className="report-card">
              <h2>Typing Accuracy</h2>
              <p>{100 - mistakes * 5}%</p>
            </div>

          </div>

          <div className="summary-box">

            <h2>
              AI Mental Health Summary
            </h2>

            <p>{getSummary()}</p>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;
