import struct
import json
import pprint

versions = [
    {'name':"N-1.0",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (V1.0).dec','actortable':0xB5E490,'scenetable':0xB71440,'heapStart':0x801DAA00,'console':'N64','game':'VANILLA'},
    {'name':"N-1.1",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (V1.1).dec','actortable':0xB5E650,'scenetable':0xB71600,'heapStart':0x801DABC0,'console':'N64','game':'VANILLA'},
    {'name':"P-1.0",'filename':'Legend of Zelda, The - Ocarina of Time (PAL) (V1.0).dec','actortable':0xB5DDA0,'scenetable':0xB70D60,'heapStart':0x801D8A40,'console':'N64','game':'VANILLA'},
    {'name':"N-1.2",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (V1.2).dec','actortable':0xB5E490,'scenetable':0xB71450,'heapStart':0x801DB2C0,'console':'N64','game':'VANILLA'},
    {'name':"P-1.1",'filename':'Legend of Zelda, The - Ocarina of Time (PAL) (V1.1).dec','actortable':0xB5DDE0,'scenetable':0xB70DA0,'heapStart':0x801D8A80,'console':'N64','game':'VANILLA'},
    {'name':"J-GC-MQDisc",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (GC) [MQ Disc].dec','actortable':0xB5CB60,'scenetable':0xB6FB20,'heapStart':0x801DBBA0,'console':'GC','game':'VANILLA'},
    {'name':"J-MQ",'filename':'Zelda no Densetsu - Toki no Ocarina Ura (J) (GC).dec','actortable':0xB5CB40,'scenetable':0xB6FB00,'heapStart':0x801DBBA0,'console':'GC','game':'MQ'},
    {'name':"U-GC",'filename':'Legend of Zelda, The - Ocarina of Time (U) (GC).dec','actortable':0xB5CB40,'scenetable':0xB6FB00,'heapStart':0x801DBBA0,'console':'GC','game':'VANILLA'},
    {'name':"U-MQ",'filename':'Legend of Zelda, The - Ocarina of Time - Master Quest (U) (GC).dec','actortable':0xB5CB20,'scenetable':0xB6FAE0,'heapStart':0x801DBB60,'console':'GC','game':'MQ'},
    {'name':"P-GC",'filename':'Legend of Zelda, The - Ocarina of Time (PAL) (GC).dec','actortable':0xB5C4A0,'scenetable':0xB6F460,'heapStart':0x801D93A0,'console':'GC','game':'VANILLA'},
    {'name':"P-MQ",'filename':'Legend of Zelda, The - Ocarina of Time - Master Quest (PAL) (GC).dec','actortable':0xB5C480,'scenetable':0xB6F440,'heapStart':0x801D9360,'console':'GC','game':'MQ'},
    {'name':"J-GC-CEDisc",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (GC) [Collector\'s Edition Disc].dec','actortable':0xB5CB40,'scenetable':0xB6FB00,'heapStart':0x801DBBA0,'console':'GC','game':'VANILLA'},
    {'name':"iQue",'filename':'Zelda Chuanshuo Shiguang Zhi Di 00200f70 (zh-CN) (iQue).dec','actortable':0xB87180,'scenetable':0xB9A120,'heapStart':0x801E7F60,'console':'GC','game':'VANILLA'},
    ]

actor_names = ["Player","[Removed]","En_Test","[Removed]","En_GirlA","[Removed]","[Removed]","En_Part","En_Light","En_Door","En_Box","Bg_Dy_Yoseizo","Bg_Hidan_Firewall","En_Poh","En_Okuta","Bg_Ydan_Sp","En_Bom","En_Wallmas","En_Dodongo","En_Firefly","En_Horse","En_Item00","En_Arrow","[Removed]","En_Elf","En_Niw","[Removed]","En_Tite","En_Reeba","En_Peehat","En_Butte","[Removed]","En_Insect","En_Fish","[Removed]","En_Holl","En_Scene_Change","En_Zf","En_Hata","Boss_Dodongo","Boss_Goma","En_Zl1","En_Viewer","En_Goma","Bg_Pushbox","En_Bubble","Door_Shutter","En_Dodojr","En_Bdfire","[Removed]","En_Boom","En_Torch2","En_Bili","En_Tp","[Removed]","En_St","En_Bw","En_A_Obj","En_Eiyer","En_River_Sound","En_Horse_Normal","En_Ossan","Bg_Treemouth","Bg_Dodoago","Bg_Hidan_Dalm","Bg_Hidan_Hrock","En_Horse_Ganon","Bg_Hidan_Rock","Bg_Hidan_Rsekizou","Bg_Hidan_Sekizou","Bg_Hidan_Sima","Bg_Hidan_Syoku","En_Xc","Bg_Hidan_Curtain","Bg_Spot00_Hanebasi","En_Mb","En_Bombf","En_Zl2","Bg_Hidan_Fslift","En_OE2","Bg_Ydan_Hasi","Bg_Ydan_Maruta","Boss_Ganondrof","[Removed]","En_Am","En_Dekubaba","En_M_Fire1","En_M_Thunder","Bg_Ddan_Jd","Bg_Breakwall","En_Jj","En_Horse_Zelda","Bg_Ddan_Kd","Door_Warp1","Obj_Syokudai","Item_B_Heart","En_Dekunuts","Bg_Menkuri_Kaiten","Bg_Menkuri_Eye","En_Vali","Bg_Mizu_Movebg","Bg_Mizu_Water","Arms_Hook","En_fHG","Bg_Mori_Hineri","En_Bb","Bg_Toki_Hikari","En_Yukabyun","Bg_Toki_Swd","En_Fhg_Fire","Bg_Mjin","Bg_Hidan_Kousi","Door_Toki","Bg_Hidan_Hamstep","En_Bird","[Removed]","[Removed]","[Removed]","[Removed]","En_Wood02","[Removed]","[Removed]","[Removed]","[Removed]","En_Lightbox","En_Pu_box","[Removed]","[Removed]","En_Trap","En_Arow_Trap","En_Vase","[Removed]","En_Ta","En_Tk","Bg_Mori_Bigst","Bg_Mori_Elevator","Bg_Mori_Kaitenkabe","Bg_Mori_Rakkatenjo","En_Vm","Demo_Effect","Demo_Kankyo","Bg_Hidan_Fwbig","En_Floormas","En_Heishi1","En_Rd","En_Po_Sisters","Bg_Heavy_Block","Bg_Po_Event","Obj_Mure","En_Sw","Boss_Fd","Object_Kankyo","En_Du","En_Fd","En_Horse_Link_Child","Door_Ana","Bg_Spot02_Objects","Bg_Haka","Magic_Wind","Magic_Fire","[Removed]","En_Ru1","Boss_Fd2","En_Fd_Fire","En_Dh","En_Dha","En_Rl","En_Encount1","Demo_Du","Demo_Im","Demo_Tre_Lgt","En_Fw","Bg_Vb_Sima","En_Vb_Ball","Bg_Haka_Megane","Bg_Haka_MeganeBG","Bg_Haka_Ship","Bg_Haka_Sgami","[Removed]","En_Heishi2","En_Encount2","En_Fire_Rock","En_Brob","Mir_Ray","Bg_Spot09_Obj","Bg_Spot18_Obj","Boss_Va","Bg_Haka_Tubo","Bg_Haka_Trap","Bg_Haka_Huta","Bg_Haka_Zou","Bg_Spot17_Funen","En_Syateki_Itm","En_Syateki_Man","En_Tana","En_Nb","Boss_Mo","En_Sb","En_Bigokuta","En_Karebaba","Bg_Bdan_Objects","Demo_Sa","Demo_Go","En_In","En_Tr","Bg_Spot16_Bombstone","[Removed]","Bg_Hidan_Kowarerukabe","Bg_Bombwall","Bg_Spot08_Iceblock","En_Ru2","Obj_Dekujr","Bg_Mizu_Uzu","Bg_Spot06_Objects","Bg_Ice_Objects","Bg_Haka_Water","[Removed]","En_Ma2","En_Bom_Chu","En_Horse_Game_Check","Boss_Tw","En_Rr","En_Ba","En_Bx","En_Anubice","En_Anubice_Fire","Bg_Mori_Hashigo","Bg_Mori_Hashira4","Bg_Mori_Idomizu","Bg_Spot16_Doughnut","Bg_Bdan_Switch","En_Ma1","Boss_Ganon","Boss_Sst","[Removed]","[Removed]","En_Ny","En_Fr","Item_Shield","Bg_Ice_Shelter","En_Ice_Hono","Item_Ocarina","[Removed]","[Removed]","Magic_Dark","Demo_6K","En_Anubice_Tag","Bg_Haka_Gate","Bg_Spot15_Saku","Bg_Jya_Goroiwa","Bg_Jya_Zurerukabe","[Removed]","Bg_Jya_Cobra","Bg_Jya_Kanaami","Fishing","Obj_Oshihiki","Bg_Gate_Shutter","Eff_Dust","Bg_Spot01_Fusya","Bg_Spot01_Idohashira","Bg_Spot01_Idomizu","Bg_Po_Syokudai","Bg_Ganon_Otyuka","Bg_Spot15_Rrbox","Bg_Umajump","[Removed]","Arrow_Fire","Arrow_Ice","Arrow_Light","[Removed]","[Removed]","Item_Etcetera","Obj_Kibako","Obj_Tsubo","En_Wonder_Item","En_Ik","Demo_Ik","En_Skj","En_Skjneedle","En_G_Switch","Demo_Ext","Demo_Shd","En_Dns","Elf_Msg","En_Honotrap","En_Tubo_Trap","Obj_Ice_Poly","Bg_Spot03_Taki","Bg_Spot07_Taki","En_Fz","En_Po_Relay","Bg_Relay_Objects","En_Diving_Game","En_Kusa","Obj_Bean","Obj_Bombiwa","[Removed]","[Removed]","Obj_Switch","Obj_Elevator","Obj_Lift","Obj_Hsblock","En_Okarina_Tag","En_Yabusame_Mark","En_Goroiwa","En_Ex_Ruppy","En_Toryo","En_Daiku","[Removed]","En_Nwc","En_Blkobj","Item_Inbox","En_Ge1","Obj_Blockstop","En_Sda","En_Clear_Tag","En_Niw_Lady","En_Gm","En_Ms","En_Hs","Bg_Ingate","En_Kanban","En_Heishi3","En_Syateki_Niw","En_Attack_Niw","Bg_Spot01_Idosoko","En_Sa","En_Wonder_Talk","Bg_Gjyo_Bridge","En_Ds","En_Mk","En_Bom_Bowl_Man","En_Bom_Bowl_Pit","En_Owl","En_Ishi","Obj_Hana","Obj_Lightswitch","Obj_Mure2","En_Go","En_Fu","[Removed]","En_Changer","Bg_Jya_Megami","Bg_Jya_Lift","Bg_Jya_Bigmirror","Bg_Jya_Bombchuiwa","Bg_Jya_Amishutter","Bg_Jya_Bombiwa","Bg_Spot18_Basket","[Removed]","En_Ganon_Organ","En_Siofuki","En_Stream","[Removed]","En_Mm","En_Ko","En_Kz","En_Weather_Tag","Bg_Sst_Floor","En_Ani","En_Ex_Item","Bg_Jya_Ironobj","En_Js","En_Jsjutan","En_Cs","En_Md","En_Hy","En_Ganon_Mant","En_Okarina_Effect","En_Mag","Door_Gerudo","Elf_Msg2","Demo_Gt","En_Po_Field","Efc_Erupc","Bg_Zg","En_Heishi4","En_Zl3","Boss_Ganon2","En_Kakasi","En_Takara_Man","Obj_Makeoshihiki","Oceff_Spot","End_Title","[Removed]","En_Torch","Demo_Ec","Shot_Sun","En_Dy_Extra","En_Wonder_Talk2","En_Ge2","Obj_Roomtimer","En_Ssh","En_Sth","Oceff_Wipe","Oceff_Storm","En_Weiyer","Bg_Spot05_Soko","Bg_Jya_1flift","Bg_Jya_Haheniron","Bg_Spot12_Gate","Bg_Spot12_Saku","En_Hintnuts","En_Nutsball","Bg_Spot00_Break","En_Shopnuts","En_It","En_GeldB","Oceff_Wipe2","Oceff_Wipe3","En_Niw_Girl","En_Dog","En_Si","Bg_Spot01_Objects2","Obj_Comb","Bg_Spot11_Bakudankabe","Obj_Kibako2","En_Dnt_Demo","En_Dnt_Jiji","En_Dnt_Nomal","En_Guest","Bg_Bom_Guard","En_Hs2","Demo_Kekkai","Bg_Spot08_Bakudankabe","Bg_Spot17_Bakudankabe","[Removed]","Obj_Mure3","En_Tg","En_Mu","En_Go2","En_Wf","En_Skb","Demo_Gj","Demo_Geff","Bg_Gnd_Firemeiro","Bg_Gnd_Darkmeiro","Bg_Gnd_Soulmeiro","Bg_Gnd_Nisekabe","Bg_Gnd_Iceblock","En_Gb","En_Gs","Bg_Mizu_Bwall","Bg_Mizu_Shutter","En_Daiku_Kakariko","Bg_Bowl_Wall","En_Wall_Tubo","En_Po_Desert","En_Crow","Door_Killer","Bg_Spot11_Oasis","Bg_Spot18_Futa","Bg_Spot18_Shutter","En_Ma3","En_Cow","Bg_Ice_Turara","Bg_Ice_Shutter","En_Kakasi2","En_Kakasi3","Oceff_Wipe4","En_Eg","Bg_Menkuri_Nisekabe","En_Zo","Obj_Makekinsuta","En_Ge3","Obj_Timeblock","Obj_Hamishi","En_Zl4","En_Mm2","Bg_Jya_Block","Obj_Warp2block"]

versionDict = {}
for v in versions:
    versionDict[v['name']] = v
f2 = open('versions.json','w')
json.dump(versionDict,f2,indent='\t')
f2.close()

###########################################

actor_count = 0x1D7

hardcoded_instance_sizes = {
    0x0: 0xA90, # Player
    0x15: 0x1A0, # En_Item00
    0x39: 0x1C0 # En_A_Obj
}

actors = [{} for _ in range(actor_count)]

for v in versions:
    print(v['name'])
    f=open('roms/'+v['filename'],'rb')
    rom = f.read()

    for actorId in range(actor_count):
        romStart, romEnd, ramStart, ramEnd, _, ramInitVars, _, allocType, _, _ = struct.unpack('>IIIIIIIhbb',rom[v['actortable']+0x20*actorId:v['actortable']+0x20*(actorId+1)])
        overlaySize = ramEnd-ramStart
        romInitVars = romStart+ramInitVars-ramStart
        if 0 < romInitVars < 0x80000000:
            _,_,_,instanceSize = struct.unpack('>IIII',rom[romInitVars:romInitVars+0x10])
        elif ramInitVars > 0:
            instanceSize = hardcoded_instance_sizes[actorId]
        else:
            instanceSize = None
        actorInfo = {'actorId':actorId,'overlaySize':overlaySize, 'instanceSize':instanceSize, 'allocType':allocType, 'name':actor_names[actorId]}
        actors[actorId][v['name']] = actorInfo

for i in range(actor_count):
    if (actors[i]["N-1.0"]==actors[i]["N-1.1"]==actors[i]["P-1.0"]==actors[i]["N-1.2"]==actors[i]["P-1.1"]==
        actors[i]["J-GC-MQDisc"]==actors[i]["J-MQ"]==actors[i]["U-GC"]==actors[i]["U-MQ"]==actors[i]["P-GC"]==actors[i]["P-MQ"]==actors[i]["J-GC-CEDisc"]):
        actors[i] = {'ALL':actors[i]["N-1.0"]}
    elif (actors[i]["N-1.0"]==actors[i]["N-1.1"]==actors[i]["P-1.0"]==actors[i]["N-1.2"]==actors[i]["P-1.1"]) and (
        actors[i]["J-GC-MQDisc"]==actors[i]["J-MQ"]==actors[i]["U-GC"]==actors[i]["U-MQ"]==actors[i]["P-GC"]==actors[i]["P-MQ"]==actors[i]["J-GC-CEDisc"]):
        actors[i] = {'N64':actors[i]["N-1.0"],'GC':actors[i]["J-GC-MQDisc"]}
    else:
        pass

f2 = open('actors.json','w')
json.dump(actors,f2,indent='\t')
f2.close()

#########################################################

scene_count = 0x65

scenes = [{} for _ in range(scene_count)]

for v in versions:
    print(v['name'])
    f=open('roms/'+v['filename'],'rb')
    rom = f.read()

    for sceneId in range(scene_count):

        scenes[sceneId][v['name']] = [None,None,None,None]

        sceneRomStart, sceneRomEnd, _, _, _ = struct.unpack('>IIIII',rom[v['scenetable']+0x14*sceneId:v['scenetable']+0x14*(sceneId+1)])

        sceneAltHeaders = None
        roomAltHeaders = {}

        for setupId in range(4):

            if setupId == 0:
                scenes[sceneId][v['name']][setupId] = {'rooms':[],'transitionActors':[]}
                sceneHeaderStart = sceneRomStart
            else:
                if sceneAltHeaders and sceneAltHeaders[setupId-1]:
                    scenes[sceneId][v['name']][setupId] = {'rooms':[],'transitionActors':[]}
                    sceneHeaderStart = sceneRomStart + (sceneAltHeaders[setupId-1]&0x00FFFFFF)
                else:
                    scenes[sceneId][v['name']][setupId] = None
                    continue
            
            sceneHeaderCommand = None
            sceneHeaderNum = 0
            while sceneHeaderCommand != 0x14:
                sceneHeaderCommand, sceneParam1, _, sceneParam2 = struct.unpack('>BBHI',rom[sceneHeaderStart+8*sceneHeaderNum:sceneHeaderStart+8*(sceneHeaderNum+1)])

                if sceneHeaderCommand == 0x18: # Alternate Headers
                    sceneSetupListStart = sceneRomStart + (sceneParam2&0x00FFFFFF)
                    sceneAltHeaders = struct.unpack('>III', rom[sceneSetupListStart:sceneSetupListStart+0xC]) # we only care about setups 0-3
                elif sceneHeaderCommand == 0x04: # Rooms
                    for roomId in range(sceneParam1):
                        roomListStart = sceneRomStart + (sceneParam2&0x00FFFFFF)
                        roomRomStart, roomRomEnd = struct.unpack('>II',rom[roomListStart+8*roomId:roomListStart+8*(roomId+1)])

                        roomData = {'actors':[]}

                        if setupId == 0:
                            roomHeaderStart = roomRomStart
                        else:
                            assert(roomAltHeaders[roomId][setupId-1])
                            roomHeaderStart = roomRomStart + (roomAltHeaders[roomId][setupId-1]&0x00FFFFFF)
                        
                        roomHeaderCommand = None
                        roomHeaderNum = 0
                        while roomHeaderCommand != 0x14:
                            roomHeaderCommand, roomParam1, _, roomParam2 = struct.unpack('>BBHI',rom[roomHeaderStart+8*roomHeaderNum:roomHeaderStart+8*(roomHeaderNum+1)])

                            if roomHeaderCommand == 0x18: # Alternate Headers
                                roomSetupListStart = roomRomStart + (roomParam2&0x00FFFFFF)
                                roomAltHeaders[roomId] = struct.unpack('>III', rom[roomSetupListStart:roomSetupListStart+0xC]) # we only care about setups 0-3
                            elif roomHeaderCommand == 0x01: #Actor List
                                for actorNum in range(roomParam1):
                                    actorListStart = roomRomStart + (roomParam2&0x00FFFFFF)
                                    actorId, _, _, _, _, _, _, actorParams = struct.unpack('>HHHHHHHH',rom[actorListStart+0x10*actorNum:actorListStart+0x10*(actorNum+1)])
                                    roomData['actors'].append({'actorId':actorId,'actorParams':actorParams})
                            roomHeaderNum += 1
                            
                        scenes[sceneId][v['name']][setupId]['rooms'].append(roomData)
            
                elif sceneHeaderCommand == 0x0E: # Transition Actors
                    for transitionActorNum in range(sceneParam1):
                        transitionActorListStart = sceneRomStart + (sceneParam2&0x00FFFFFF)
                        frontRoom, _, backRoom, _, actorId, _, _, _, _, actorParams = struct.unpack('>BBBBHHHHHH',rom[transitionActorListStart+0x10*transitionActorNum:transitionActorListStart+0x10*(transitionActorNum+1)])
                        scenes[sceneId][v['name']][setupId]['transitionActors'].append({'frontRoom':frontRoom,'backRoom':backRoom,'actorId':actorId,'actorParams':actorParams})
                
                sceneHeaderNum += 1
                
            if sceneAltHeaders:
                assert len(roomAltHeaders) == len(scenes[sceneId][v['name']][setupId]['rooms'])
            else:
                assert len(roomAltHeaders) == 0
            
for i in range(scene_count):
    if (scenes[i]["N-1.0"]==scenes[i]["N-1.1"]==scenes[i]["P-1.0"]==scenes[i]["N-1.2"]==scenes[i]["P-1.1"]==scenes[i]["J-GC-MQDisc"]==scenes[i]["U-GC"]==scenes[i]["P-GC"]==scenes[i]["J-GC-CEDisc"]
        ==scenes[i]["J-MQ"]==scenes[i]["U-MQ"]==scenes[i]["P-MQ"]):
        scenes[i] = {'ALL':scenes[i]["N-1.0"]}
    elif (scenes[i]["N-1.0"]==scenes[i]["N-1.1"]==scenes[i]["P-1.0"]==scenes[i]["N-1.2"]==scenes[i]["P-1.1"]==scenes[i]["J-GC-MQDisc"]==scenes[i]["U-GC"]==scenes[i]["P-GC"]==scenes[i]["J-GC-CEDisc"]
          ) and (scenes[i]["J-MQ"]==scenes[i]["U-MQ"]==scenes[i]["P-MQ"]):
        scenes[i] = {'VANILLA':scenes[i]["N-1.0"],'MQ':scenes[i]["J-MQ"]}
    else:
        pass

f2 = open('scenes.json','w')
json.dump(scenes,f2,indent='\t')
f2.close()
