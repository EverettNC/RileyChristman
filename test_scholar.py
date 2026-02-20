
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_scholar():
    cortex = get_riley_cortex()
    print("--- Scholar Test ---")
    result = await cortex.process_interaction(b"I hear a distressed hum.")
    print(f"Input: 'I hear a distressed hum.'")
    print(f"Clinical Report: {result.get('clinical_context', 'None')}")
    print(f"Full Response: {result['response_text']}")

if __name__ == "__main__":
    asyncio.run(test_scholar())
