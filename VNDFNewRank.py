# VNDFNewRank.py
# V0.7

#import discord
from VNDFHelper import hunt_for_rankval, ranktoint, inttorank, findname, findc_rank, rankval_id, c_rankval_id

class NewRank:
    class AuthorityError(Exception):
        pass
    
    def __init__(self, who):
        self.who = who
        
        self.rankval = hunt_for_rankval(who.roles)
        self.limit = 0
    def __repr__(self):
        return f"Rank({self.who}, {self.rankval})"
    def __int__(self) -> int:
        return ranktoint(self.rankval)
    def __str__(self) -> str:
        return findname(self.rankval)
    def __add__(self, by:int):
        newint:int = ranktoint(self.rankval)+by
        if newint > self.limit:
            raise self.AuthorityError(f"Exceeded authority.\nYour promotion limit is {self.limit}, you tried to get to {newint}")
        
        self.rankval = inttorank(newint)
        return self
    def __sub__(self, by:int):
        currint = ranktoint(self.rankval)
        newint:int = currint-by
        if newint < 0:
            raise ValueError("You cannot demote below E-0")
        if currint > self.limit:
            raise self.AuthorityError(f"Exceeded authority.\nYour promotion limit is {self.limit}, you tried to alter {currint}")
        
        self.rankval = inttorank(newint)
        return self
    
    def get_c_rank(self) -> str:
        return findc_rank(self.rankval)
    def get_id(self) -> list:
        try:
            return [rankval_id[self.rankval], c_rankval_id[findc_rank(self.rankval)]]
        except KeyError:
            return [rankval_id[self.rankval], ""]
        
    

