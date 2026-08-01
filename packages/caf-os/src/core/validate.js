const levels=new Set(["none","low","medium","high"]);
export function validateProject(p){
 if(!p||typeof p!=="object")throw new Error("Project must be an object");
 if(!/^[a-z0-9][a-z0-9-]{2,63}$/.test(p.id??""))throw new Error("Invalid project id");
 for(const k of ["title","purpose","audience","createdAt"])if(typeof p[k]!=="string"||!p[k])throw new Error(`${k} is required`);
 if(Number.isNaN(Date.parse(p.createdAt)))throw new Error("createdAt must be ISO date-time"); return p;
}
export function validateShot(s){
 if(!s||typeof s!=="object")throw new Error("Shot must be an object");
 for(const k of ["id","sceneId","description"])if(typeof s[k]!=="string"||!s[k])throw new Error(`${k} is required`);
 if(!Number.isInteger(s.characterCount)||s.characterCount<0||s.characterCount>20)throw new Error("characterCount must be 0..20");
 if(!["shot","scene","sequence","production"].includes(s.identityScope))throw new Error("Invalid identityScope");
 for(const k of ["poseRotation","dialogue","cameraComplexity","motionComplexity","occlusion","realismPriority","styleControl","budgetPriority","latencyPriority"])if(!levels.has(s[k]))throw new Error(`Invalid ${k}`);
 if(typeof s.durationSeconds!=="number"||s.durationSeconds<=0||s.durationSeconds>300)throw new Error("Invalid durationSeconds");
 for(const k of ["audioFirst","requiresLipSync","multiShot"])if(typeof s[k]!=="boolean")throw new Error(`${k} must be boolean`); return s;
}
export function validateRenderRequest(x){if(!x||typeof x!=="object")throw new Error("Request must be object");if(typeof x.projectId!=="string"||!x.projectId)throw new Error("projectId required");validateShot(x.shot);if(typeof x.prompt!=="string"||!x.prompt)throw new Error("prompt required");return x;}
