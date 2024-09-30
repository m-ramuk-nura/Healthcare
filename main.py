  import os
  import google.generativeai as genai

  os.environ["GEMINI_API_KEY"] = "AIzaSyD9lgGztXmBhYG49DH6ZO3HTp20Lhkmdm4"


  genai.configure(api_key=os.environ["GEMINI_API_KEY"])


  print("GEMINI_API_KEY:", os.environ.get("GEMINI_API_KEY"))

  genai.configure(api_key=os.environ["GEMINI_API_KEY"])


  generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 512,
    "response_mime_type": "text/plain",
  }


  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(
    history=[]
  )

  while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
      print("Goodbye!")
      break

    response = chat_session.send_message(user_input)

    print(f"Gemini: {response.text}")


