
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_sacred():
    cortex = get_riley_cortex()
    print("--- Sacred Testament Test ---")
    # Trigger words: "brother" or "eternal"
    result = await cortex.process_interaction(b"My eternal brother, I miss you.")
    
    print(f"Input: 'My eternal brother, I miss you.'")
    testament = result.get('testament_result', {})
    print(f"Testament State: {testament.get('state')}")
    print(f"Message: {testament.get('message')}")
    print(f"Full Response: {result['response_text']}")

if __name__ == "__main__":
    asyncio.run(test_sacred())
