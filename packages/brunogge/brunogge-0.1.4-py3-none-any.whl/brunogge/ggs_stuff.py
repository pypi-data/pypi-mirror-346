import websockets, asyncio, random, re
import json as json_module
from .just_funcs import getserver
async def ggs_login(ws, nick: str, pwrd: str, server: str, kid: int = "0") -> None:
    
    """
    Login function which logins to your account.
    """
    if ws.open:
        await ws.send(f"""<msg t='sys'><body action='verChk' r='0'><ver v='166' /></body></msg>""")
        await ws.send(f"""<msg t='sys'><body action='login' r='0'><login z='{server}'><nick><![CDATA[]]></nick><pword><![CDATA[605015%pl%0]]></pword></login></body></msg>""")
        await ws.send(f"""<msg t='sys'><body action='autoJoin' r='-1'></body></msg>""")
        await ws.send(f"""<msg t='sys'><body action='roundTrip' r='1'></body></msg>""")
        await ws.send(f"""%xt%{server}%lli%1%{{"CONM":625,"RTM":56,"ID":0,"PL":1,"NOM":"{nick}","PW":"{pwrd}","LT":null,"LANG":"pl","DID":"0","AID":"1726521097373776320","KID":"","REF":"https://empire.goodgamestudios.com","GCI":"","SID":9,"PLFID":1}}%""")
        await ws.send(f"%xt%{server}%nch%1%")
        while ws.open:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5.5)
                response = response.decode('utf-8')

                if "%xt%lli%1%" in response:
                    if "%xt%lli%1%0%" not in response:
                        print("Wrong login data.")
                        exit()
                elif "%xt%gbd%1%0%" in response:
                    response = response.replace('%xt%gbd%1%0%', '').rstrip('%').strip()
                    response = json_module.loads(response)
                    lids = []
                    fragments = response["gli"]["C"]
                    for fragment in fragments:
                        lids.append(fragment["ID"])
                    lids = sorted(lids)
                    break
            except asyncio.TimeoutError:
                break

        await ws.send(f"""%xt%{server}%core_gic%1%{{"T":"link","CC":"PL","RR":"html5"}}%""")
        await ws.send(f"%xt%{server}%gbl%1%{{}}%")
        await ws.send(f"""%xt%{server}%jca%1%{{"CID":-1,"KID":0}}%""")
        await ws.send(f"%xt%{server}%alb%1%{{}}%")
        await ws.send(f"%xt%{server}%sli%1%{{}}%")
        await ws.send(f"%xt%{server}%gie%1%{{}}%")
        await ws.send(f"%xt%{server}%asc%1%{{}}%")
        await ws.send(f"%xt%{server}%sie%1%{{}}%")
        await ws.send(f"""%xt%{server}%ffi%1%{{"FIDS":[1]}}%""")
        await ws.send(f"%xt%{server}%kli%1%{{}}%")
        while ws.open:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=2)
                response = response.decode('utf-8')
                if "%xt%jaa%1%0%" in response:
                    pattern = rf"\[{kid},(\d+),(\d+),(\d+),1"
                    match = re.search(pattern, response)
                    cid = match.group(1)
                    global sx, sy
                    sx = match.group(2)
                    sy = match.group(3)
                    break
            except asyncio.TimeoutError:
                break

        while ws.open:
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=3.5)
                response = response.decode('utf-8')
                if "%xt%ffi%1%0%" in response:
                    await ws.send(f"%xt%{server}%gcs%1%{{}}%")
                    print("Successfully logged in")
                    break
            except asyncio.TimeoutError:
                break
    else:
        print("Connection closed, stopping login")
    sx = int(sx)
    sy = int(sy)
    return sx, sy, lids, cid

async def keeping(ws, server):
    while ws.open:
        try:
            await ws.send(f"%xt%{server}%pin%1%<RoundHouseKick>%")
            print("Sending keep-alive message...")
            await asyncio.sleep(60)  # Keep-alive interval
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed, stopping keep-alive")
            break

async def ggs_account(ws, nick, pwrd, server) -> None:
    """Login to the account and trigger next functions."""
    print("Logging in...")
    try:
        server = getserver(server, "ex")
        keepconnect = asyncio.create_task(keeping(ws, server))
        sx, sy, lids, cid = await ggs_login(ws, nick, pwrd, server)
        print("Keeping connection alive...")
        while ws.open:
            await asyncio.sleep(100)
    except websockets.exceptions.ConnectionClosedError:
        print("Theoretically you should never see this. If you do, pray for your account.")
    