import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# تأكد من إضافة GEMINI_API_KEY في إعدادات Railway لاحقاً
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    data = request.json
    player_name = data.get("player", "لاعب")
    message = data.get("message", "")
    
    # التعليمات الخاصة بشخصية المساعد
    prompt = f"أنت مساعد ذكي داخل لعبة روبلوكس. اللاعب {player_name} يسأل: {message}. أجب باختصار وحماس."
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "عذراً، أحاول التركيز.. جرب مرة أخرى!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
