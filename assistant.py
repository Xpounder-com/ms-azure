import openai

# Set your OpenAI API key here
openai.api_key = 'your_api_key_here'

# Creating an Assistant
assistant = openai.Assistant.create(
  model="gpt-4-turbo-preview",  # Choose the model best suited for your needs
  instructions="You are a knowledgeable assistant providing customer support.",
  tools=[{"type": "retrieval"}],  # Specify the tools your Assistant will use, e.g., knowledge retrieval
  file_ids=["file-abc123"]  # Include file_ids if you have files uploaded and want to use them with your Assistant
)

# Creating a Thread with an initial user message
thread = openai.Thread.create(
  messages=[
    {
      "role": "user",
      "content": "How do I troubleshoot my device?"
    }
  ]
)

# Running the Thread with the Assistant
run = openai.ThreadRun.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)