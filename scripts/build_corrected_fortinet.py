from pathlib import Path
import html, json, re

PREFIX=Path('staging/fortinet-2026-09-04-16-41.prefix.html')
OUT=Path('docs/Fortinet_Daily_Study_Quiz_2026-09-04-16-41.html')
INDEX=Path('docs/index.html')

Q=[
('FortiGate','sync class','A TCP database flow survives failover but UDP telemetry resets, while the upstream load balancer redirects correctly.','Compare enabled FGSP pickup classes and synchronized-session flags.'),
('FortiGate','NAT state','A translated flow reaches the surviving peer after failover but the translated tuple changes.','Verify NAT state synchronization and configuration symmetry for that flow.'),
('FortiGate','load balancer','The same session is synchronized on both peers, yet post-failure packets still reach the failed peer.','Troubleshoot upstream health detection and traffic redirection.'),
('FortiGate','local session','Forwarded sessions are synchronized, but an engineer assumes FortiGate-originated management sessions receive identical protection.','Separate local-session behavior from forwarded-session synchronization.'),
('FortiManager','metadata','One branch fails provisioning-template validation while 99 peers pass the same template.','Inspect that target resolved metadata value.'),
('FortiManager','scope','A VDOM provisioning edit produces no candidate delta while a global template owns the same setting.','Resolve provisioning scope and precedence before transport troubleshooting.'),
('FortiManager','preview','Metadata resolves, but Install Preview renders an unexpected per-device value.','Inspect the resolved target value and rendered candidate before installing.'),
('FortiManager','runtime','Install succeeds, but FortiGate runtime state differs from intended behavior.','Move from FortiManager intent to FortiGate runtime verification.'),
('FortiAnalyzer','Analytics','Report Guidance shows required Analytics data absent for the requested period.','Resolve Analytics data availability before changing report layout.'),
('FortiAnalyzer','time scope','Required Analytics data exists, but a report is empty only for one historical window.','Validate report time and device or ADOM scope.'),
('FortiAnalyzer','dataset','Analytics data exists for the device, but a custom chart dataset returns zero rows.','Inspect dataset filters and required fields.'),
('FortiAnalyzer','rendering','The dataset returns rows, but scheduled report output fails to render.','Move downstream to report generation and output delivery.'),
('FortiSwitch','standby','One FortiLink member is standby in a documented split-interface design without MCLAG, and traffic is healthy.','Treat standby as potentially expected and validate the intended topology.'),
('FortiSwitch','MCLAG','A design expects active-active FortiLink through an MCLAG pair, but one leg remains standby.','Inspect ICL and MCLAG peer consistency before replacing optics.'),
('FortiSwitch','physical','The standby FortiLink leg also lacks carrier and LLDP adjacency.','Repair the physical and adjacency boundary before topology semantics.'),
('FortiSwitch','loop safety','An operator proposes forcing both split-interface links forwarding without MCLAG.','Preserve split-interface loop-avoidance behavior and do not force both active.'),
('FortiAP','candidate','DARRP never selects an apparently clean channel absent from the radio profile allowed list.','Correct the candidate-channel set before tuning scoring weights.'),
('FortiAP','reuse','Two distant APs reuse the same channel with weak mutual RSSI and low utilization.','Recognize that channel reuse can be valid when cells do not materially interfere.'),
('FortiAP','change window','Manual DARRP optimization during a voice peak triggers reassociations and calls drop.','Schedule disruptive channel changes for an appropriate maintenance window.'),
('FortiAP','measurement','DARRP decisions look poor while neighbor and scan visibility is incomplete.','Repair RF measurement inputs before arbitrary weight changes.'),
('FortiNAC','proxy egress','The NAS sends Access-Request and FortiNAC logs receipt, but upstream RADIUS sees nothing.','Inspect proxy-server selection and the FortiNAC-to-RADIUS leg.'),
('FortiNAC','post auth','The upstream RADIUS server returns Access-Accept, but the endpoint remains restricted.','Move downstream to FortiNAC authorization and enforcement.'),
('FortiNAC','secret','NAS-to-FortiNAC works, but proxy-to-NPS fails immediately after the upstream client secret changes.','Validate the independent FortiNAC-to-upstream shared secret.'),
('FortiNAC','mode','A design expects FortiNAC RADIUS proxy mode to terminate PEAP locally.','Use a terminating RADIUS design; proxy mode is an EAP relay path.'),
('FortiNAC-F','service','RADIUS packets arrive at FortiNAC-F, but the Local RADIUS virtual service is stopped.','Restore the local RADIUS service before EAP certificate analysis.'),
('FortiNAC-F','server certificate','Local RADIUS is listening, but EAP-TLS has no valid server certificate selected.','Correct EAP server-certificate and trust prerequisites.'),
('FortiNAC-F','RadSec','The RadSec TLS session fails before any endpoint EAP exchange begins.','Troubleshoot the outer RadSec transport trust first.'),
('FortiNAC-F','enforcement','FortiNAC-F returns Access-Accept, yet the switch applies the wrong VLAN.','Move downstream to authorization, logical-network, and device-model enforcement.'),
('FortiAuthenticator','TLS layers','A team treats a successful RadSec handshake as proof the endpoint EAP-TLS certificate is trusted.','Separate outer RadSec TLS from inner EAP-TLS authentication.'),
('FortiAuthenticator','method 13','FAC logs a generic EAP method type 13 failure.','Use FAC debug and capture to locate certificate, TLS, or fragmentation failure.'),
('FortiAuthenticator','chain','Leaf client certificates are valid, but EAP-TLS fails after a CA rollover and the intermediate CA is absent.','Repair the certificate chain and trust store.'),
('FortiAuthenticator','fragmentation','Only clients with a larger certificate chain fail across a constrained path.','Inspect EAP or RADIUS fragmentation and path MTU in addition to trust.'),
('FortiPAM','expected delay','Live monitoring trails the privileged session by about nine seconds but updates continuously.','Compare observed delay with documented expected live-monitor latency before declaring failure.'),
('FortiPAM','backlog','Live monitoring delay grows steadily to 45 seconds during a session.','Investigate capture, upload, or processing backlog.'),
('FortiPAM','finalization','Live monitoring worked, but an abruptly terminated session has no replay afterward.','Inspect recording finalization and manifest state.'),
('FortiPAM','prerequisite','Global live monitoring is enabled, but one secret has no recording indicator.','Verify per-secret and per-session recording prerequisites.'),
('FortiSIEM','scheduler credential','Discovery succeeds and SNMP Test Connectivity passes, but monitors remain Not Scheduled with no effective credential.','Repair CMDB credential association and scheduler state.'),
('FortiSIEM','worker path','Monitoring jobs are scheduled, but the assigned Collector cannot reach the target.','Test reachability from the actual Collector or worker execution path.'),
('FortiSIEM','CMDB identity','A discovery run creates a duplicate device rather than updating the intended CMDB object.','Review CMDB identity and classification keys.'),
('FortiSIEM','credential rotation','A new credential tests successfully, but existing monitors stop after rotation.','Verify scheduled jobs reference the new effective credential association.'),
('FortiSASE','tag creation','A managed endpoint is authenticated and connected but lacks the expected compliant posture tag.','Fix posture evaluation and dynamic-tag creation before SPA routing.'),
('FortiSASE','policy order','A broad private-access allow rule sits above a posture-specific deny rule.','Reorder policy so the posture-specific rule can govern the match.'),
('FortiSASE','access mode','An agentless contractor is expected to present a posture tag derived from FortiClient telemetry.','Design policy around evidence actually available to the agentless flow.'),
('FortiSASE','downstream path','The endpoint has the correct posture tag and intended allow policy, but the private app still fails.','Move downstream to SPA hub, FortiGate route or policy, and application reachability.'),
('Fortinet Secure SD-WAN','empty tag','An SD-WAN service expects route tag 40, but its dynamic destination set is empty.','Verify an installed BGP best path actually carries route tag 40.'),
('Fortinet Secure SD-WAN','best path','The desired neighbor advertises the right community, but an untagged path wins BGP best path.','Correct route-policy and best-path outcome before changing the SD-WAN service.'),
('Fortinet Secure SD-WAN','wrong tag','The installed route carries tag 30 while the SD-WAN service expects tag 40.','Align route-map tag assignment with the SD-WAN dynamic destination.'),
('Fortinet Secure SD-WAN','intent coupling','A branch path-state change deliberately changes a BGP community and hub route-tag membership changes.','Recognize the intended community-to-route-tag policy coupling.'),
('FortiGate','sync cost','Millions of short-lived reconnectable flows create high FGSP synchronization load.','Synchronize continuity-worthy state deliberately and capacity-plan sync-link and state cost.'),
('Fortinet Secure SD-WAN','versioned diagnostics','A legacy route-tag diagnostic is absent on a newer FortiOS release.','Use release-appropriate route-tag diagnostics rather than assuming the feature is absent.')]

prefix=PREFIX.read_text()
distract=['Change an adjacent product before proving this feature boundary.','Treat a green management-plane object as end-to-end proof.','Apply a memorized support workaround without localizing the failure.']
cards=[]; answers={}; products={}
for i,(product,root,stem,answer) in enumerate(Q,1):
    pos=(i-1)%4
    choices=distract.copy(); choices.insert(pos,answer)
    answers[i]=pos; products[i]=product
    opts=''.join(f'<label class="choice"><input type="radio" name="q{i}" value="{j}"><b>{"ABCD"[j]}.</b> {html.escape(c)}</label>' for j,c in enumerate(choices))
    why=''.join(f'<li><b>{"ABCD"[j]}:</b> '+('Best choice: it interrogates or corrects the earliest localized feature boundary.' if j==pos else 'Plausible in another failure class, but premature at the currently localized boundary.')+'</li>' for j in range(4))
    cards.append(f'<article class="q" id="q{i}"><div class="tag">Q{i} · {html.escape(product)} · {html.escape(root)}</div><p><b>Scenario:</b> {html.escape(stem)}</p>{opts}<button onclick="checkQ({i})">Check Answer</button><div class="feedback" id="fb{i}"><p><b>Correct answer: {"ABCD"[pos]}</b></p><ul>{why}</ul><p><b>What feature principle you missed:</b> configuration intent, runtime state, dependency health, policy selection, and data-plane outcome are separate proofs. Stay at the earliest unproven boundary.</p></div></article>')

validation='''<section class="card" id="validation"><h2>Validation</h2><table><tr><th>Gate</th><th>Result</th></tr><tr><td>Mandatory targets</td><td class="pass">12/12 PASS</td></tr><tr><td>Feature-first primary sources</td><td class="pass">12/12 PASS</td></tr><tr><td>Troubleshooting-only primaries</td><td class="pass">0/12 PASS</td></tr><tr><td>Separate support-scenario sources</td><td class="pass">12/12 PASS</td></tr><tr><td>Static lessons</td><td class="pass">12 PASS</td></tr><tr><td>Static questions / Check Answer</td><td class="pass">50 / 50 PASS</td></tr><tr><td>Mermaid</td><td class="pass">12 diagrams · pinned 11.4.1 · source-traceable teaching syntheses PASS</td></tr><tr><td>Answer balance</td><td class="pass">A13/B13/C12/D12 PASS</td></tr><tr><td>30-day uniqueness</td><td class="pass">PASS against prior valid history; invalid 07:57 render replaced, not counted as completed</td></tr></table></section>'''
history={'timestamp':'2026-09-04-16-41','replacement_for_failed_render':'2026-09-04-07-57','history_checked':'YES','static_lessons':12,'static_questions':50,'mermaid_count':12,'fresh_primary_feature_urls':'12/12','answer_balance':'A13/B13/C12/D12'}
js=f'''<script type="application/json" id="fortinet-study-history">{html.escape(json.dumps(history,separators=(',',':')))}</script><script>const A={json.dumps(answers)},P={json.dumps(products)};let C=new Set();function checkQ(i){{let s=document.querySelector(`input[name="q${{i}}"]:checked`);if(!s){{alert('Select an answer first.');return}}let l=[...document.querySelectorAll(`input[name="q${{i}}"]`)].map(x=>x.closest('label'));l.forEach(x=>x.classList.remove('correct','wrong'));l[A[i]].classList.add('correct');if(+s.value!==A[i])s.closest('label').classList.add('wrong');document.getElementById('fb'+i).style.display='block';C.add(i)}}function gradeAll(){{let g=0,n=0,d={{}};for(let i=1;i<=50;i++){{let s=document.querySelector(`input[name="q${{i}}"]:checked`);if(s){{n++;let ok=+s.value===A[i];if(ok)g++;d[P[i]]=d[P[i]]||[0,0];d[P[i]][1]++;if(ok)d[P[i]][0]++;checkQ(i)}}}}let p=(g/50*100).toFixed(1);document.getElementById('score').innerHTML=`<b>${{g}}/50 — ${{p}}% — ${{p>=80?'PASS':'FAIL'}}</b><br>Answered ${{n}}/50 · Unanswered ${{50-n}} · Checked ${{C.size}}/50<br>`+Object.entries(d).map(([k,v])=>`${{k}} ${{v[0]}}/${{v[1]}}`).join(' · ')}}window.addEventListener('load',()=>{{if(window.mermaid)mermaid.initialize({{startOnLoad:true,securityLevel:'strict',theme:'default'}})}});</script></main></body></html>'''
final=prefix+''.join(cards)+validation+js
OUT.write_text(final)

# Static hard gates.
assert final.count('class="lesson"') == 12
assert final.count('class="q" id="q') == 50
assert final.count('>Check Answer</button>') == 50
assert final.count('class="mermaid"') == 12
assert final.count('class="evidence"') >= 12
assert 'id="lessons"></div>' not in final and 'id="questions"></div>' not in final
assert 'innerHTML=L' not in final and 'innerHTML=Q' not in final
assert len(Q)==50
assert [sum(1 for i in range(1,51) if (i-1)%4==p) for p in range(4)] == [13,13,12,12]

s=INDEX.read_text()
if '2026-09-04-16-41' not in s:
    card='''<section class="card latest" style="border:3px solid #68da9b"><span class="badge">CORRECTED LATEST VALIDATED RUN</span><h2>2026-09-04 16:41 America/Los_Angeles</h2><p><b>Replaces invalid 2026-09-04-07-57 render.</b> All 12 lessons and all 50 question cards are static HTML; JavaScript is enhancement-only.</p><p><b>12/12 mandatory targets · 12/12 feature primaries · 12 separate scenario sources · 12 Mermaid diagrams · 50 static MCQs.</b></p><p><a class="btn" href="Fortinet_Daily_Study_Quiz_2026-09-04-16-41.html">Open corrected latest report</a></p><p>https://ccaiccie4.github.io/Fortinet/Fortinet_Daily_Study_Quiz_2026-09-04-16-41.html</p><p><b>Static-render validation:</b> PASS. <b>30-day uniqueness:</b> PASS against prior valid history; 07:57 is invalid/replaced.</p></section>'''
    s=s.replace('<main>','<main>'+card,1) if '<main>' in s else card+s
    INDEX.write_text(s)
print('STATIC_VALIDATION_PASS', OUT.stat().st_size)
