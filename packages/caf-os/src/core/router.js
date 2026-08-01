const n={none:0,low:1,medium:2,high:3};
const base=provider=>({provider,score:0,reasons:[],risks:[]}); const add=(s,p,r)=>{s.score+=p;s.reasons.push(r)}; const risk=(s,r)=>s.risks.push(r);
export function routeShot(shot){
 const scores=["kling","seedance","lora","avatar","assembly","mock"].map(base); const by=Object.fromEntries(scores.map(s=>[s.provider,s]));
 if(shot.characterCount===1&&!shot.multiShot)add(by.kling,4,"Single-subject isolated shot suits first-frame motion extension.");
 if(n[shot.poseRotation]<=1)add(by.kling,3,"Low pose rotation reduces first-frame identity drift risk.");else risk(by.kling,"Large pose rotation can destabilise facial geometry.");
 if(n[shot.motionComplexity]>=2||n[shot.realismPriority]>=2)add(by.kling,3,"Natural motion and realism are high priorities.");
 if(shot.multiShot){add(by.seedance,6,"Sequence requires multi-shot continuity.");risk(by.kling,"Cross-shot identity is not guaranteed by a single start frame.");}
 if(n[shot.cameraComplexity]>=2)add(by.seedance,4,"Complex camera grammar benefits from sequence-level generation.");
 if(shot.requiresLipSync&&n[shot.dialogue]>=2){add(by.seedance,3,"Dialogue-heavy sequence benefits from integrated reference and timing control.");add(by.avatar,2,"Precise phoneme delivery is useful where staging is presenter-like.");}
 if(["production","sequence"].includes(shot.identityScope)){add(by.lora,5,"Long persistence scope can justify trained identity conditioning.");add(by.seedance,3,"Persistent multi-angle reference binding suits long continuity.");}
 if(n[shot.styleControl]>=2)add(by.lora,4,"High style control favours composable or trained workflows.");
 if(shot.cameraComplexity==="none"&&shot.motionComplexity==="none"&&shot.requiresLipSync)add(by.avatar,6,"Locked talking-head delivery matches avatar architecture.");
 if(n[shot.budgetPriority]>=2&&n[shot.latencyPriority]>=2&&!shot.multiShot)add(by.assembly,4,"Fast assembly is prioritised over cinematic character continuity.");
 add(by.mock,1,"Local deterministic execution is available for testing.");
 for(const s of scores){if(shot.characterCount>1&&s.provider==="kling")risk(s,"Multiple principal faces increase target-lock ambiguity.");if(n[shot.occlusion]>=2&&["kling","avatar"].includes(s.provider))risk(s,"Face occlusion can impair identity and lip alignment.");}
 scores.sort((a,b)=>b.score-a.score||a.provider.localeCompare(b.provider)); const gap=scores[0].score-scores[1].score;
 return {primary:scores[0],alternative:scores[1],confidence:gap>=4?"high":gap>=2?"medium":"low",evaluatedAt:new Date().toISOString()};
}
