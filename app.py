from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv


app = Flask(__name__)

openai.api_key=os.getenv("OPENAI_API_KEY")

@app.route('/start_conversation', methods=['POST'])
def run_function_calling():
    # Get user prompt from request JSON
    user_prompt = request.json.get('prompt', '')

    # Using GPT-4 to understand the intent
    chat_completion = openai.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{user_prompt} if you are asked to generate an image please respond with the word 'pn(photo needed)'",

        }
    ],
    max_tokens=60,
    model="gpt-4",
)
    result = chat_completion.choices[0].message.content.strip()
    if result != "pn(photo needed)":
        return jsonify({"result":result})

    # If the intent is to create an image
    if result == "pn(photo needed)":
        image_subject = user_prompt.strip()
        try:
            image_response = openai.images.generate(
                model="dall-e-3",
                prompt=image_subject,
                size="1024x1024"
            )
            image_url = image_response.data[0].url
            return jsonify({'image_url': image_url})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'response': 'Request not recognized or not supported yet.'})

if __name__ == '__main__':
    app.run(debug=True)

