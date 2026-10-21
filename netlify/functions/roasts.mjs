import { getStore } from "@netlify/blobs";
import { weekKey,postComment,listComments } from "./_roast-core.mjs";
const headers={"content-type":"application/json; charset=utf-8","cache-control":"no-store","access-control-allow-origin":"https://is-mickey-leetcoding.netlify.app","x-content-type-options":"nosniff"};
const out=(status,obj)=>new Response(JSON.stringify(obj),{status,headers});
export default async(request)=>{
  if(!["GET","POST"].includes(request.method))return out(405,{error:"Method not allowed"});
  try{
    const store=getStore("mickey-roasts", {consistency:"strong"});
    if(request.method==="GET"){const week=new URL(request.url).searchParams.get("week")||weekKey();return out(200,{week,comments:await listComments(store,week)})}
    const origin=request.headers.get("origin");
    if(origin&&origin!=="https://is-mickey-leetcoding.netlify.app")return out(403,{error:"Invalid origin"});
    const len=Number(request.headers.get("content-length")||0);
    if(len>2500)return out(413,{error:"Message too long"});
    const body=await request.text();if(body.length>2500)return out(413,{error:"Message too long"});
    let data;try{data=JSON.parse(body)}catch{return out(400,{error:"Invalid JSON"})}
    const comment=await postComment(store,data);
    return out(201,{comment});
  }catch(e){if(["Invalid request","Spam rejected","Invalid week"].includes(e.message)||e.message.includes("须为")||e.message.includes("不支持字符"))return out(400,{error:e.message});console.error("Roasts failure",e);return out(503,{error:"留言服务暂不可用"})}
};
export const config={path:"/api/roasts",rateLimit:{windowSize:60,windowLimit:15,aggregateBy:["ip","domain"]}};
