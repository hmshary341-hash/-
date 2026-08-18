import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# جلب مفتاح API الخاص بـ Gemini من بيئة التشغيل السحابية
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# إعداد نموذج الذكاء الاصطناعي مع توجيهات الشخصية
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 150,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="أنت مساعد ذكي داخل لعبة روبلوكس. أجب اللاعبين باللغة العربية بأسلوب حماسي، قصير، ومفيد جداً."
)

@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    data = request.json
    player_name = data.get("player", "لاعب")
    message = data.get("message", "مرحباً")
    
    try:
        # إرسال الرسالة إلى الذكاء الاصطناعي
        chat = model.start_chat(history=[])
        response = chat.send_message(f"اللاعب {player_name} يقول: {message}")
        reply = response.text
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "عذراً، أواجه مشكلة مؤقتة في التفكير!"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
