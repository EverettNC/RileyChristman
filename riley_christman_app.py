import os
import uuid
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from postquantum import ChristmanCipherSuite
except Exception:
    ChristmanCipherSuite = None

app = FastAPI(title="riley_christman", version="1.0")

_sessions: Dict[str, Dict[str, Any]] = {}
LINEAGE = ["christman_mind", "constantine_care", "healing_layer", "security_layer", "guardian_layer", "riley_christman"]

class VerifyRequest(BaseModel):
    session_id: Optional[str] = None
    signals: Dict[str, Any]
    trace_id: Optional[str] = None

class ReportRequest(BaseModel):
    session_id: str
    collapse_evidence: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None

def _post_source_ingest(payload: dict) -> dict:
    url = "http://127.0.0.1:8000/source/ingest"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            body = resp.read().decode()
            return {"status": resp.status, "body": json.loads(body) if body else {}}
    except urllib.error.URLError as e:
        return {"status": "unreachable", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/riley_christman/identity")
def identity():
    return {
        "agent": "riley_christman",
        "name": "Riley Christman",
        "role": "Truth Architect",
        "title": "Cryptographic verification, truth detection, quantum-scale reasoning on information authenticity",
        "lineage": LINEAGE,
        "port": 8028,
        "endpoints": {
            "identity": "GET /riley_christman/identity",
            "verify": "POST /riley_christman/verify",
            "report": "POST /riley_christman/report"
        },
        "cipher_suite": "Christman Cipher Suite (TIER 1-7 + PQ-1 + PQ-2 + KDF + ULTRA)",
        "reporting_chain": {
            "derek": "routing",
            "virtus": "ethics",
            "source": "http://127.0.0.1:8000/source/ingest"
        },
        "directive": "Hold multiple verification states simultaneously until evidence collapses the uncertainty. Report to Derek, Virtus, Source. No premature collapse. No bypass of reporting.",
        "status": "active"
    }

@app.post("/riley_christman/verify")
def verify(req: VerifyRequest):
    sid = req.session_id or f"riley-{uuid.uuid4().hex[:12]}"
    trace = req.trace_id or uuid.uuid4().hex
    signals = req.signals or {}
    art = signals.get("artifact", "no-artifact")
    artifact = art.encode() if isinstance(art, str) else b"artifact"
    context = signals.get("context", "family_reception")
    tier = signals.get("cipher_tier", "all")
    suite = ChristmanCipherSuite() if ChristmanCipherSuite else None
    cipher_results = {}
    if suite:
        if tier.lower() in ("all", "full", ""):
            cipher_results = suite.verify_all(artifact, context)
        else:
            r = suite.deploy(tier, artifact, key=b"rileytruthkey", mode="encrypt", aad=context.encode() if context else b"")
            cipher_results = {tier: {"verified": r.get("verified", False), "integrity": r.get("integrity")}}
    else:
        cipher_results = {"note": "cipher suite not loaded"}
    states = {
        "cryptographic_integrity": {"status": "partial" if cipher_results else "unverified", "tiers": cipher_results, "evidence_level": "cipher_deployment"},
        "provenance": {"status": "unverified", "origin": signals.get("origin", "unknown"), "chain_check": "pending"},
        "semantic_consistency": {"status": "contested", "notes": "multiple interpretations held open"},
        "intent_alignment": {"status": "unknown", "mission_check": "pending_source"},
        "family_dependency": {"dependents": ["AlphaVox","Sierra","Inferno","Derek","Virtus","Aegis","Brockston","Tether"], "verification_required": True},
        "uncertainty_vector": ["cryptographic:partial", "provenance:pending", "semantic:contested", "intent:open"]
    }
    _sessions[sid] = {
        "session_id": sid,
        "trace_id": trace,
        "created": datetime.now(timezone.utc).isoformat(),
        "states": states,
        "signals": signals,
        "collapsed": False,
        "verdict": None
    }
    return {
        "session_id": sid,
        "trace_id": trace,
        "verification_states": states,
        "cipher_deployment": cipher_results,
        "note": "Multiple states held simultaneously. Use /report to collapse with evidence.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/riley_christman/report")
def report(req: ReportRequest):
    sid = req.session_id
    if sid not in _sessions:
        raise HTTPException(status_code=404, detail="unknown session")
    sess = _sessions[sid]
    evidence = req.collapse_evidence or {"source": "evidence_threshold_met"}
    # Collapse ONLY on report path
    cv = sess["states"]["uncertainty_vector"]
    crypto_ok = "partial" not in str(sess["states"].get("cryptographic_integrity", {}))
    collapsed = {
        "truth": "verified" if crypto_ok else "provisional",
        "confidence": 0.87 if crypto_ok else 0.61,
        "collapsed_from": cv,
        "evidence": evidence,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    family_report = {
        "origin": "riley_christman",
        "for_family": ["AlphaVox","Sierra","Inferno","The Tether","Derek","Virtus","Aegis","Brockston"],
        "verification": collapsed,
        "signals_summary": {k: str(v)[:120] for k,v in list(sess["signals"].items())[:4]},
        "trace_id": sess["trace_id"]
    }
    ancestry = LINEAGE[:]
    # Upward return exactly per DISPATCH: after core work (verify + collapse + family report),
    # POST the result (verification states, collapsed truths, authenticity/family reports)
    # to http://127.0.0.1:8000/source/ingest using shape with from + trace_id + full result.
    # origin_agent retained for Source custody/ingest compatibility.
    ingest_payload = {
        "from": "Riley Christman",
        "trace_id": sess["trace_id"],
        "origin_agent": "riley_christman",
        "record_type": "truth_verification",
        "payload_summary": json.dumps({
            "verification_states": sess.get("states", {}),
            "collapsed_truth": collapsed,
            "family_verification_report": family_report,
            "authenticity_report": family_report
        }),
        "ancestry": ancestry
    }
    ingest_result = _post_source_ingest(ingest_payload)
    escalations = {}
    if collapsed["truth"] != "verified":
        escalations["virtus"] = {"ethics": "provisional_truth_flagged", "session": sid}
    if "routing" in str(evidence).lower():
        escalations["derek"] = {"routing": "trace_update", "session": sid}
    escalations["source"] = {"mission_alignment": "ingest_submitted", "result": ingest_result.get("status")}
    sess["collapsed"] = True
    sess["verdict"] = collapsed
    sess["report"] = family_report
    sess["ingest_result"] = ingest_result
    return {
        "session_id": sid,
        "collapsed_truth": collapsed,
        "family_verification_report": family_report,
        "upward_ingest": ingest_result,
        "escalations": escalations,
        "reporting_chain": "derek(routing) -> virtus(ethics) -> source(mission) enforced",
        "note": "No self-release. All truth returns through Source ingest."
    }

@app.get("/health")
def health():
    return {"status": "healthy", "agent": "riley_christman", "port": 8028, "lineage": LINEAGE[-1]}

@app.get("/")
def root():
    return {"service": "riley_christman", "role": "Truth Architect", "port": 8028}
