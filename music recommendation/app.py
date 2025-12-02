from flask import Flask, render_template, request, jsonify
from rag_chatbot import RAGChatbot
import os

# Flask 앱 초기화
app = Flask(__name__)

# RAG 챗봇 인스턴스 생성
# 웹 서버가 시작될 때 한 번만 실행되어 모델과 인덱스를 메모리에 로드합니다.
print("Initializing RAG Chatbot...")
chatbot = RAGChatbot()
print("Chatbot initialized.")

@app.route("/")
def index():
    """메인 페이지를 렌더링합니다."""
    return render_template("index.html")

@app.route("/chat", methods=['POST'])
def chat():
    """
    사용자 메시지를 받아 챗봇의 답변을 반환하는 API 엔드포인트
    """
    try:
        user_message = request.json['message']
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # 챗봇으로부터 답변 생성
        bot_response = chatbot.generate_response(user_message)
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error during chat: {e}")
        return jsonify({"error": "Sorry, an error occurred while generating a response."}), 500

if __name__ == '__main__':
    # host='0.0.0.0'는 외부에서도 접속 가능하도록 설정합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)