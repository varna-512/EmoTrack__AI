import { useState } from "react";

function Questionnaire({ setQuestionnaireScore }) {

  const questions = [
    {
      question: "How often do you feel stressed?",
      options: [1, 2, 3, 4, 5]
    },
    {
      question: "How well do you sleep?",
      options: [1, 2, 3, 4, 5]
    },
    {
      question: "How often do you feel anxious?",
      options: [1, 2, 3, 4, 5]
    },
    {
      question: "How motivated are you daily?",
      options: [1, 2, 3, 4, 5]
    },
    {
      question: "How emotionally tired are you?",
      options: [1, 2, 3, 4, 5]
    }
  ];

  const [answers, setAnswers] = useState([]);

  const handleAnswer = (value) => {
    const updated = [...answers, value];
    setAnswers(updated);

    const total =
      updated.reduce((a, b) => a + b, 0);

    setQuestionnaireScore(total);
  };

  return (
    <div>

      <h1 className="panel-title">
        Mental Health Questionnaire
      </h1>

      {questions.map((q, index) => (
        <div className="card" key={index}>

          <h3>{q.question}</h3>

          {q.options.map((option) => (
            <button
              className="option-btn"
              key={option}
              onClick={() => handleAnswer(option)}
            >
              {option}
            </button>
          ))}

        </div>
      ))}

    </div>
  );
}

export default Questionnaire;