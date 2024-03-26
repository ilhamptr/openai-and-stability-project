from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv


app = Flask(__name__)

openai.api_key=os.getenv("OPENAI_API_KEY")

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.json["description"]
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return jsonify({"image":image_url})
if __name__ == '__main__':
    app.run(debug=True)
