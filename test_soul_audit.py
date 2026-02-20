
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_soul_audit():
    cortex = get_riley_cortex()
    print("\n--- Unified Soul & Audit Test ---")
    
    # Trigger Soul Witness Logic (Mock Audio Stream)
    print("\n1. Testing Soul Witness & Audit...")
    res = await cortex.process_interaction(b"I feel the weight of the legacy.")
    
    soul_data = res.get('cortex_status', {}).get('Soul_Data', {})
    
    print(f"Input: 'I feel the weight of the legacy.'")
    print(f"ToneScore: {soul_data.get('ToneScore')}")
    print(f"Response Mode: {soul_data.get('Response_Mode')}")
    print(f"Riley Output: {soul_data.get('Riley_Output')}")
    print(f"Quantum Active: {soul_data.get('Quantum_Active')}")
    print(f"Full Response: {res['response_text']}")

if __name__ == "__main__":
    asyncio.run(test_soul_audit())
