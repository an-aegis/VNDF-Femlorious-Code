# VNDFHelper.py
# V0.7.1
import re

class ApiError(Exception):
    pass

rankval_id = {
    "E-0": 1534948496069628084,
    
    "E-1": 1534948494710804561,
    
    "E-2": 1534948493406376046,
    
    "E-3": 1534948492114399392,
    
    "E-4": 1534948490218569809,
    
    "E-5": 1534948488352239699,
    
    "E-6": 1534948487236681738,
    
    "E-7": 1534948486192038038,
    
    "E-8": 1534948484996796536,
    
    "E-9": 1534948483885301801,
    
    "E-10": 1534948482832400588,
    
    "O-1": 1534948481830224003,
    
    "O-2": 1534948480835915796,
    
    "O-3": 1534948479787470918,
    
    "O-4": 1534948478738763947,
    
    "O-5": 1534948466252451871,
    
    "O-6": 1534948466252451871,
    
    "O-7": 1534948465107275846,
    
    "O-8": 1534948464071540897,
    
    "O-9": 1534948463094005841,
    
    "O-10": 1534948462100217906,
    }
c_rankval_id = {
    "C0": 1534948460984402040,
    "C1": 1534948458689986652,
    "C2": 1534948457704329266,
    "C3": 1534948456572125365,
    "C4": 1534948455041073265
    }

def findname(rankval: str): # this could be a dict, but i felt like a function was prettier
    match rankval:
        case "E-0":
            return "Recruit"
        case "E-1":
            return "PSC"
        case "E-2":
            return "PFC"
        case "E-3":
            return "Specialist"
        case "E-4":
            return "Corporal"
        case "E-5":
            return "Sergeant"
        case "E-6":
            return "Staff Sergeant"
        case "E-7":
            return "Sgnt Mj. B"
        case "E-8":
            return "Sgnt Mj. A"
        case "E-9":
            return "First Sergeant"
        case "E-10":
            return "Command Sergeant"
        case "O-1":
            return "Lt. "
        case "O-2":
            return "Captain"
        case "O-3":
            return "Major"
        case "O-4":
            return "Colonel 2nd Cl."
        case "O-5":
            return "Colonel 1st Cl."
        case "O-6":
            return "Brigadier General"
        case "O-7":
            return "Lieutenant General"
        case "O-8":
            return "Major General"
        case "O-9":
            return "General 1st Cl."
        case "O-10":
            return "Field Marshal"

async def get_role(member,ID:int):
    role = member.guild.get_role(ID)
    return role

def hunt_for_rankval(roles:list) -> str:
    if roles != []:
        id_rankval = {value: key for key,value in rankval_id.items()} # shush ik its slow
        
        rankfound = False
        for role in roles:
            if role.id in id_rankval:
                rankfound = True
                break
        
        if rankfound:
            return id_rankval[role.id]
        else:
            raise ApiError("No rank was able to be found for the target")
    else:
        raise ApiError("Member roles were not found")

def findc_rank(rankval: str):
    if rankval in ["E-1","E-2","E-3","E-4"]:
        return "C0"
    elif rankval in ["E-5","E-6","E-7"]:
        return "C1"
    elif rankval in ["E-8","E-9","E-10","O-1","O-2"]:
        return "C2"
    elif rankval in ["O-3","O-4","O-5","O-6"]:
        return "C3"
    elif rankval in ["O-7","O-8","O-9","O-10"]:
        return "C4"
    else:
        return "" # recruit

def ranktoint(rankval):
    rankval_list = list(rankval_id)
    
    return rankval_list.index(rankval)

def inttorank(ranknum):
    rankval_list = list(rankval_id)
    
    return rankval_list[ranknum]

def namegen(currnick, rankname, rankval, c_rankval):
    # Brigadier - 2Shots (O-6/C-3)
    pattern = re.compile(
        r"-(?:\s*)(?P<username>[^(\r\n]+?)(?=\s*\()"
        )
    match = pattern.search(currnick)
    slash = "/" if rankval != "E-0" else ""
    if match != None:
        check = f"{rankname} - {match.group('username')} ({rankval}{slash}{c_rankval})"
        if len(check) <= 33:
            return check
        else:
            return f"{match.group('username')}({rankval}{slash}{c_rankval})"
    else:
        print("bad case")
        check = f"{rankname} - {currnick} ({rankval}{slash}{c_rankval})"
        if len(check) <= 32:
            return check
        else:
            return f"{currnick} ({rankval}{slash}{c_rankval})"
    
    
