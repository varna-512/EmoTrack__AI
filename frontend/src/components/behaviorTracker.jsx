import { useEffect, useState } from "react";

function BehaviorTracker({ onBehaviorUpdate }) {

  const [startTime] = useState(Date.now());

  const [keystrokes, setKeystrokes] =
    useState(0);

  const [mistakes, setMistakes] =
    useState(0);

  const [speed, setSpeed] =
    useState(0);

  const [accuracy, setAccuracy] =
    useState(100);

  useEffect(() => {

    const handleKey = (e) => {

      setKeystrokes((prev) => prev + 1);

      if(e.key === "Backspace"){

        setMistakes((prev) => prev + 1);
      }

      const currentTime =
      (Date.now() - startTime) / 1000;

      const calculatedSpeed =
      (
        (keystrokes / 5 / currentTime) * 60
      ) || 0;

      const calculatedAccuracy =
      keystrokes > 0
      ?
      (
        (
          (keystrokes - mistakes)
          /
          keystrokes
        ) * 100
      ).toFixed(1)
      :
      100;

      setSpeed(
        calculatedSpeed.toFixed(1)
      );

      setAccuracy(
        calculatedAccuracy
      );

      onBehaviorUpdate({

        speed:
        calculatedSpeed.toFixed(1),

        accuracy:
        calculatedAccuracy,

        mistakes,
      });
    };

    window.addEventListener(
      "keydown",
      handleKey
    );

    return () => {

      window.removeEventListener(
        "keydown",
        handleKey
      );
    };

  },[
    keystrokes,
    mistakes,
    startTime,
    onBehaviorUpdate
  ]);

  return (

    <div>

      <h1 className="panel-title">
        Live Behavior Analysis
      </h1>

      <div className="report-box">

        <div className="stat">
          ⌨ Typing Speed:
          {" "}
          {speed}
          {" "}
          WPM
        </div>

        <div className="stat">
          🎯 Accuracy:
          {" "}
          {accuracy}
          %
        </div>

        <div className="stat">
          ⚠ Mistakes:
          {" "}
          {mistakes}
        </div>

        <div
          className="stat"
          style={{
            marginTop:"25px",
            color:"#38bdf8",
            fontSize:"22px",
            fontWeight:"700"
          }}
        >
          Behavioral Monitoring Active
        </div>

      </div>

    </div>
  );
}

export default BehaviorTracker;