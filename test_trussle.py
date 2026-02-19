
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_trussle():
    cortex = get_riley_cortex()
    print("--- Trussle RAG Test ---")
    # Trigger keywords: "autism", "stimming"
    result = await cortex.process_interaction(b"Tell me about autism and stimming.")
    
    print(f"Input: 'Tell me about autism and stimming.'")
    trussle = result.get('trussle_result', [])
    print(f"Trussle Insights: {len(trussle)}")
    if trussle:
        print(f"Top Result: {trussle[0]['content']}")
    
    print(f"\nFull Response Snippet: {result['response_text'][:200]}...")

if __name__ == "__main__":
    asyncio.run(test_trussle())
