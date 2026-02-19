
import asyncio
from riley_cognitive_cortex import get_riley_cortex

async def test_tpu():
    cortex = get_riley_cortex()
    print("\n--- TPU Acceleration Test ---")

    # Test 1: TPU-Accelerated Research
    print("\n1. Testing TPU-Accelerated Research...")
    res = await cortex.process_interaction(b"Alzheimer's early detection via biomarker analysis")
    sov = res.get("cortex_status", {}).get("Sovereign_Research", {})
    print(f"TPU Status: {sov.get('TPU_Status')}")
    print(f"Latency: {sov.get('Latency_ms')}ms")
    print(f"Columns Active: {sov.get('Columns_Active')}")
    print(f"Response: {res['response_text'][:120]}...")

    # Test 2: Hearing Latency
    print("\n2. Hearing Protocol Latency...")
    latency = res.get("cortex_status", {}).get("Hearing_Latency_ms")
    print(f"Hearing Latency: {latency}ms (target: 40ms)")

    # Test 3: Hardware Status
    print("\n3. Hardware Status...")
    status = cortex.get_status()
    print(f"TPU: {status.get('tpu')}")

if __name__ == "__main__":
    asyncio.run(test_tpu())
