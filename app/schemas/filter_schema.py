from enum import Enum

class Filter(str, Enum): 
    NEXT_MONTH = "next-month"
    CURRENT_MONTH = "current-month"
    NEXT_WEEK = "next-week"
    CURRENT_WEEK = "current-week"