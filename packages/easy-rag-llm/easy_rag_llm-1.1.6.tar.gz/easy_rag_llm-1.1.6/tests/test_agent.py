import faiss
import numpy as np
import os
from easy_rag.agent import Agent
from dotenv import load_dotenv

load_dotenv()

def test_agent():
    d = 128
    index = faiss.IndexFlatL2(d)
    data = np.random.random((10, d)).astype(np.float32)
    index.add(data)

    agent = Agent(
        model="deepseek-chat",
        open_api_key=os.getenv("OPENAI_API_KEY"),
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
        deepseek_base_url="https://api.deepseek.com",
    )

    mock_resource = (index, [{"text": "Sample text", "file_name": "test.pdf", "page_number": i+1} for i in range(10)])
    query = "What is the content of test.pdf?"

    # Generate prompt
    agent.generate_response(mock_resource, query, return_prompt=True)

    # Output the generated prompt
    print("\nGenerated Prompt:\n", agent.last_prompt)

    # Assertions for the prompt
    assert "System:" in agent.last_prompt, "Prompt should contain system instructions."
    assert "Knowledge: start" in agent.last_prompt, "Prompt should include the Knowledge section."
    assert query in agent.last_prompt, "Prompt should include the user query."
    print("Prompt test passed.")

    try:
        # Generate and validate the response
        response = agent.generate_response(mock_resource, query)
        print("\nGenerated Response:\n", response)
        assert isinstance(response, str), "Response should be a string."
    except Exception as e:
        print("Test failed:", e)
        assert False, "Test failed."

if __name__ == "__main__":
    test_agent()
