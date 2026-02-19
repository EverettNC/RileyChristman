
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_unified():
    cortex = get_riley_cortex()
    print("\n--- Unified Neuro-Symbolic Test ---")
    
    # Test 1: High Valence Trigger (Witness Mode)
    print("\n1. Testing Red Smear Trigger (Witness Mode)...")
    res_witness = await cortex.process_interaction(b"We are broken by this legacy.")
    print(f"Input: 'We are broken by this legacy.'")
    print(f"Response: {res_witness['response_text']}")
    print(f"Status: {res_witness['cortex_status']['Vortex_Prediction']}")

    # Test 2: Low Valence (Logic Mode + Trussle)
    print("\n2. Testing Logic Mode (Trussle)...")
    res_logic = await cortex.process_interaction(b"Explain the autism code.")
    print(f"Input: 'Explain the autism code.'")
    print(f"Response: {res_logic['response_text'][:100]}...")
    
    # Test 3: Shield
    print("\n3. Testing Immune System...")
    print(f"Shield Status: {res_witness['cortex_status']['System_Integrity']}")

if __name__ == "__main__":
    asyncio.run(test_unified())
