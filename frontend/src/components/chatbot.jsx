import { useState } from "react";
import axios from "axios";

function Chatbot({ setEmotion }) {

  const [text, setText] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text:
      "Hello 👋 I am EmoTrack AI. Tell me how you are feeling today."
    }
  ]);

  const [typing, setTyping] = useState(false);

  const sendMessage = async () => {

    if(text.trim() === ""){
      return;
    }

    const userMessage = {
      sender:"user",
      text:text
    };

    setMessages((prev) => [
      ...prev,
      userMessage
    ]);

    setTyping(true);

    try{

      const response =
      await axios.post(
        "http://127.0.0.1:8000/api/predict/",
        {
          text:text
        }
      );

      const detectedEmotion =
      response.data.emotion;

      setEmotion(detectedEmotion);

      let aiReply = "";

      if(detectedEmotion === "happy"){

        aiReply =
        "😊 You seem happy today. What made your day feel positive?";
      }

      else if(detectedEmotion === "sad"){

        aiReply =
        "💙 I can sense sadness. Have you been emotionally tired recently?";
      }

      else if(detectedEmotion === "stressed"){

        aiReply =
        "🌙 You seem mentally stressed. Are studies or work overwhelming you?";
      }

      else if(detectedEmotion === "angry"){

        aiReply =
        "🔥 I notice frustration in your words. Would you like to explain what happened?";
      }

      else{

        aiReply =
        "🤖 Tell me more about your emotional state.";
      }

      setTimeout(() => {

        const aiMessage = {
          sender:"ai",
          text:aiReply
        };

        setMessages((prev) => [
          ...prev,
          aiMessage
        ]);

        setTyping(false);

      },1200);

    }

    catch(error){

      console.log(error);

      setTyping(false);
    }

    setText("");
  };

  return (

    <div>

      <h1 className="panel-title">
        Emotion AI Chatbot
      </h1>

      <div
        style={{
          height:"500px",
          overflowY:"auto",
          marginBottom:"20px"
        }}
      >

        {
          messages.map((msg,index) => (

            <div
              key={index}
              className="chat-message"
              style={{
                background:
                msg.sender === "user"
                ?
                "#2563eb55"
                :
                "rgba(255,255,255,0.05)"
              }}
            >

              {msg.text}

            </div>
          ))
        }

        {
          typing && (

            <div className="chat-message">

              AI is typing...

            </div>
          )
        }

      </div>

      <textarea
        placeholder="Type your feelings..."
        value={text}
        onChange={(e) =>
          setText(e.target.value)
        }
      />

      <button onClick={sendMessage}>
        Send Message
      </button>

    </div>
  );
}

export default Chatbot;