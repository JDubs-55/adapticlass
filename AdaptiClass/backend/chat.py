""""
Description: This code is designed to function as a chatbot that answers Algebra 1 questions, 
providing step-by-step solutions with brief text explanations for each step. It uses Google 
Generative AI model, Gemini, for generating the solutions. To test this chatbot via the command 
line, run the command 'python chat.py "your algebra problem here"' in the terminal within the same 
directory as this script. ~ Mary Klawa
"""

import sys
import google.generativeai as genai

if len(sys.argv) < 2:
    print("Usage: python chat.py 'Your prompt here'")
    sys.exit(1)

chat_prompt = sys.argv[1]

genai.configure(api_key="AIzaSyBIKvpvW6-RDwXMorDKCs-EJv8bBgmYxPo")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_LOW_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

directions = "For the given Algebra 1 problem, please illustrate each step towards finding the solution. Provide a concise text explanation for what each step accomplishes, aiming for clarity and brevity. It's crucial to demonstrate the process without skipping directly to the solution. If the following problem is not related to Math, please respond kindly prompting the student to stay on topic. Problem: "

full_prompt = directions + chat_prompt

prompt_parts = [{"text": full_prompt}]

response = model.generate_content(prompt_parts)

if not response.parts:
    print("No response generated. This may be due to the prompt being blocked by safety settings or another issue. Check the 'response.prompt_feedback' for more information.")
    if response.prompt_feedback:
        for feedback in response.prompt_feedback:
            print(f"Feedback: {feedback.category}, {feedback.decision}")
else:
    # response.parts can be returned to the front end
    for part in response.parts:
        print(part.text)