#!/usr/bin/env python3
"""Read-only fail-closed paperwork precheck; never makes a generation call."""
from pathlib import Path
import json, sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent/'j4_authorization_template.json'
a=json.loads(p.read_text(encoding='utf-8'))
conditions={
 'Neon explicit GO':bool(a.get('neon_explicit_go') and a.get('neon_approval_evidence')),
 'Director estimate posted':bool(a.get('director_posted_estimate_to_service') and a.get('director_post_evidence')),
 'Current pricing verified':bool(a.get('current_provider_pricing_verified')),
 'Monthly headroom evidence':bool(a.get('monthly_headroom_evidence')),
 'Rights review complete':bool(a.get('asset_rights_and_contest_review_complete')),
}
used=a.get('credits_already_used_verified');planned=a.get('proposed_generation_credits_verified');limit=a.get('month_credits_limit',9000)
conditions['Budget arithmetic verified']=(isinstance(used,(int,float)) and not isinstance(used,bool) and isinstance(planned,(int,float)) and not isinstance(planned,bool) and used>=0 and planned>0 and used+planned<=limit)
for name,ok in conditions.items():print(('CHECK' if ok else 'BLOCK')+': '+name)
print('LOCAL PAPERWORK '+('READY_FOR_HUMAN_CONFIRMATION' if all(conditions.values()) else 'BLOCKED')+'; does not authorize actual provider generation.')
sys.exit(0 if all(conditions.values()) else 2)
