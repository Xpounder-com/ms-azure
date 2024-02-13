import openai

# Set your OpenAI API key here
openai.api_key = 'your_api_key_here'

# Creating an Assistant
assistant = openai.Assistant.create(
  model="gpt-4-turbo-preview",  # Choose the model 
  instructions="You are a knowledgeable assistant providing customer support.",
  tools=[{"type": "retrieval"}],  # Specify the tools your Assistant will use, e.g., knowledge retrieval
  file_ids=["file_id_1", "file_id_2", "file_id_3"]  # Include file_ids if you want to use them with your Assistant
)

# Creating a Thread with an initial user message
thread = openai.Thread.create(
  messages=[
    {
      "role": "user",
      "content": "How do I troubleshoot my device?"
      "file_ids": ["file_id_1", "file_id_2", "file_id_3"] 
    }
  ]
)

# Running the Thread with the Assistant
run = openai.ThreadRun.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)