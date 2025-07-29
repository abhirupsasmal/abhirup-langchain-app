from flask import Flask, render_template, request, make_response
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])

def generate():
  if request.method == 'POST':
    if request.is_json:
      req_json = request.get_json()
      prompt = req_json.get('prompt')
    else:
      return make_response("Request must be JSON", 400)
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        return make_response("OpenAI API key not configured", 500)
    
    prompt_template = PromptTemplate.from_template("Generate a blog on title {prompt}?")
    llm = OpenAI(temperature=0.3)

    chain = LLMChain(llm=llm, prompt=prompt_template)
    output = chain.run(prompt)
    print(output)
    return output

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
