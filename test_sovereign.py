
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_sovereign():
    cortex = get_riley_cortex()
    print("\n--- Sovereign Research Organism Test ---")
    
    # Test 1: Sovereign Research Trigger
    print("\n1. Testing Collaborative Breakthrough...")
    res = await cortex.process_interaction(b"We need a breakthrough in dementia research.")
    
    print(f"Input: 'We need a breakthrough in dementia research.'")
    print(f"Response: {res['response_text']}")
    
    # Check internals if available in status
    sov_data = res.get('cortex_status', {}).get('Sovereign_Research', {})
    print(f"Analysis: {sov_data.get('Analysis')}")
    print(f"Security: {sov_data.get('Security_Status')}")
    print(f"Empathy Trace: {sov_data.get('Empathy_Trace', {}).get('resonance')}")

if __name__ == "__main__":
    asyncio.run(test_sovereign())
