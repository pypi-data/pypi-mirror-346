### OUTDATED DONT USE ->>import asyncio, json, websockets, math, random, time, os, sys, re
### OUTDATED DONT USE ->>from datetime import datetime
### OUTDATED DONT USE ->>message_queue = []
### OUTDATED DONT USE ->>time_list = []
### OUTDATED DONT USE ->>async def generatescans(kid, distance, sx, sy, servers, rect_width=13, rect_height=13):
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>    min_x = (sx-distance)
### OUTDATED DONT USE ->>    max_x = (sx+distance)
### OUTDATED DONT USE ->>    min_y = (sy-distance)
### OUTDATED DONT USE ->>    max_y = (sy+distance)
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>    messages = []
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>    y = min_y
### OUTDATED DONT USE ->>    while y < max_y:
### OUTDATED DONT USE ->>        x = min_x
### OUTDATED DONT USE ->>        while x < max_x:
### OUTDATED DONT USE ->>            ax1, ay1 = x, y
### OUTDATED DONT USE ->>            ax2 = min(x + rect_width - 1, max_x - 1)
### OUTDATED DONT USE ->>            ay2 = min(y + rect_height - 1, max_y - 1)
### OUTDATED DONT USE ->>            messages.append(f"%xt%{servers}%gaa%1%{{\"KID\":{kid},\"AX1\":{ax1},\"AY1\":{ay1},\"AX2\":{ax2},\"AY2\":{ay2}}}%")
### OUTDATED DONT USE ->>            x = ax2 + 1
### OUTDATED DONT USE ->>        y = ay2 + 1
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>    return messages
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>def coma_to_list(value):
### OUTDATED DONT USE ->>    return [int(item.strip()) for item in value.split(",") if item.strip()]
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def listening(ws, kid, radius_option, sx, sy, distance):
### OUTDATED DONT USE ->>    targets = []
### OUTDATED DONT USE ->>    while ws.open:
### OUTDATED DONT USE ->>        try:
### OUTDATED DONT USE ->>            response = await asyncio.wait_for(ws.recv(), timeout=3)
### OUTDATED DONT USE ->>            response = response.decode('utf-8')
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            if "%xt%gaa%1%0%" in response:
### OUTDATED DONT USE ->>                response = response.replace('%xt%gaa%1%0%', '').rstrip('%').strip()
### OUTDATED DONT USE ->>                response = json.loads(response)
### OUTDATED DONT USE ->>                objects = response["AI"]
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>                for object in objects:
### OUTDATED DONT USE ->>                    if len(object) == 7:
### OUTDATED DONT USE ->>                        if object[0] == 2 and object[5] < 0 and object[6] == int(kid):
### OUTDATED DONT USE ->>                            tx = object[1]
### OUTDATED DONT USE ->>                            ty = object[2]
### OUTDATED DONT USE ->>                            radius = round(math.sqrt((sx - tx)*(sx - tx) + (sy - ty)*(sy - ty)), 2)
### OUTDATED DONT USE ->>                            target = [tx, ty, radius]
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>                            if target not in targets and (radius <= int(distance) or radius_option == "s"):
### OUTDATED DONT USE ->>                                targets.append(target)
### OUTDATED DONT USE ->>        except asyncio.TimeoutError:
### OUTDATED DONT USE ->>            targets.sort(key=lambda x: x[2])
### OUTDATED DONT USE ->>            return targets
### OUTDATED DONT USE ->>    print("Connection closed or error occurred.")
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def inspecting(ws, leaders):
### OUTDATED DONT USE ->>    try:
### OUTDATED DONT USE ->>        global total_time
### OUTDATED DONT USE ->>        while ws.open:
### OUTDATED DONT USE ->>            response = (await asyncio.wait_for(ws.recv(), timeout=300)).decode('utf-8')
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            if '%xt%cra%1%' in response:
### OUTDATED DONT USE ->>                if '%xt%cra%1%0%' not in response:
### OUTDATED DONT USE ->>                    print("!ERROR! Attack not sent!")
### OUTDATED DONT USE ->>                else:
### OUTDATED DONT USE ->>                    response = response.replace('%xt%cra%1%0%', '').rstrip('%').strip()
### OUTDATED DONT USE ->>                    response = json.loads(response)
### OUTDATED DONT USE ->>                    total_time = response["AAM"]["M"]["TT"]
### OUTDATED DONT USE ->>                    leader_id = response["AAM"]["UM"]["L"]["ID"]
### OUTDATED DONT USE ->>                    now = int(datetime.now().timestamp())
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>                    time_list[leaders.index(leader_id)] = now + total_time
### OUTDATED DONT USE ->>            elif '%xt%cat%1%0%' in response:
### OUTDATED DONT USE ->>                print("We hit the tower!")
### OUTDATED DONT USE ->>                response = response.replace('%xt%cat%1%0%', '').rstrip('%').strip()
### OUTDATED DONT USE ->>                response = json.loads(response)
### OUTDATED DONT USE ->>                total_time = response["A"]["M"]["TT"]
### OUTDATED DONT USE ->>                leader_id = response["A"]["UM"]["L"]["ID"]
### OUTDATED DONT USE ->>                time_list[leaders.index(leader_id)] += total_time
### OUTDATED DONT USE ->>    except websockets.ConnectionClosedError as e:
### OUTDATED DONT USE ->>        print("inspecting: Connection closed.")
### OUTDATED DONT USE ->>        raise e
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def scanning(ws, messages):
### OUTDATED DONT USE ->>    while True:
### OUTDATED DONT USE ->>        for line in messages:
### OUTDATED DONT USE ->>            await ws.send(line)
### OUTDATED DONT USE ->>            await asyncio.sleep(0.04)
### OUTDATED DONT USE ->>        break
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def attacking(ws, sx, sy, leaders, kid, vip_option, targets, max_flank, max_front, unit_id, flank_id, flank_tool_ammount, front_id_1, front_tool_ammount1, front_tool_ammount2, front_id_2, servers):
### OUTDATED DONT USE ->>    global message_queue
### OUTDATED DONT USE ->>    i = 0
### OUTDATED DONT USE ->>    print("Starting to attack.\n")
### OUTDATED DONT USE ->>    if vip_option == "n":
### OUTDATED DONT USE ->>        for line in targets:
### OUTDATED DONT USE ->>            tx = line[0]
### OUTDATED DONT USE ->>            ty = line[1]
### OUTDATED DONT USE ->>            bpc = 0
### OUTDATED DONT USE ->>            lid = leaders[i % len(leaders)]
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            if max_flank == 0:
### OUTDATED DONT USE ->>                flank_unit_id = -1
### OUTDATED DONT USE ->>            else:
### OUTDATED DONT USE ->>                flank_unit_id = unit_id
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            if max_front == 0:
### OUTDATED DONT USE ->>                front_unit_id = -1
### OUTDATED DONT USE ->>            else:
### OUTDATED DONT USE ->>                front_unit_id = unit_id
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            while True:
### OUTDATED DONT USE ->>                now = int(datetime.now().timestamp())
### OUTDATED DONT USE ->>                if now > time_list[i % len(leaders)] + 3:
### OUTDATED DONT USE ->>                    break
### OUTDATED DONT USE ->>                else:
### OUTDATED DONT USE ->>                    await asyncio.sleep(1)
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            # Instead of sending directly, add the message to the queue
### OUTDATED DONT USE ->>            message_queue.append(f"""%xt%{servers}%adi%1%{{"SX":{sx},"SY":{sy},"TX":{tx},"TY":{ty},"KID":{kid}}}%""")
### OUTDATED DONT USE ->>            if i == 0:
### OUTDATED DONT USE ->>                message_queue.append(f"""%xt%{servers}%gas%1%{{}}%""")
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            message_queue.append(f"""%xt%{servers}%cra%1%{{"SX":{sx},"SY":{sy},"TX":{tx},"TY":{ty},"KID":{kid},"LID":{lid},"WT":0,"HBW":-1,"BPC":{bpc},"ATT":0,"AV":0,"LP":0,"FC":0,"PTT":1,"SD":0,"ICA":0,"CD":99,"A":[{{"L":{{"T":[[{flank_id},{flank_tool_ammount}],[-1,0]],"U":[[{flank_unit_id},{max_flank}],[-1,0]]}},"R":{{"T":[[{flank_id},{flank_tool_ammount}],[-1,0]],"U":[[{flank_unit_id},{max_flank}],[-1,0]]}},"M":{{"T":[[{front_id_1},{front_tool_ammount1}],[{front_id_2},{front_tool_ammount2}],[-1,0]],"U":[[{front_unit_id},{max_front}],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]]}}}}],"BKS":[],"AST":[-1,-1,-1],"RW":[[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]],"ASCT":0}}%""")
### OUTDATED DONT USE ->>            if i % 10 == 0:
### OUTDATED DONT USE ->>                print(f"Queued attack number {i+1}")
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            i += 1
### OUTDATED DONT USE ->>        print(f"Queued {i}  attacks.")
### OUTDATED DONT USE ->>    elif vip_option == "y":
### OUTDATED DONT USE ->>        # Similar logic for the VIP option
### OUTDATED DONT USE ->>        for line in targets:
### OUTDATED DONT USE ->>            tx = line[0]
### OUTDATED DONT USE ->>            ty = line[1]
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>            if i < len(leaders):
### OUTDATED DONT USE ->>                bpc = 0
### OUTDATED DONT USE ->>                lid = leaders[i]
### OUTDATED DONT USE ->>            else:
### OUTDATED DONT USE ->>                bpc = 1
### OUTDATED DONT USE ->>                lid = "-14"
### OUTDATED DONT USE ->>            
### OUTDATED DONT USE ->>            message_queue.append(f"""%xt%{servers}%adi%1%{{"SX":{sx},"SY":{sy},"TX":{tx},"TY":{ty},"KID":{kid}}}%""")
### OUTDATED DONT USE ->>            if i == 0:
### OUTDATED DONT USE ->>                message_queue.append(f"""%xt%{servers}%gas%1%{{}}%""")
### OUTDATED DONT USE ->>            
### OUTDATED DONT USE ->>            message_queue.append(f"""%xt%{servers}%cra%1%{{"SX":{sx},"SY":{sy},"TX":{tx},"TY":{ty},"KID":{kid},"LID":{lid},"WT":0,"HBW":-1,"BPC":{bpc},"ATT":0,"AV":0,"LP":0,"FC":0,"PTT":1,"SD":0,"ICA":0,"CD":99,"A":[{{"L":{{"T":[[{flank_id},{flank_tool_ammount}],[-1,0]],"U":[[{flank_unit_id},{max_flank}],[-1,0]]}},"R":{{"T":[[{flank_id},{flank_tool_ammount}],[-1,0]],"U":[[{flank_unit_id},{max_flank}],[-1,0]]}},"M":{{"T":[[{front_id_1},{front_tool_ammount1}],[{front_id_2},{front_tool_ammount2}],[-1,0]],"U":[[{front_unit_id},{max_front}],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]]}}}}],"BKS":[],"AST":[-1,-1,-1],"RW":[[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0],[-1,0]],"ASCT":0}}%""")
### OUTDATED DONT USE ->>            
### OUTDATED DONT USE ->>            print(f"Queued attack number {i+1}")
### OUTDATED DONT USE ->>            i += 1
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def process_queue(ws):
### OUTDATED DONT USE ->>    try:
### OUTDATED DONT USE ->>        if ws.open:
### OUTDATED DONT USE ->>            print("Processing message queue...")
### OUTDATED DONT USE ->>            global message_queue
### OUTDATED DONT USE ->>            while message_queue:
### OUTDATED DONT USE ->>                message = message_queue.pop(0)  # Get the first message in the queue
### OUTDATED DONT USE ->>                await ws.send(message)
### OUTDATED DONT USE ->>                await asyncio.sleep(random.uniform(2.01,2.5))  # Random delay between messages
### OUTDATED DONT USE ->>            if len(message_queue) == 0:
### OUTDATED DONT USE ->>                print("Done.")
### OUTDATED DONT USE ->>                exit()
### OUTDATED DONT USE ->>    except websockets.ConnectionClosedError:
### OUTDATED DONT USE ->>        print("process_queue: Connection closed.")
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def baronbot(ws, sx, sy, info, servers, leaders):
### OUTDATED DONT USE ->>    print("Starting Baron bot...")
### OUTDATED DONT USE ->>    kid = info["kid"]
### OUTDATED DONT USE ->>    distance = info["distance"]
### OUTDATED DONT USE ->>    excluded_commanders = info["excluded_commanders"]
### OUTDATED DONT USE ->>    vip_option = info["vip_option"]
### OUTDATED DONT USE ->>    radius_option = info["radius_option"]
### OUTDATED DONT USE ->>    max_flank = info["max_flank"]
### OUTDATED DONT USE ->>    max_front = info["max_front"]  
### OUTDATED DONT USE ->>    unit_id = info["unit_id"]
### OUTDATED DONT USE ->>    flank_id = info["flank_id"]
### OUTDATED DONT USE ->>    flank_tool_ammount = info["flank_tool_ammount"]
### OUTDATED DONT USE ->>    front_id_1 = info["front_id_1"]
### OUTDATED DONT USE ->>    front_id_2 = info["front_id_2"]
### OUTDATED DONT USE ->>    front_tool_ammount1 = info["front_tool_ammount1"]
### OUTDATED DONT USE ->>    front_tool_ammount2 = info["front_tool_ammount2"]
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>    messages = await generatescans(kid, distance, sx, sy, servers)
### OUTDATED DONT USE ->>    if excluded_commanders != "-1":
### OUTDATED DONT USE ->>        excluded_commanders = coma_to_list(excluded_commanders)
### OUTDATED DONT USE ->>        leaders = [lids for i, lids in enumerate(leaders, start=1) if i not in excluded_commanders]
### OUTDATED DONT USE ->>    global time_list
### OUTDATED DONT USE ->>    for leader in leaders:
### OUTDATED DONT USE ->>        time_list.append(0)
### OUTDATED DONT USE ->>    czas = random.uniform(1,2)
### OUTDATED DONT USE ->>    lister = asyncio.create_task(listening(ws, kid, radius_option, sx, sy, distance))
### OUTDATED DONT USE ->>    await scanning(ws, messages)
### OUTDATED DONT USE ->>    targets = await lister
### OUTDATED DONT USE ->>    print(f"Barons to attack: {len(targets)}")
### OUTDATED DONT USE ->>    czas = random.uniform(3,6)
### OUTDATED DONT USE ->>    await asyncio.sleep(czas)
### OUTDATED DONT USE ->>    inspection = asyncio.create_task(inspecting(ws, leaders))
### OUTDATED DONT USE ->>    await attacking(ws, sx, sy, leaders, kid, vip_option, targets, max_flank, max_front, unit_id, flank_id, flank_tool_ammount, front_id_1, front_tool_ammount1, front_tool_ammount2, front_id_2, servers)
### OUTDATED DONT USE ->>    processattacks = asyncio.create_task(process_queue(ws))
### OUTDATED DONT USE ->>
### OUTDATED DONT USE ->>async def baronbot_restarted(ws):
### OUTDATED DONT USE ->>    if ws.open:
### OUTDATED DONT USE ->>        try:
### OUTDATED DONT USE ->>            print(f"Baron bot resumed, left to attack {len(message_queue) // 2} barons.")
### OUTDATED DONT USE ->>            await process_queue(ws)
### OUTDATED DONT USE ->>        except websockets.ConnectionClosedError as e:
### OUTDATED DONT USE ->>            print("You should never see this, if you do please contact the Authors of the script.")
### OUTDATED DONT USE ->>            raise e