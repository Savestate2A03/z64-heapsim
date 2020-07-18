import struct
import json
import pprint

versions = [
    {'name':"OoT-N-1.0",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (V1.0).dec','actortable':0xB5E490,'scenetable':0xB71440,'heapStart':0x801DAA00,'console':'N64','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-N-1.1",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (V1.1).dec','actortable':0xB5E650,'scenetable':0xB71600,'heapStart':0x801DABC0,'console':'N64','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-P-1.0",'filename':'Legend of Zelda, The - Ocarina of Time (PAL) (V1.0).dec','actortable':0xB5DDA0,'scenetable':0xB70D60,'heapStart':0x801D8A40,'console':'N64','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-N-1.2",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (V1.2).dec','actortable':0xB5E490,'scenetable':0xB71450,'heapStart':0x801DB2C0,'console':'N64','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-P-1.1",'filename':'Legend of Zelda, The - Ocarina of Time (PAL) (V1.1).dec','actortable':0xB5DDE0,'scenetable':0xB70DA0,'heapStart':0x801D8A80,'console':'N64','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-J-GC-MQDisc",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (GC) [MQ Disc].dec','actortable':0xB5CB60,'scenetable':0xB6FB20,'heapStart':0x801DBBA0,'console':'GC','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-J-MQ",'filename':'Zelda no Densetsu - Toki no Ocarina Ura (J) (GC).dec','actortable':0xB5CB40,'scenetable':0xB6FB00,'heapStart':0x801DBBA0,'console':'GC','game':'OoT', 'variation':'MQ'},
    {'name':"OoT-U-GC",'filename':'Legend of Zelda, The - Ocarina of Time (U) (GC).dec','actortable':0xB5CB40,'scenetable':0xB6FB00,'heapStart':0x801DBBA0,'console':'GC','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-U-MQ",'filename':'Legend of Zelda, The - Ocarina of Time - Master Quest (U) (GC).dec','actortable':0xB5CB20,'scenetable':0xB6FAE0,'heapStart':0x801DBB60,'console':'GC','game':'OoT', 'variation':'MQ'},
    {'name':"OoT-P-GC",'filename':'Legend of Zelda, The - Ocarina of Time (PAL) (GC).dec','actortable':0xB5C4A0,'scenetable':0xB6F460,'heapStart':0x801D93A0,'console':'GC','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-P-MQ",'filename':'Legend of Zelda, The - Ocarina of Time - Master Quest (PAL) (GC).dec','actortable':0xB5C480,'scenetable':0xB6F440,'heapStart':0x801D9360,'console':'GC','game':'OoT', 'variation':'MQ'},
    {'name':"OoT-J-GC-CEDisc",'filename':'Zelda no Densetsu - Toki no Ocarina (J) (GC) [Collector\'s Edition Disc].dec','actortable':0xB5CB40,'scenetable':0xB6FB00,'heapStart':0x801DBBA0,'console':'GC','game':'OoT', 'variation':'VANILLA'},
    {'name':"OoT-iQue",'filename':'Zelda Chuanshuo Shiguang Zhi Di 00200f70 (zh-CN) (iQue).dec','actortable':0xB87180,'scenetable':0xB9A120,'heapStart':0x801E7F60,'console':'GC','game':'OoT', 'variation':'VANILLA'},
    {'name':"MM-U",'filename':'Legend of Zelda, The - Majora\'s Mask (USA).dec','actortable':0xC45510,'scenetable':0xC5A1E0,'heapStart':0x803FFDA0,'console':'N64','game':'MM', 'variation': None},
    ]

actor_names = {
    "OoT": ["Player","[Removed]","En_Test","[Removed]","En_GirlA","[Removed]","[Removed]","En_Part","En_Light","En_Door","En_Box","Bg_Dy_Yoseizo","Bg_Hidan_Firewall","En_Poh","En_Okuta","Bg_Ydan_Sp","En_Bom","En_Wallmas","En_Dodongo","En_Firefly","En_Horse","En_Item00","En_Arrow","[Removed]","En_Elf","En_Niw","[Removed]","En_Tite","En_Reeba","En_Peehat","En_Butte","[Removed]","En_Insect","En_Fish","[Removed]","En_Holl","En_Scene_Change","En_Zf","En_Hata","Boss_Dodongo","Boss_Goma","En_Zl1","En_Viewer","En_Goma","Bg_Pushbox","En_Bubble","Door_Shutter","En_Dodojr","En_Bdfire","[Removed]","En_Boom","En_Torch2","En_Bili","En_Tp","[Removed]","En_St","En_Bw","En_A_Obj","En_Eiyer","En_River_Sound","En_Horse_Normal","En_Ossan","Bg_Treemouth","Bg_Dodoago","Bg_Hidan_Dalm","Bg_Hidan_Hrock","En_Horse_Ganon","Bg_Hidan_Rock","Bg_Hidan_Rsekizou","Bg_Hidan_Sekizou","Bg_Hidan_Sima","Bg_Hidan_Syoku","En_Xc","Bg_Hidan_Curtain","Bg_Spot00_Hanebasi","En_Mb","En_Bombf","En_Zl2","Bg_Hidan_Fslift","En_OE2","Bg_Ydan_Hasi","Bg_Ydan_Maruta","Boss_Ganondrof","[Removed]","En_Am","En_Dekubaba","En_M_Fire1","En_M_Thunder","Bg_Ddan_Jd","Bg_Breakwall","En_Jj","En_Horse_Zelda","Bg_Ddan_Kd","Door_Warp1","Obj_Syokudai","Item_B_Heart","En_Dekunuts","Bg_Menkuri_Kaiten","Bg_Menkuri_Eye","En_Vali","Bg_Mizu_Movebg","Bg_Mizu_Water","Arms_Hook","En_fHG","Bg_Mori_Hineri","En_Bb","Bg_Toki_Hikari","En_Yukabyun","Bg_Toki_Swd","En_Fhg_Fire","Bg_Mjin","Bg_Hidan_Kousi","Door_Toki","Bg_Hidan_Hamstep","En_Bird","[Removed]","[Removed]","[Removed]","[Removed]","En_Wood02","[Removed]","[Removed]","[Removed]","[Removed]","En_Lightbox","En_Pu_box","[Removed]","[Removed]","En_Trap","En_Arow_Trap","En_Vase","[Removed]","En_Ta","En_Tk","Bg_Mori_Bigst","Bg_Mori_Elevator","Bg_Mori_Kaitenkabe","Bg_Mori_Rakkatenjo","En_Vm","Demo_Effect","Demo_Kankyo","Bg_Hidan_Fwbig","En_Floormas","En_Heishi1","En_Rd","En_Po_Sisters","Bg_Heavy_Block","Bg_Po_Event","Obj_Mure","En_Sw","Boss_Fd","Object_Kankyo","En_Du","En_Fd","En_Horse_Link_Child","Door_Ana","Bg_Spot02_Objects","Bg_Haka","Magic_Wind","Magic_Fire","[Removed]","En_Ru1","Boss_Fd2","En_Fd_Fire","En_Dh","En_Dha","En_Rl","En_Encount1","Demo_Du","Demo_Im","Demo_Tre_Lgt","En_Fw","Bg_Vb_Sima","En_Vb_Ball","Bg_Haka_Megane","Bg_Haka_MeganeBG","Bg_Haka_Ship","Bg_Haka_Sgami","[Removed]","En_Heishi2","En_Encount2","En_Fire_Rock","En_Brob","Mir_Ray","Bg_Spot09_Obj","Bg_Spot18_Obj","Boss_Va","Bg_Haka_Tubo","Bg_Haka_Trap","Bg_Haka_Huta","Bg_Haka_Zou","Bg_Spot17_Funen","En_Syateki_Itm","En_Syateki_Man","En_Tana","En_Nb","Boss_Mo","En_Sb","En_Bigokuta","En_Karebaba","Bg_Bdan_Objects","Demo_Sa","Demo_Go","En_In","En_Tr","Bg_Spot16_Bombstone","[Removed]","Bg_Hidan_Kowarerukabe","Bg_Bombwall","Bg_Spot08_Iceblock","En_Ru2","Obj_Dekujr","Bg_Mizu_Uzu","Bg_Spot06_Objects","Bg_Ice_Objects","Bg_Haka_Water","[Removed]","En_Ma2","En_Bom_Chu","En_Horse_Game_Check","Boss_Tw","En_Rr","En_Ba","En_Bx","En_Anubice","En_Anubice_Fire","Bg_Mori_Hashigo","Bg_Mori_Hashira4","Bg_Mori_Idomizu","Bg_Spot16_Doughnut","Bg_Bdan_Switch","En_Ma1","Boss_Ganon","Boss_Sst","[Removed]","[Removed]","En_Ny","En_Fr","Item_Shield","Bg_Ice_Shelter","En_Ice_Hono","Item_Ocarina","[Removed]","[Removed]","Magic_Dark","Demo_6K","En_Anubice_Tag","Bg_Haka_Gate","Bg_Spot15_Saku","Bg_Jya_Goroiwa","Bg_Jya_Zurerukabe","[Removed]","Bg_Jya_Cobra","Bg_Jya_Kanaami","Fishing","Obj_Oshihiki","Bg_Gate_Shutter","Eff_Dust","Bg_Spot01_Fusya","Bg_Spot01_Idohashira","Bg_Spot01_Idomizu","Bg_Po_Syokudai","Bg_Ganon_Otyuka","Bg_Spot15_Rrbox","Bg_Umajump","[Removed]","Arrow_Fire","Arrow_Ice","Arrow_Light","[Removed]","[Removed]","Item_Etcetera","Obj_Kibako","Obj_Tsubo","En_Wonder_Item","En_Ik","Demo_Ik","En_Skj","En_Skjneedle","En_G_Switch","Demo_Ext","Demo_Shd","En_Dns","Elf_Msg","En_Honotrap","En_Tubo_Trap","Obj_Ice_Poly","Bg_Spot03_Taki","Bg_Spot07_Taki","En_Fz","En_Po_Relay","Bg_Relay_Objects","En_Diving_Game","En_Kusa","Obj_Bean","Obj_Bombiwa","[Removed]","[Removed]","Obj_Switch","Obj_Elevator","Obj_Lift","Obj_Hsblock","En_Okarina_Tag","En_Yabusame_Mark","En_Goroiwa","En_Ex_Ruppy","En_Toryo","En_Daiku","[Removed]","En_Nwc","En_Blkobj","Item_Inbox","En_Ge1","Obj_Blockstop","En_Sda","En_Clear_Tag","En_Niw_Lady","En_Gm","En_Ms","En_Hs","Bg_Ingate","En_Kanban","En_Heishi3","En_Syateki_Niw","En_Attack_Niw","Bg_Spot01_Idosoko","En_Sa","En_Wonder_Talk","Bg_Gjyo_Bridge","En_Ds","En_Mk","En_Bom_Bowl_Man","En_Bom_Bowl_Pit","En_Owl","En_Ishi","Obj_Hana","Obj_Lightswitch","Obj_Mure2","En_Go","En_Fu","[Removed]","En_Changer","Bg_Jya_Megami","Bg_Jya_Lift","Bg_Jya_Bigmirror","Bg_Jya_Bombchuiwa","Bg_Jya_Amishutter","Bg_Jya_Bombiwa","Bg_Spot18_Basket","[Removed]","En_Ganon_Organ","En_Siofuki","En_Stream","[Removed]","En_Mm","En_Ko","En_Kz","En_Weather_Tag","Bg_Sst_Floor","En_Ani","En_Ex_Item","Bg_Jya_Ironobj","En_Js","En_Jsjutan","En_Cs","En_Md","En_Hy","En_Ganon_Mant","En_Okarina_Effect","En_Mag","Door_Gerudo","Elf_Msg2","Demo_Gt","En_Po_Field","Efc_Erupc","Bg_Zg","En_Heishi4","En_Zl3","Boss_Ganon2","En_Kakasi","En_Takara_Man","Obj_Makeoshihiki","Oceff_Spot","End_Title","[Removed]","En_Torch","Demo_Ec","Shot_Sun","En_Dy_Extra","En_Wonder_Talk2","En_Ge2","Obj_Roomtimer","En_Ssh","En_Sth","Oceff_Wipe","Oceff_Storm","En_Weiyer","Bg_Spot05_Soko","Bg_Jya_1flift","Bg_Jya_Haheniron","Bg_Spot12_Gate","Bg_Spot12_Saku","En_Hintnuts","En_Nutsball","Bg_Spot00_Break","En_Shopnuts","En_It","En_GeldB","Oceff_Wipe2","Oceff_Wipe3","En_Niw_Girl","En_Dog","En_Si","Bg_Spot01_Objects2","Obj_Comb","Bg_Spot11_Bakudankabe","Obj_Kibako2","En_Dnt_Demo","En_Dnt_Jiji","En_Dnt_Nomal","En_Guest","Bg_Bom_Guard","En_Hs2","Demo_Kekkai","Bg_Spot08_Bakudankabe","Bg_Spot17_Bakudankabe","[Removed]","Obj_Mure3","En_Tg","En_Mu","En_Go2","En_Wf","En_Skb","Demo_Gj","Demo_Geff","Bg_Gnd_Firemeiro","Bg_Gnd_Darkmeiro","Bg_Gnd_Soulmeiro","Bg_Gnd_Nisekabe","Bg_Gnd_Iceblock","En_Gb","En_Gs","Bg_Mizu_Bwall","Bg_Mizu_Shutter","En_Daiku_Kakariko","Bg_Bowl_Wall","En_Wall_Tubo","En_Po_Desert","En_Crow","Door_Killer","Bg_Spot11_Oasis","Bg_Spot18_Futa","Bg_Spot18_Shutter","En_Ma3","En_Cow","Bg_Ice_Turara","Bg_Ice_Shutter","En_Kakasi2","En_Kakasi3","Oceff_Wipe4","En_Eg","Bg_Menkuri_Nisekabe","En_Zo","Obj_Makekinsuta","En_Ge3","Obj_Timeblock","Obj_Hamishi","En_Zl4","En_Mm2","Bg_Jya_Block","Obj_Warp2block"],
    "MM": ["unset / Player","En_Test / ?","En_GirlA / ?","En_Part / ?","En_Light / Deku Shrine - Flames of Varying Colours","En_Door / Wooden Door","En_Box / Treasure Chest","En_Pametfrog / Gekko & Snapper Miniboss - Gekko","En_Okuta / Octorok","En_Bom / Bomb","En_Wallmas / Wallmaster","En_Dodongo / Dodongo","En_Firefly / Keese","En_Horse / ?","En_Item00 / Collectable Items","En_Arrow / Small Orange Flame That Fades Away","En_Elf / Tatl","En_Niw / Cucco","En_Tite / Tektite","unset / ?","En_Peehat / Peahat","En_Butte / ?","En_Insect / Bug","En_Fish / Fish","En_Holl / Black Room Transition Plane","En_Dinofos / Dinolfos","En_Hata / Red Flag on Post","En_Zl1 / Child Zelda","En_Viewer / ?","En_Bubble / Shabom","Door_Shutter / Studded Lifting Door","unset / ?","En_Boom / Zora Fin Returning","En_Torch2 / ?","En_Minifrog / Frog","unset / ?","En_St / Skulltula","unset / ?","En_A_Obj / ?","Obj_Wturn / ?","En_River_Sound / ?","unset / ?","En_Ossan / ?","unset / ?","unset / ?","En_Famos / Death Armos","unset / ?","En_Bombf / Bombflower","unset / ?","unset / ?","En_Am / Armos","En_Dekubaba / Deku Baba","En_M_Fire1 / ?","En_M_Thunder / ?","Bg_Breakwall / ?","unset / ?","Door_Warp1 / Blue Warp","Obj_Syokudai / Golden Torch Stand","Item_B_Heart / Heart Container","En_Dekunuts / Mad Scrub","En_Bbfall / Red Bubble","Arms_Hook / Hookshot","En_Bb / Blue Bubble","Bg_Keikoku_Spr / Fountain","unset / ?","En_Wood02 / Termina Field Tree","unset / ?","En_Death / Gomess","En_Minideath / Bats Surrounding Gomess?","unset / ?","unset / ?","En_Vm / Beamos","Demo_Effect / ?","Demo_Kankyo / ?","En_Floormas / Floormaster","unset / ?","En_Rd / Gibdo","Bg_F40_Flift / Stone Tower Temple - Grey Square Stone Elevator"," / Golden Gauntlets Rock (JP 1.0 Only)","Obj_Mure / ?","En_Sw / Skullwalltula","Object_Kankyo / ?","unset / ?","unset / ?","En_Horse_Link_Child / Child Epona","Door_Ana / Hole in Ground Exit","unset / ?","unset / ?","unset / ?","unset / ?","unset / ?","En_Encount1 / ?","Demo_Tre_Lgt / Light Radiating From Treasure Chest","unset / ?","unset / ?","En_Encount2 / Astral Observatory - Majora's Mask Balloon","En_Fire_Rock / Rock With Beam of Light","Bg_Ctower_Rot / Twisting Path to Clocktower","Mir_Ray / Mirror Shield Face & Light Ray","unset / ?","En_Sb / Shellblade","En_Bigslime / Mad Jelly","En_Karebaba / Wilted Deku Baba","En_In / Gorman Bros.","unset / ?","En_Ru / Ruto","En_Bom_Chu / Bombchu","En_Horse_Game_Check / Arrow, Posts, & Splatter","En_Rr / Like Like","unset / ?","unset / ?","unset / ?","unset / ?","unset / ?","unset / ?","En_Fr / ?","unset / ?","unset / ?","unset / ?","unset / ?","unset / ?"," / Fishing Pond Owner (JP 1.0 Only)","Obj_Oshihiki / Pushable Block","Eff_Dust / ?","Bg_Umajump / ?","Arrow_Fire / Fire Arrow","Arrow_Ice / Ice Arrow","Arrow_Light / Light Arrow","Item_Etcetera / ?","Obj_Kibako / Small Wooden Crate","Obj_Tsubo / Pot","unset / ?","En_Ik / Iron Knuckle","unset / ?","unset / ?","unset / ?","unset / ?","Demo_Shd / ?","En_Dns / Deku Palace - King's Chamber Deku Guard","Elf_Msg / ?","En_Honotrap / ?","En_Tubo_Trap / ?","Obj_Ice_Poly / ?","En_Fz / Freezard","En_Kusa / ?","Obj_Bean / Floating Bean Plant","Obj_Bombiwa / Bombable Rock","Obj_Switch / ?","unset / ?","Obj_Lift / Dampe's Grave - Brown Elevator","Obj_Hsblock / Stone Hookshot Target Pillar","En_Okarina_Tag / ?","unset / ?","En_Goroiwa / Grey Boulder That Rolls Around","unset / ?","unset / ?","En_Daiku / Carpenter","En_Nwc / Cucco Chick","Item_Inbox / ?","En_Ge1 / Gerudo Lieutenant","Obj_Blockstop / ?","En_Sda / ?","En_Clear_Tag / Dissipating Cloud of Black Smoke Following Explosion","unset / ?","En_Gm / Gorman","En_Ms / Bean Seller","En_Hs / Grog","Bg_Ingate / Swamp - Tour Boat","En_Kanban / Square Signpost","unset / ?","En_Attack_Niw / Attacking Cucco","unset / ?","unset / ?","unset / ?","En_Mk / Marine Researcher","En_Owl / Kaepora Gaebora","En_Ishi / ?","Obj_Hana / Flower With Glitched Textures","Obj_Lightswitch / Sun Switch","Obj_Mure2 / ?","unset / ?","En_Fu / Honey & Darling","unset / ?","unset / ?","En_Stream / Water Spout","En_Mm / ?","unset / ?","unset / ?","En_Weather_Tag / ?","En_Ani / Part-Timer","unset / ?","En_Js / Moon Child","unset / ?","unset / ?","unset / ?","unset / ?","En_Okarina_Effect / ?","En_Mag / Title Logo","Elf_Msg2 / ?","Bg_F40_Swlift / Stone Tower Temple - Floating Stone Platform","unset / ?","unset / ?","En_Kakasi / Scarecrow","Obj_Makeoshihiki / ?","Oceff_Spot / ?","unset / ?","En_Torch / ?","unset / ?","Shot_Sun / ?","unset / ?","unset / ?","Obj_Roomtimer / ?","En_Ssh / Cursed Man","unset / ?","Oceff_Wipe / ?","Oceff_Storm / ?","Obj_Demo / ?","En_Minislime / Mad Jelly - Jelly Droplets?","En_Nutsball / Deku Nut Projectile","unset / ?","unset / ?","unset / ?","unset / ?","Oceff_Wipe2 / ?","Oceff_Wipe3 / ?","unset / ?","En_Dg / Dog","En_Si / Gold Skulltula Token","Obj_Comb / Honeycomb","Obj_Kibako2 / Normal Wooden Crate","unset / ?","En_Hs2 / Blue Target Spot","Obj_Mure3 / ?","En_Tg / Honey & Darling","unset / ?","unset / ?","En_Wf / Wolfos","En_Skb / Stalchild","unset / ?","En_Gs / Gossip Stone","Obj_Sound / Termina Field - Fountain Sound Effects","En_Crow / Guay","unset / ?","En_Cow / Cow","unset / ?","unset / ?","Oceff_Wipe4 / ?","unset / ?","En_Zo / Zora","Obj_Makekinsuta / ?","En_Ge3 / Aveil","unset / ?","Obj_Hamishi / ?","En_Zl4 / Skullkid With Flute, OoT, Link Mask, Majora's Mask","En_Mm2 / Postman's Letter to Himself","unset / ?","Door_Spiral / ?","unset / ?","Obj_Pzlblock / ?","Obj_Toge / Blade Trap","unset / ?","Obj_Armos / Armos Statue","Obj_Boyo / Green Bumper","unset / ?","unset / ?","En_Grasshopper / Dragonfly","unset / ?","Obj_Grass / ?","Obj_Grass_Carry / ?","Obj_Grass_Unit / ?","unset / ?","unset / ?","Bg_Fire_Wall / Proximity-Activated Firewall","En_Bu / ?","En_Encount3 / Circle of Light","En_Jso / Garo Master","Obj_Chikuwa / Row of Blocks That Collapse on Approach","En_Knight / Igos du Ikana","En_Warp_tag / ?","En_Aob_01 / Mamamu Yan","En_Boj_01 / ?","En_Boj_02 / ?","En_Boj_03 / ?","En_Encount4 / ?","En_Bom_Bowl_Man / Bomber","En_Syateki_Man / Swamp Shooting Gallery Manager","unset / ?","Bg_Icicle / Blue Icicle","En_Syateki_Crow / Shooting Gallery - Guay","En_Boj_04 / ?","En_Cne_01 / ?","En_Bba_01 / ?","En_Bji_01 / Shikashi","Bg_Spdweb / Spiderweb","unset / ?","unset / ?","En_Mt_tag / ?","Boss_01 / Odolwa","Boss_02 / Twinmold","Boss_03 / Gyorg","Boss_04 / Wart","Boss_05 / Bio Deku Baba","Boss_06 / ?","Boss_07 / Majora","Bg_Dy_Yoseizo / Great Fairy","unset / ?","En_Boj_05 / ?","unset / ?","unset / ?","En_Sob1 / ?","unset / ?","unset / ?","En_Go / Goron","unset / ?","En_Raf / Carnivorous Lilypad","Obj_Funen / Plume of Smoke Rising High Into the Sky","Obj_Raillift / Various Elevators (1, 2, 3, 4, 5)","Bg_Numa_Hana / Woodfall Temple - Wooden Flower","Obj_Flowerpot / Breakable Pot With Grass","Obj_Spinyroll / Spike-Covered Log","Dm_Hina / Cutscene - Boss Remains","En_Syateki_Wf / Shooting Gallery - Wolfos","Obj_Skateblock / ?","Obj_Iceblock / Ice Block That Appears After Freezing Enemy","En_Bigpamet / Gekko & Snapper Miniboss - Snapper","En_Syateki_Dekunuts / Shooting Gallery - Deku Scrub","Elf_Msg3 / ?","En_Fg / Frog","Dm_Ravine / Link Riding Through Lost Woods Cutscene - Tree Trunk","Dm_Sa / Skullkid With Flute, OoT, Link Mask, Majora's Mask","En_Slime / Chuchu","En_Pr / Desbreko","Obj_Toudai / Clock Tower Spotlight","Obj_Entotu / Chimney Expelling Smoke","Obj_Bell / Stock Pot Inn Bell","En_Syateki_Okuta / Shooting Gallery - Octorok","unset / ?","Obj_Shutter / ?","Dm_Zl / Song of Time Cutscene - Child Zelda","En_Elfgrp / ?","Dm_Tsg / Tatl Left Behind Cutscene - Deku Door/Spotlights","En_Baguo / Nejiron","Obj_Vspinyroll / Vertically-Oriented Rotating Spiked Log","Obj_Smork / Romani Ranch - Chimney Smoke Plume","En_Test2 / ?","En_Test3 / Kafei","En_Test4 / Three-Day Timer","En_Bat / Bad Bat","En_Sekihi / ?","En_Wiz / Wizzrobe","En_Wiz_Brock / Wizzrobe - Warp Platform","En_Wiz_Fire / Wizzrobe - Fire Attack","Eff_Change / Camera Focuses on Link","Dm_Statue / Elegy of Emptiness - Beam of Light When Creating Statue","Obj_Fireshield / Switch-Deactivated Circle of Flames Surrounding Platforms","Bg_Ladder / Ladder","En_Mkk / Black Boe","Demo_Getitem / ?","unset / ?","En_Dnb / Deku Nut Projectile","En_Dnh / Blue Target Spot Saying Koume's Boat Cruise Is Closed","En_Dnk / ?","En_Dnq / Deku King","unset / ?","Bg_Keikoku_Saku / Tall Spiked Iron Fence","Obj_Hugebombiwa / Boulder Blocking Goron Racetrack","En_Firefly2 / Yellow Target Spot (object_En_Firefly)","En_Rat / Real Bombchu","En_Water_Effect / Water Dripping on Ground","En_Kusa2 / ?","Bg_Spout_Fire / Proximity-Activated Firewall","unset / ?","Bg_Dblue_Movebg / Great Bay Temple Gears","En_Dy_Extra / Fairy Grants Power Cutscenes - Spiral Beam of Light","En_Bal / Tingle With Balloon","En_Ginko_Man / Bank Teller, Sakon, Twin Jugglers","En_Warp_Uzu / Pirates' Fortress - Telescope on Tripod","Obj_Driftice / Ice Platform That Floats in Water","En_Look_Nuts / Deku Palace - Patrolling Deku Guard","En_Mushi2 / ?","En_Fall / ?","En_Mm3 / Counting Game Postman","Bg_Crace_Movebg / Strange Wooden/Metal Texture","En_Dno / Deku Butler","En_Pr2 / ?","En_Prz / Skullfish - Defeated","En_Jso2 / Link Turns & Walks Away on Approach","Obj_Etcetera / Pink & Green Deku Flower","En_Egol / Eyegore","Obj_Mine / Exploding Metal Spike Trap","Obj_Purify / ?","En_Tru / Koume on Broom","En_Trt / Kotake","unset / ?","unset / ?","En_Test5 / ?","En_Test6 / ?","En_Az / Beaver Bros. Big Brother","En_Estone / Rubble Blasted by Eyegore","Bg_Hakugin_Post / Snowhead Temple - Central Pillar","Dm_Opstage / Opening Cutscene - Grass in Lost Woods","Dm_Stk / Skullkid With Flute, OoT, Link Mask, Majora's Mask","Dm_Char00 / No Textures, No Display Lists to Render","Dm_Char01 / Cutscene - Woodfall Temple Rises From the Mire","Dm_Char02 / Clock Tower Roof Cutscene - OoT & Majora's Mask","Dm_Char03 / Cutscene - Happy Mask Salesman","Dm_Char04 / ?","Dm_Char05 / Healing Pamela's Father Cutscene - Gibdo Mask","Dm_Char06 / Mountain Village Unfreezes Cutscene - Mountain","Dm_Char07 / Ending Cutscene - Indigo-Go's Milk Bar Stage","Dm_Char08 / Turtle Island Cutscene - Turtle","Dm_Char09 / Beehive Cutscene - Giant Bee","Obj_Tokeidai / Clock Tower & Light Beam","unset / ?","En_Mnk / Monkey","En_Egblock / Grey Rectangular Stone Block","En_Guard_Nuts / Deku Palace - Entrance Guard","Bg_Hakugin_Bombwall / Snowhead Temple - Bombable Wall","Obj_Tokei_Tobira / Clock Tower - Swinging Doors","Bg_Hakugin_Elvpole / Snowhead Temple - Punchable Central Pole Inserts","En_Ma4 / Romani","En_Twig / Beaver Dam Twig Texture & Lifesaver Ring","En_Po_Fusen / Romani Ranch - Poe Balloon","En_Door_Etc / ?","En_Bigokuta / Big Octo","Bg_Icefloe / Ice Platform Created by Ice Arrow","Obj_Ocarinalift / Elevator With Triforce Texture","En_Time_Tag / ?","Bg_Open_Shutter / Tatl Left Behind Cutscene - Wooden Deku Door","Bg_Open_Spot / Taunted by Skullkid Cutscene - Spotlights","Bg_Fu_Kaiten / Honey & Darling's Shop - Rotating Platform","Obj_Aqua / Water Poured Out of Bottle","En_Elforg / Stray Fairy","En_Elfbub / Stray Fairy in Bubble","unset / ?","En_Fu_Mato / Honey & Darling's Shop - Target","En_Fu_Kago / Honey & Darling's Shop - Basket","En_Osn / Happy Mask Salesman","Bg_Ctower_Gear / Clock Tower - Rotating Wooden Cog","En_Trt2 / Kotake on Broom","Obj_Tokei_Step / Door to Top of Clock Tower","Bg_Lotus / Lilypad","En_Kame / Snapper","Obj_Takaraya_Wall / Treasure Chest Game - Proximity-Activated White Wall","Bg_Fu_Mizu / Circle of Water Surrounding Honey & Darling Platform","En_Sellnuts / Business Scrub Carrying Bags","Bg_Dkjail_Ivy / Ivy in Deku Jail","unset / ?","Obj_Visiblock / Invisible Blue Platforms Seen With Lens of Truth","En_Takaraya / Treasure Chest Game - Employee","En_Tsn / Great Bay - Fisherman","En_Ds2n / Ocarina of Time - Potion Shop Owner","En_Fsn / Curiosity Shop - Owner","En_Shn / Swamp Tourist Center - Guide","unset / ?","En_Stop_heishi / Clock Town - Gate-Blocking Soldier","Obj_Bigicicle / Ice Block","En_Lift_Nuts / Deku Scrub Playground - Employee","En_Tk / Dampe","unset / ?","Bg_Market_Step / West Clocktown - Stairs","Obj_Lupygamelift / Deku Scrub Playground - Rupee Elevator","En_Test7 / ?","Obj_Lightblock / Block That Dissolves in Sunlight","Mir_Ray2 / Mirror Shield Face & Light Ray","En_Wdhand / Dexihand","En_Gamelupy / Deku Scrub Playground - Large Green Rupee","Bg_Danpei_Movebg / ?","En_Snowwd / Snow-Covered Tree","En_Pm / Postman Delivering Letters","En_Gakufu / Termina Field - 2D Song Buttons Appearing on Wall","Elf_Msg4 / ?","Elf_Msg5 / ?","En_Col_Man / ?","En_Talk_Gibud / Gibdo Requesting Blue Potion","En_Giant / Giant","Obj_Snowball / Large Snowball","Boss_Hakugin / Goht","En_Gb2 / Spirit House - Owner","En_Onpuman / ?","Bg_Tobira01 / Gate to Goron Shrine","En_Tag_Obj / ?","Obj_Dhouse / Dampe's House Facade","Obj_Hakaisi / Gravestone","Bg_Hakugin_Switch / Goron Link Switch","unset / ?","En_Snowman / Eeno","TG_Sw / ?","En_Po_Sisters / Poe Sisters","En_Pp / Hiploop","En_Hakurock / Rocks Kicked Up by Goht","En_Hanabi / ?","Obj_Dowsing / ?","Obj_Wind / ?","En_Racedog / Racetrack Dog (Arrow Over Head)","En_Kendo_Js / Swordsman","Bg_Botihasira / Captain Keeta Race - Gatepost","En_Fish2 / Marine Research Lab Fish","En_Pst / Postbox","En_Poh / Poe","Obj_Spidertent / Tent-Shaped Spider Web","En_Zoraegg / Zora Egg","En_Kbt / Zubora","En_Gg / Darmani's Ghost","En_Maruta / Swordsman's School - Practice Log","Obj_Snowball2 / Small Snowball","En_Gg2 / Darmani's Ghost","Obj_Ghaka / Darmani's Gravestone","En_Dnp / Deku Princess","En_Dai / Biggoron","Bg_Goron_Oyu / Goron Hot Spring Water","En_Kgy / Gabora","En_Invadepoh / ?","En_Gk / Goron Elder's Son","En_An / Anju","unset / ?","En_Bee / Giant Bee","En_Ot / Seahorse","En_Dragon / Deep Python","Obj_Dora / Swordsman's School - Gong","En_Bigpo / Big Poe","Obj_Kendo_Kanban / Swordsman's School - Cuttable Board","Obj_Hariko / Little Cow Statue Head","En_Sth / ?","Bg_Sinkai_Kabe / No Textures, No Display Lists to Render","Bg_Haka_Curtain / Curtain That Lifts to Reveal Flat's Tomb","Bg_Kin2_Bombwall / Ocean Spider House - Bombable Wall","Bg_Kin2_Fence / Ocean Spider House - Fireplace Grate","Bg_Kin2_Picture / Ocean Spider House - Skullkid Painting","Bg_Kin2_Shelf / Ocean Spider House - Drawers","En_Rail_Skb / Ikana Graveyard - Circle of Stalchildren","En_Jg / Goron Elder","En_Tru_Mt / Koume's Target Game - Koume on Broom","Obj_Um / Cremia's Cart","En_Neo_Reeba / Leever","Bg_Mbar_Chair / Milk Bar - Chair","Bg_Ikana_Block / Stone Tower Temple - Rotating Room Pushblock","Bg_Ikana_Mirror / Stone Tower Temple - Mirror","Bg_Ikana_Rotaryroom / Stone Tower Temple - Rotating Room","Bg_Dblue_Balance / Great Bay Temple - See-Saw","Bg_Dblue_Waterfall / Great Bay Temple - Freezable Geyser","En_Kaizoku / Gerudo Pirate","En_Ge2 / Patrolling Pirate Guard","En_Ma_Yts / Romani","En_Ma_Yto / Cremia","Obj_Tokei_Turret / South Clock Town - Flags & Carnival Platform","Bg_Dblue_Elevator / Great Bay Temple - Elevator","Obj_Warpstone / Owl Statue","En_Zog / Mikau","Obj_Rotlift / Deku Moon Dungeon - Spiked Rotating Platforms","Obj_Jg_Gakki / Goron Elder - Drum","Bg_Inibs_Movebg / Twinmold Arena","En_Zot / Great Bay - Zora With Directions to Zora Hall","Obj_Tree / North Clock Town - Tree","Obj_Y2lift / Elevator?","Obj_Y2shutter / Pirate's Fortress - Interior Door","Obj_Boat / Pirate Boat","Obj_Taru / Wooden Barrel","Obj_Hunsui / Switch-Activated Geyser","En_Jc_Mato / Koume's Target Game - Target","Mir_Ray3 / Mirror Shield Face & Light Ray","En_Zob / Japas","Elf_Msg6 / ?","Obj_Nozoki / ?","En_Toto / Toto","En_Railgibud / Music Box House - Patrolling Gibdos","En_Baba / Bomb Shop Lady","En_Suttari / ?","En_Zod / Tijo","En_Kujiya / Clock Town - Lottery Shop","En_Geg / Goron With Don Gero's Mask","Obj_Kinoko / ?","Obj_Yasi / Palm Tree","En_Tanron1 / ?","En_Tanron2 / Bubbles Surrounding Wart?","En_Tanron3 / Fish Surrounding Gyorg?","Obj_Chan / Goron Village - Chandelier","En_Zos / Evan","En_S_Goro / Goron Complaining About Baby Crying","En_Nb / Anju's Grandma","En_Ja / Juggler","Bg_F40_Block / Stone Tower Temple - Movable Monkey-Faced Blocks","Bg_F40_Switch / Elegy of Emptiness Switch","En_Po_Composer / Poe Composers","En_Guruguru / Guru-Guru","Oceff_Wipe5 / ?","En_Stone_heishi / Shiro","Oceff_Wipe6 / ?","En_Scopenuts / Astral Observatory - Business Scrub in Telescope","En_Scopecrow / Astral Observatory - Guay in Telescope","Oceff_Wipe7 / ?","Eff_Kamejima_Wave / Wave Created by Turtle Awakening","En_Hg / Pamela's Father","En_Hgo / Pamela's Father As a Gibdo","En_Zov / Lulu","En_Ah / Madame Dotour","Obj_Hgdoor / Music Box House - Closet Door","Bg_Ikana_Bombwall / Stone Tower Temple - Bombable Tan Floor Tile","Bg_Ikana_Ray / Stone Tower Temple - Light Rays","Bg_Ikana_Shutter / Stone Tower Temple - Door","Bg_Haka_Bombwall / Beneath the Grave - Bombable Wall","Bg_Haka_Tomb / Flat's Tomb","En_Sc_Ruppe / Large Rotating Green Rupee","Bg_Iknv_Doukutu / Sharp's Cave","Bg_Iknv_Obj / Music Box House - Waterwheel","En_Pamera / Pamela","Obj_HsStump / Ikana Canyon - Hookshotable Tree","En_Hidden_Nuts / Swamp Spider House - Sleeping Deku Scrub","En_Zow / Great Bay - Zora Complaining About Water","En_Talk / Green Target Spot (Indigo-Go's Poster)","En_Al / Madame Aroma","En_Tab / Mr. Barten","En_Nimotsu / Bomb Shop Bag Stolen by Sakon","En_Hit_Tag / ?","En_Ruppecrow / Guay Circling Clock Town","En_Tanron4 / Flock of Seagulls","En_Tanron5 / ?","En_Tanron6 / Flock of Giant Bees","En_Daiku2 / Milk Road - Carpenter Hacking at Boulder","En_Muto / Mutoh","En_Baisen / Vissen","En_Heishi / ?","En_Demo_heishi / Title Sequence - Soldier","En_Dt / Mayor Dotour","En_Cha / Laundry Pool - Sign With Bell","Obj_Dinner / Cremia & Romani's 6pm Dinner","Eff_Lastday / Moon Crashing Into Clocktown Effects","Bg_Ikana_Dharma / Ikana Castle - Punchable Pillar Segments","En_Akindonuts / Woodfall - Business Scrub","Eff_Stk / Skullkid Screams to Call Moon Down - Effects","En_Ig / Link the Goron","En_Rg / Medigoron","En_Osk / Captain Keeta","En_Sth2 / ?","En_Yb / Kamaro","En_Rz / Rosa Sister","En_Scopecoin / ?","En_Bjt / Hand in Toilet","En_Bomjima / Bombers - Jim","En_Bomjimb / Bombers - Jim","En_Bombers / Bombers - Blue-Hatted Bomber","En_Bombers2 / Bombers - Hideout Guard","En_Bombal / Bombers - Majora Balloon","Obj_Moon_Stone / Moon's Tear","Obj_Mu_Pict / ?","Bg_Ikninside / Various Ikana Objects","Eff_Zoraband / Blue Spotlight Effect","Obj_Kepn_Koya / Gorman Bros. Buildings","Obj_Usiyane / Roof of Cow Barn","En_Nnh / Twisted Corpse of Deku Butler's Son","Obj_Kzsaku / Huge Metal Portcullis","Obj_Milk_Bin / Cart Delivery Bottle of Chateau Romani","En_Kitan / Keaton","Bg_Astr_Bombwall / Astral Observatory - Bombable Wall","Bg_Iknin_Susceil / Stone Tower Temple - Hot Checkered Ceiling","En_Bsb / Captain Keeta","En_Recepgirl / Receptionist","En_Thiefbird / Takkuri","En_Jgame_Tsn / Fisherman's Jumping Game - Fisherman","Obj_Jgame_Light / Fisherman's Jumping Game - Torch","Obj_Yado / Stockpot Inn - 2nd Floor Window","Demo_Syoten / Unknown","Demo_Moonend / Ending Cutscene - Moon Gets Tossed Back Into Sky","Bg_Lbfshot / Colourful Hookshot Target Pillar","Bg_Last_Bwall / Link Moon Dungeon - Bombable, Climbable Wall","En_And / Anju in Wedding Dress","En_Invadepoh_Demo / ?","Obj_Danpeilift / Red & Brown Elevator","En_Fall2 / Falling Moon","Dm_Al / Ending Cutscene - Madame Aroma at Wedding","Dm_An / Blue Target Spot","Dm_Ah / Ending Cutscene - Anju's Mother at Wedding","Dm_Nb / Ending Cutscene - Anju's Grandmother at Wedding","En_Drs / Wedding Dress Mannequin","En_Ending_Hero / Ending Cutscene - Mayor Dotour at Wedding","Dm_Bal / Ending Cutscene - Tingle at Wedding","En_Paper / Ending Cutscene - Confetti at Wedding","En_Hint_Skb / Stalchild - Gives Hints","Dm_Tag / ?","En_Bh / Moon - Brown Bird","En_Ending_Hero2 / Ending Cutscene - Vissen at Wedding","En_Ending_Hero3 / Ending Cutscene - Mutoh at Wedding","En_Ending_Hero4 / Ending Cutscene - Soldier Cheering Guruguru","En_Ending_Hero5 / Ending Cutscene - Carpenter Watching Indigo-Go's","En_Ending_Hero6 / ?","Dm_Gm / Blue Target Spot","Obj_Swprize / ?","En_Invisible_Ruppe / ?","Obj_Ending / Ending Cutscene - Stump With Skullkid's Doodle","En_Rsn / Ending Cutscene - Bomb Shop Owner"]
}

versionDict = {}
for v in versions:
    versionDict[v['name']] = v
f2 = open('versions.json','w')
json.dump(versionDict,f2,indent='\t')
f2.close()

###########################################

actor_count = {
    "OoT": 0x1D7,
    "MM": 0x02B2
}

hardcoded_instance_sizes = {
    "OoT": {
        0x0: 0xA90, # Player
        0x15: 0x1A0, # En_Item00
        0x39: 0x1C0 # En_A_Obj
    },
    "MM": {
        0x0: 0xD80, # Player
        0xE: 0x1B0, # En_Item00
        0x26: 0x1A0 # En_A_Obj
    }
}

actors = {
    "OoT": [{} for _ in range(actor_count["OoT"])],
    "MM": [{} for _ in range(actor_count["MM"])]
}

for v in versions:
    print(v['name'])
    f=open('roms/'+v['filename'],'rb')
    rom = f.read()

    for actorId in range(actor_count[v['game']]):
        romStart, romEnd, ramStart, ramEnd, _, ramInitVars, _, allocType, _, _ = struct.unpack('>IIIIIIIhbb',rom[v['actortable']+0x20*actorId:v['actortable']+0x20*(actorId+1)])
        overlaySize = ramEnd-ramStart
        romInitVars = romStart+ramInitVars-ramStart
        if 0 < romInitVars < 0x80000000:
            _,_,_,instanceSize = struct.unpack('>IIII',rom[romInitVars:romInitVars+0x10])
        elif ramInitVars > 0:
            instanceSize = hardcoded_instance_sizes[v['game']][actorId]
        else:
            instanceSize = None
        actorInfo = {'actorId':actorId,'overlaySize':overlaySize, 'instanceSize':instanceSize, 'allocType':allocType, 'name':actor_names[v['game']][actorId]}
        actors[v['game']][actorId][v['name']] = actorInfo

#for i in range(actor_count):
#    if (actors[i]["N-1.0"]==actors[i]["N-1.1"]==actors[i]["P-1.0"]==actors[i]["N-1.2"]==actors[i]["P-1.1"]==
#        actors[i]["J-GC-MQDisc"]==actors[i]["J-MQ"]==actors[i]["U-GC"]==actors[i]["U-MQ"]==actors[i]["P-GC"]==actors[i]["P-MQ"]==actors[i]["J-GC-CEDisc"]):
#        actors[i] = {'ALL':actors[i]["N-1.0"]}
#    elif (actors[i]["N-1.0"]==actors[i]["N-1.1"]==actors[i]["P-1.0"]==actors[i]["N-1.2"]==actors[i]["P-1.1"]) and (
#        actors[i]["J-GC-MQDisc"]==actors[i]["J-MQ"]==actors[i]["U-GC"]==actors[i]["U-MQ"]==actors[i]["P-GC"]==actors[i]["P-MQ"]==actors[i]["J-GC-CEDisc"]):
#        actors[i] = {'N64':actors[i]["N-1.0"],'GC':actors[i]["J-GC-MQDisc"]}
#    else:
#        pass

f2 = open('actors.json','w')
json.dump(actors,f2,indent='\t')
f2.close()

#########################################################

scene_count = {
    "OoT": 0x65,
    "MM": 0x71
}

scenes = {
    "OoT": [{} for _ in range(scene_count["OoT"])],
    "MM": [{} for _ in range(scene_count["MM"])]
}

min_setup_count = {
    "OoT": 4,
    "MM": 1
}

for v in versions:
    print(v['name'])
    f=open('roms/'+v['filename'],'rb')
    rom = f.read()

    for sceneId in range(scene_count[v['game']]):

        scenes[v['game']][sceneId][v['name']] = [None] * min_setup_count[v['game']]

        if v['game'] == 'MM':
            sceneRomStart, sceneRomEnd, _, _ = struct.unpack('>IIII',rom[v['scenetable']+0x10*sceneId:v['scenetable']+0x10*(sceneId+1)])
        else:
            sceneRomStart, sceneRomEnd, _, _, _ = struct.unpack('>IIIII',rom[v['scenetable']+0x14*sceneId:v['scenetable']+0x14*(sceneId+1)])
        #print('scene', hex(sceneId), hex(sceneRomStart), hex(sceneRomEnd))

        if sceneRomStart==0 and sceneRomEnd==0:
            continue # null entry

        sceneAltHeaders = None
        roomAltHeaders = {}

        for setupId in range(min_setup_count[v['game']]):

            #print('setup', hex(setupId))
            if setupId == 0:
                scenes[v['game']][sceneId][v['name']][setupId] = {'rooms':[],'transitionActors':[]}
                sceneHeaderStart = sceneRomStart
            else:
                if sceneAltHeaders and sceneAltHeaders[setupId-1]:
                    scenes[v['game']][sceneId][v['name']][setupId] = {'rooms':[],'transitionActors':[]}
                    sceneHeaderStart = sceneRomStart + (sceneAltHeaders[setupId-1]&0x00FFFFFF)
                else:
                    scenes[v['game']][sceneId][v['name']][setupId] = None
                    continue
            
            sceneHeaderCommand = None
            sceneHeaderNum = 0
            while sceneHeaderCommand != 0x14:
                sceneHeaderCommand, sceneParam1, _, sceneParam2 = struct.unpack('>BBHI',rom[sceneHeaderStart+8*sceneHeaderNum:sceneHeaderStart+8*(sceneHeaderNum+1)])

                #print('cmd',hex(sceneHeaderCommand))
                assert sceneHeaderCommand < 0x1F
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
                                    if v['game'] == 'MM':
                                        actorId, _, _, _, spawnTimeHi, _, spawnTimeLo, actorParams = struct.unpack('>HHHHHHHH',rom[actorListStart+0x10*actorNum:actorListStart+0x10*(actorNum+1)])
                                        actorId &= 0xFFF
                                        spawnTimeBits = ((spawnTimeHi & 0x7) << 7) | spawnTimeLo & 0x7F
                                        spawnTime = [(spawnTimeBits>>x) & 1 for x in reversed(range(10))]
                                        roomData['actors'].append({'actorId':actorId,'actorParams':actorParams,'spawnTime':spawnTime})
                                    else:
                                        actorId, _, _, _, _, _, _, actorParams = struct.unpack('>HHHHHHHH',rom[actorListStart+0x10*actorNum:actorListStart+0x10*(actorNum+1)])
                                        roomData['actors'].append({'actorId':actorId,'actorParams':actorParams})
                            roomHeaderNum += 1
                            
                        scenes[v['game']][sceneId][v['name']][setupId]['rooms'].append(roomData)
            
                elif sceneHeaderCommand == 0x0E: # Transition Actors
                    for transitionActorNum in range(sceneParam1):
                        transitionActorListStart = sceneRomStart + (sceneParam2&0x00FFFFFF)
                        frontRoom, _, backRoom, _, actorId, _, _, _, _, actorParams = struct.unpack('>BBBBHHHHHH',rom[transitionActorListStart+0x10*transitionActorNum:transitionActorListStart+0x10*(transitionActorNum+1)])
                        scenes[v['game']][sceneId][v['name']][setupId]['transitionActors'].append({'frontRoom':frontRoom,'backRoom':backRoom,'actorId':actorId,'actorParams':actorParams})
                
                sceneHeaderNum += 1
                
            if sceneAltHeaders:
                assert len(roomAltHeaders) == len(scenes[v['game']][sceneId][v['name']][setupId]['rooms'])
            else:
                assert len(roomAltHeaders) == 0
            
#for i in range(scene_count):
#    if (scenes[i]["N-1.0"]==scenes[i]["N-1.1"]==scenes[i]["P-1.0"]==scenes[i]["N-1.2"]==scenes[i]["P-1.1"]==scenes[i]["J-GC-MQDisc"]==scenes[i]["U-GC"]==scenes[i]["P-GC"]==scenes[i]["J-GC-CEDisc"]
#        ==scenes[i]["J-MQ"]==scenes[i]["U-MQ"]==scenes[i]["P-MQ"]):
#        scenes[i] = {'ALL':scenes[i]["N-1.0"]}
#    elif (scenes[i]["N-1.0"]==scenes[i]["N-1.1"]==scenes[i]["P-1.0"]==scenes[i]["N-1.2"]==scenes[i]["P-1.1"]==scenes[i]["J-GC-MQDisc"]==scenes[i]["U-GC"]==scenes[i]["P-GC"]==scenes[i]["J-GC-CEDisc"]
#          ) and (scenes[i]["J-MQ"]==scenes[i]["U-MQ"]==scenes[i]["P-MQ"]):
#        scenes[i] = {'VANILLA':scenes[i]["N-1.0"],'MQ':scenes[i]["J-MQ"]}
#    else:
#        pass

f2 = open('scenes.json','w')
json.dump(scenes,f2,indent='\t')
f2.close()
