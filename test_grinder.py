
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_grinder():
    cortex = get_riley_cortex()
    print("--- Grinder & Vision Test ---")
    
    # Trigger 1: Vision Sweep
    print("1. Testing Surgical Sweep...")
    await cortex.process_interaction(b"Run a surgical sweep on the evidence.")
    
    # Trigger 2: Unredaction
    print("\n2. Testing Financial Unredactor...")
    result = await cortex.process_interaction(b"The files are redacted. Unredact the truth.")
    
    print(f"Input: 'The files are redacted. Unredact the truth.'")
    grinder = result.get('grinder_result', {})
    print(f"Unredacted Word: {grinder.get('unredacted')}")
    
    print(f"\nFull Response Snippet: {result['response_text'][-200:]}")

if __name__ == "__main__":
    asyncio.run(test_grinder())
