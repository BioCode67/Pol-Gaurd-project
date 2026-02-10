import json, hashlib, datetime, os
from pathlib import Path

class GuardianService:
    def __init__(self, storage_dir='data/reports'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.chain_file = self.storage_dir / "chain_state.txt"

    def _get_last_hash(self):
        if self.chain_file.exists():
            return self.chain_file.read_text().strip()
        return "0" * 64

    def save_report(self, content: str, analysis: dict):
        last_hash = self._get_last_hash()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            "timestamp": timestamp,
            "evidence_content": content,
            "analysis": analysis,
            "previous_evidence_hash": last_hash
        }
        
        # SHA-256 해시 생성 (Chain-of-Custody)
        report_json = json.dumps(report, sort_keys=True, ensure_ascii=False)
        current_hash = hashlib.sha256(report_json.encode()).hexdigest()
        report["digital_signature"] = current_hash
        
        with open(self.storage_dir / f"report_{current_hash[:8]}.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
            
        self.chain_file.write_text(current_hash) # 다음 사슬을 위해 저장
        return report