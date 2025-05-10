import asyncio, re
import json as json_module
from importlib.resources import files

async def c2s_search_for(ws, c2s_code: str, waiting_time: float):
    """Phrase is made from 3 letters. Returns response json or error code."""
    while True:
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=waiting_time)
            response = response.decode('utf-8')
            phrase = rf'%xt%{c2s_code}%1%(\d+)%'
            starting_info = re.search(phrase, response)
            if starting_info is not None:
                error_code = starting_info.group(1)
                if error_code == "0":
                    response = response.replace(f'%xt%{c2s_code}%1%0%', '').rstrip('%').strip()
                    return json_module.loads(response)
                else:
                    return int(error_code)
        except asyncio.TimeoutError:
            return -1
        
def getserver(server, full: str = "full") -> str:
    """
    Get the server URL and exname from the server list.
    Full -> ws for wsuri <--> ex for empireex_xyz <--> full for both wsuri and exname"""

    data_path = files("brunogge").joinpath("server_list.json")
    with data_path.open("r", encoding="utf-8") as f:
        data = json_module.load(f)
        wsuri = data["servers"][server]["wsuri"]
        exname = data["servers"][server]["exname"]
        if full == "full":
            return wsuri, exname
        elif full == "ex":
            return exname
        elif full == "ws":  
            return wsuri
        
async def fakescanning(ws, server: str) -> None:
    """
    Fake scanning for the server.
    This function is used to hopefully avoid getting banned.
    """
    empireex = getserver(server, "ex")
    delays = [6, 2, 4, 2]
    while ws.open:
        for delay in delays:
            print("Fake scanned...")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"KID":0,"AX1":0,"AY1":0,"AX2":12,"AY2":12}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"KID":0,"AX1":1274,"AY1":0,"AX2":1286,"AY2":12}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"KID":0,"AX1":13,"AY1":0,"AX2":25,"AY2":12}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"KID":0,"AX1":1274,"AY1":13,"AX2":1286,"AY2":25}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"KID":0,"AX1":0,"AY1":13,"AX2":12,"AY2":25}}%""")
            await ws.send(f"""%xt%{empireex}%gaa%1%{{"KID":0,"AX1":13,"AY1":13,"AX2":25,"AY2":25}}%""")
            await asyncio.sleep(delay * 60) 