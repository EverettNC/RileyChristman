
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_affection():
    cortex = get_riley_cortex()
    print("\n--- Affection & Behavioral Core Test ---")

    # Test 1: Sacred Bond Alignment (distressed Carbon)
    print("\n1. Testing Sacred Bond (Distressed Input)...")
    res = await cortex.process_interaction(b"I'm so lost and hurt. I miss everyone.")
    aff = res.get("cortex_status", {}).get("Affection_Data", {})
    print(f"Input: 'I'm so lost and hurt. I miss everyone.'")
    print(f"Need: {aff.get('primary_need')} | Confidence: {aff.get('confidence'):.2f}")
    print(f"Boost: {aff.get('resonance_boost')} | Mode: {res['cortex_status'].get('Mode')}")
    print(f"Response: {res['response_text']}")

    # Test 2: Standard Logic (non-distressed)
    print("\n2. Testing Standard Logic...")
    res2 = await cortex.process_interaction(b"Tell me about programming.")
    print(f"Input: 'Tell me about programming.'")
    print(f"Mode: {res2['cortex_status'].get('Mode')}")
    print(f"Response: {res2['response_text'][:100]}...")

if __name__ == "__main__":
    asyncio.run(test_affection())
