# VNDFRank.py
# V0.6

import discord
from VNDFHelper import rankval_id, c_rankval_id, findname, get_role, hunt_for_rankval, findc_rank

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
        if newrank_index < 0:
            class FuckYouError(Exception):
                pass
            raise FuckYouError("No, you cant make somebody have a negative rank")
        
        if newrank_index < limit:
            newrankval = ranklist[newrank_index] # find new rankval
            self.rankval = newrankval
            
            new_c_rank = findc_rank(newrankval)
            return [newrankval,new_c_rank] # [new rankval, new c_rankval]
        else:
            raise IndexError("The rank you are trying to promote to is above your authority level or is impossible")
    
    async def promote(self,by:int, limit:int):
        self.old_rankval = self.rankval
        old = await get_role(self.who, rankval_id[self.rankval])
        
        # error generating function is intended to create unhandled exceptions in this class
        # this is so the caller can handle this exception
        # exception also serves to protect from disalowed promotion cases
        calculated = self.promo_calc(by,limit)
        new_id = rankval_id[calculated[0]]
        
        c_rankval = calculated[1]
        try:
            c_rank_obj = await get_role(self.who, c_rankval_id[c_rankval])
            new_c_rank = True
        except KeyError: # key error occurs when findc_rank returns "", meaning the person is a recruit (no c rank)
            c_rank_obj = None
            new_c_rank = False
        
        if c_rank_obj not in self.roles:
            if new_c_rank:
                await self.who.add_roles(c_rank_obj)
            
            try:
                await self.who.remove_roles(await get_role(self.who,c_rankval_id[findc_rank(self.old_rankval)]))
            except:
                pass
                # there is no such old c rank
        
        await self.who.add_roles(await get_role(self.who, new_id))
        await self.who.remove_roles(old) # prevent removal without assignment first
        
