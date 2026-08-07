# VNDFRank.py
import discord
from VNDFHelper import rankval_id, c_rankval_id, findname, get_role, hunt_for_rankval

class rank:
    def __init__(self, who = None, roles = None, rankval = "", __rankname = ""):
        self.who:discord.Member = who # discord member object
        self.roles:list = roles
        self.rankval:str = rankval
        self.rankname:str = __rankname
        self.displayname:str|None = ""
        self.old_rankval:str|None = None
        
        if self.who != None:
            self.displayname = self.who.nick
        
        if self.rankval == "":
            if self.roles == None:
                self.roles = self.who.roles
            
            self.rankval = hunt_for_rankval(self.roles)
            # error generating function is intended to create unhandled exceptions in this class
            # this is so the caller can handle this exception
        
        self.rankname = findname(self.rankval)
    
    def promo_calc(self, by:int, limit:int) -> list:
        
        ranklist = list(rankval_id)
        
        newrank_index = ranklist.index(self.rankval)+by
        
        if newrank_index < limit:
            newrankval = ranklist[newrank_index] # find new rankval
            
            if newrank_index < 5:
                new_c_rank = "C0"
            elif newrank_index in range(5,8):
                new_c_rank = "C1"
            elif newrank_index in range(8,13):
                new_c_rank = "C2"
            elif newrank_index in range(13,17):
                new_c_rank = "C3"
            elif newrank_index in range(17,21):
                new_c_rank = "C4"
            self.rankval = newrankval
            return [rankval_id[newrankval],new_c_rank] # [new rankval, new c_rankval]
        else:
            raise IndexError("The rank you are trying to promote to is above your authority level or is impossible")
    
    async def promote(self,by:int, limit:int):
        self.old_rankval = self.rankval
        old = await get_role(self.who, rankval_id[self.rankval])
        
        # error generating function is intended to create unhandled exceptions in this class
        # this is so the caller can handle this exception
        # exception also serves to protect from disalowed promotion cases
        calculated = self.promo_calc(by,limit)
        new_id = calculated[0]
        
        c_rankval = calculated[1]
        c_rank_obj = await get_role(self.who, c_rankval_id[c_rankval])
        
        if c_rank_obj not in self.roles:
            await self.who.add_roles(c_rank_obj)
            c_rank_list = list(c_rankval_id)
            try:
                subtract = 1 if by>0 else -1
                await self.who.remove_roles(await get_role(self.who,c_rankval_id[c_rank_list[c_rank_list.index(c_rankval)-subtract]]))
                # gets index of current rankval, subtracts 1 and reads whats at that index
                # gets that role id and then removes it
            except:
                pass
                # there is no such old c rank
        
        await self.who.add_roles(await get_role(self.who, new_id))
        await self.who.remove_roles(old) # prevent removal without assignment first
        
