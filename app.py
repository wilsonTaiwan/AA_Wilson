from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')

GPT_INSTRUCTIONS = """
你是一位商业计划书和营运计划书专家，请按以下步骤完成内容：
1. 简要概述主题与市场需求
2. 分析目标客户及市场规模
3. 制定产品和营销策略，描述商业模式
4. 提出运营计划、团队架构和财务预测
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_plan():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": GPT_INSTRUCTIONS},
            {"role": "user", "content": f"请为以下主题生成计划：{topic}"}
        ]
    )
    plan_text = response['choices'][0]['message']['content']
    return jsonify({'plan': plan_text})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
