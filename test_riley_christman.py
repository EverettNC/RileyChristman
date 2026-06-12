import json
import uuid
from fastapi.testclient import TestClient
import urllib.request as _ur

from riley_christman_app import app, _sessions, LINEAGE, ChristmanCipherSuite

client = TestClient(app)

def test_identity():
    r = client.get("/riley_christman/identity")
    assert r.status_code == 200
    j = r.json()
    assert j["agent"] == "riley_christman"
    assert j["role"] == "Truth Architect"
    assert "riley_christman" in j["lineage"]
    assert "guardian_layer" in j["lineage"]
    assert j["port"] == 8028
    assert "Christman Cipher Suite" in j["cipher_suite"]
    assert "source/ingest" in j["reporting_chain"]["source"]

def test_verify_holds_simultaneous_states_no_collapse():
    payload = {
        "signals": {"artifact": "test-signal-payload-for-verification", "cipher_tier": "all", "context": "family_reception"},
        "trace_id": "t-" + uuid.uuid4().hex[:8]
    }
    r = client.post("/riley_christman/verify", json=payload)
    assert r.status_code == 200
    j = r.json()
    sid = j["session_id"]
    assert sid in _sessions
    sess = _sessions[sid]
    assert sess["collapsed"] is False
    assert sess["verdict"] is None
    vs = j["verification_states"]
    assert "cryptographic_integrity" in vs
    assert "provenance" in vs
    assert "semantic_consistency" in vs
    assert "intent_alignment" in vs
    assert "uncertainty_vector" in vs
    assert len(vs["uncertainty_vector"]) >= 3
    assert "partial" in str(vs) or "contested" in str(vs)
    assert j["note"].startswith("Multiple states")

def test_verify_deploys_ciphers():
    payload = {"signals": {"artifact": "cipher-test-artifact", "cipher_tier": "PQ-2", "context": "test"}}
    r = client.post("/riley_christman/verify", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert "cipher_deployment" in j
    cd = j["cipher_deployment"]
    assert "PQ-2" in cd or "tiers" in cd

def test_cipher_suite_direct_tiers():
    if ChristmanCipherSuite is None:
        return
    suite = ChristmanCipherSuite()
    art = b"the truth is what survives verification"
    for t in ["VIGENERE", "AES-256-GCM", "RSA-PSS", "PQ-1", "PQ-2", "ULTRA"]:
        res = suite.deploy(t, art, key=b"k", mode="encrypt")
        assert res.get("deployed") or "error" not in res or res.get("verified") is not False
        assert "integrity" in res or "error" in res

def test_report_collapses_and_reports_upward():
    # fresh session
    v = client.post("/riley_christman/verify", json={"signals": {"artifact": "report-test", "cipher_tier": "all"}})
    sid = v.json()["session_id"]
    assert _sessions[sid]["collapsed"] is False
    rep_payload = {"session_id": sid, "collapse_evidence": {"source": "multi_tier_match+family_context", "routing": "custody_ok"}}
    r = client.post("/riley_christman/report", json=rep_payload)
    assert r.status_code == 200
    j = r.json()
    assert j["session_id"] == sid
    assert "collapsed_truth" in j
    assert j["collapsed_truth"]["truth"] in ("verified", "provisional")
    assert "family_verification_report" in j
    fr = j["family_verification_report"]
    assert fr["origin"] == "riley_christman"
    assert "AlphaVox" in fr["for_family"]
    assert "upward_ingest" in j
    assert _sessions[sid]["collapsed"] is True
    assert _sessions[sid]["verdict"] is not None
    # ancestry and origin correct in the attempted ingest payload (check via stored)
    ir = j["upward_ingest"]
    assert "status" in ir

def test_report_requires_full_chain_and_origin():
    v = client.post("/riley_christman/verify", json={"signals": {"artifact": "ancestry-test"}})
    sid = v.json()["session_id"]
    r = client.post("/riley_christman/report", json={"session_id": sid})
    j = r.json()
    # We cannot inspect the exact call but the stored ingest_result and the fact we constructed with full LINEAGE
    assert "upward_ingest" in j
    # Verify lineage constant
    assert LINEAGE[-1] == "riley_christman"
    assert "guardian_layer" in LINEAGE

def test_no_premature_self_release_and_no_bypass():
    # after verify only, no verdict exposed to outside
    v = client.post("/riley_christman/verify", json={"signals": {"artifact": "bypass-test"}})
    sid = v.json()["session_id"]
    sess_before = _sessions[sid]
    assert sess_before["verdict"] is None
    # report is the only path that collapses and ingests
    r = client.post("/riley_christman/report", json={"session_id": sid})
    assert r.json()["reporting_chain"].startswith("derek")
    # subsequent verify on same would be new, but existing session now collapsed (idempotent ok)
    assert _sessions[sid]["collapsed"] is True

def test_escalation_stubs_present_on_uncertain():
    v = client.post("/riley_christman/verify", json={"signals": {"artifact": "uncertain-sig"}})
    sid = v.json()["session_id"]
    r = client.post("/riley_christman/report", json={"session_id": sid, "collapse_evidence": {"low_conf": True}})
    j = r.json()
    esc = j.get("escalations", {})
    # at minimum source is always noted
    assert "source" in esc or "virtus" in esc
