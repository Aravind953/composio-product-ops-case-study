"""Run application-documentation searches through Composio MCP.

Reuses successful searches by default. Set FORCE_REFRESH=1 to re-search.
This agent collects evidence leads; it does not write conclusions into the CSV.
"""
import asyncio, csv, json, os, time
from pathlib import Path
from dotenv import load_dotenv
from composio import Composio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client, create_mcp_http_client

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "apps_research.csv"
RESULTS_PATH = ROOT / "data" / "search_results.json"
USER_ID = os.getenv("COMPOSIO_USER_ID", "composio-app-research")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", "5"))
DELAY_SECONDS = float(os.getenv("DELAY_SECONDS", "1"))
FORCE_REFRESH = os.getenv("FORCE_REFRESH", "0") == "1"
TOOL_SLUG = "KEENABLE_SEARCH_WEB_PUBLIC"

def load_json():
    if RESULTS_PATH.exists():
        try: return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError): print("Existing JSON unreadable; starting fresh.")
    return []

def extract_text(result):
    return "\n".join(getattr(p, "text", "") for p in (getattr(result, "content", []) or []) if getattr(p, "text", None))

def parse_response(raw):
    decoder = json.JSONDecoder()
    for i, ch in enumerate(raw):
        if ch == "{":
            try:
                obj, _ = decoder.raw_decode(raw[i:])
                if isinstance(obj, dict) and ("successful" in obj or "data" in obj): return obj
            except json.JSONDecodeError: pass
    raise ValueError("Could not parse structured Composio MCP response")

def normalise(payload):
    items = payload.get("data", payload)
    if isinstance(items, dict): items = items.get("results", items.get("data", items))
    if isinstance(items, dict): items = [items]
    out=[]
    if isinstance(items, list):
        for x in items:
            if isinstance(x, dict):
                out.append({"title":x.get("title") or x.get("name") or "",
                            "url":x.get("url") or x.get("link") or "",
                            "snippet":x.get("snippet") or x.get("description") or ""})
    return out

async def run():
    if not os.getenv("COMPOSIO_API_KEY"): raise SystemExit("Missing COMPOSIO_API_KEY in local .env")
    apps=list(csv.DictReader(CSV_PATH.open(encoding="utf-8-sig")))
    results=load_json()
    existing={x.get("app","").lower():x for x in results if x.get("status")=="success"}
    client=Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
    session=client.create(user_id=USER_ID)
    config=session.mcp
    async with create_mcp_http_client(headers=config.headers) as http:
        async with streamable_http_client(config.url,http_client=http) as (read_stream,write_stream):
            async with ClientSession(read_stream,write_stream) as mcp:
                await mcp.initialize()
                for n,app in enumerate(apps,1):
                    name=app["app"].strip()
                    if not name: continue
                    if not FORCE_REFRESH and name.lower() in existing:
                        print(f"[{n}/{len(apps)}] Reusing: {name}"); continue
                    query=f"{name} official developer documentation API reference authentication OAuth REST MCP"
                    args={"tools":[{"tool_slug":TOOL_SLUG,"arguments":{"query":query,"max_results":MAX_RESULTS,"mode":"pro","keenable_title":"Composio App Research"}}],
                          "thought":f"Find primary developer documentation for {name}; collect source links for human verification.",
                          "sync_response_to_workbench":False,"current_step":"APP_DOCUMENTATION_RESEARCH",
                          "current_step_metric":f"{n}/{len(apps)}","session_id":"mine"}
                    try:
                        response=await mcp.call_tool("COMPOSIO_MULTI_EXECUTE_TOOL",arguments=args)
                        if getattr(response,"is_error",False): raise RuntimeError(extract_text(response)[:500])
                        payload=parse_response(extract_text(response))
                        found=normalise(payload)
                        item={"id":app.get("id"),"app":name,"category":app.get("category",""),"query":query,
                              "results":found,"result_count":len(found),"status":"success" if found else "no_results",
                              "source_method":"Composio MCP"}
                    except Exception as e:
                        print("Search failed:",name,str(e))
                        item={"id":app.get("id"),"app":name,"category":app.get("category",""),"query":query,
                              "results":[],"result_count":0,"status":"failed","source_method":"Composio MCP","error":str(e)[:500]}
                    results=[x for x in results if x.get("app","").lower()!=name.lower()]+[item]
                    RESULTS_PATH.write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8")
                    await asyncio.sleep(DELAY_SECONDS)
    print(f"Saved {len(results)} app records; successful={sum(x.get('status')=='success' for x in results)}, failed={sum(x.get('status')=='failed' for x in results)}")
    print("Research conclusions remain for human verification in apps_research.csv.")

if __name__=="__main__": asyncio.run(run())
