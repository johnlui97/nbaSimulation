import random

TotalGameTime = 48.0
tip_off_result = 5

homeScore = 0
awayScore = 0

def away_Defence_Blocks():
    awayteam_blocks = 10
    away_Block = awayteam_blocks / possessions

    return away_Block

def PACE_Calculation(PACE_raw):
    Upper_range = int(round(PACE_raw + 3))
    Lower_range = int(round(PACE_raw - 3))
    Simulation_PACE = random.randint(Lower_range, Upper_range)

    return Simulation_PACE

Home_Possessions = PACE_Calculation(102.20)
Away_Possessions = PACE_Calculation(100.29)

def away_Defence_Steals(stls, Away_Possessions):
    away_Steals = stls / Away_Possessions

    return away_Steals

def home_Defence_Steals(stls, Away_Possessions):
    away_Steals = stls / Away_Possessions

    return away_Steals

def away_Defence_Blocks(blks, Away_Possessions):
    away_Block = blks / Away_Possessions

    return away_Block

def home_Defence_Blocks(blks, Away_Possessions):
    away_Block = blks / Away_Possessions

    return away_Block

def away_Defensive_Rebounding(DReb, TotalReb):
    sum_Rebound = float(DReb / TotalReb)

    return sum_Rebound

def home_Defensive_Rebounding(DReb, TotalReb):
    sum_Rebound = float(DReb / TotalReb)

    return sum_Rebound

def away_Offensive_Rebounding(OReb, TotalReb):
    sum_Rebound = float(OReb / TotalReb)

    return sum_Rebound

def home_Offensive_Rebounding(OReb, TotalReb):
    sum_Rebound = float(OReb / TotalReb)
    return sum_Rebound

def away_CloseOutFGP(PGDFG, SGDFG, SFDFG, PFDFG, CDFG):
    sum_DFG = float(PGDFG + SGDFG + SFDFG + PFDFG + CDFG) / 5
    return sum_DFG

CloseOutfgp = (away_CloseOutFGP( .452, .448, .478, .462, .475))
    
def Home_Player_Possessions(Home_Possessions, USG, Minutes):
    MinutesRatio = float(Minutes/TotalGameTime)
    Player_OnFloor = MinutesRatio * Home_Possessions
    Player_Possessions = int(Player_OnFloor * USG)
    Variance_Player_Possessions = random.randint((Player_Possessions - 3), (Player_Possessions + 3))

    return Variance_Player_Possessions

Player1_Possessions = Home_Player_Possessions(Home_Possessions, .197, 33.8)

def OpenAttempts(Player1_Possessions, FREQ):
    NumberShotsWideOpen = round(Player1_Possessions * FREQ)
    return NumberShotsWideOpen

def UncontestedAttempts(Player1_Possessions, FREQ):
    NumberShotsWideOpen = round(Player1_Possessions * FREQ)
    return NumberShotsWideOpen

def ContestedAttempts(Player1_Possessions, FREQ):
    NumberShotsWideOpen = round(Player1_Possessions * FREQ)
    return NumberShotsWideOpen

Player1_OpenAttempts_Possessions = OpenAttempts(Player1_Possessions, .250)
Player1_UncontestdAttempts_Possessions = UncontestedAttempts(Player1_Possessions, .310)
Player1_ContestedAttempts_Possessions = ContestedAttempts(Player1_Possessions, .149)

Remaining_Player1_Possessions = Player1_Possessions - Player1_OpenAttempts_Possessions - Player1_UncontestdAttempts_Possessions - Player1_ContestedAttempts_Possessions

def Open_Shot_Attempt(FG2, FG3, FREQ, Player1_Possessions, FreqTwo, FreqThree):
    NumberShotsWideOpen = Player1_Possessions * FREQ
    RateOfTwo = FreqTwo / FREQ
    RateOfThree = FreqThree / FREQ
    TwoPointAttempts = round((NumberShotsWideOpen * RateOfTwo) + 0.5)
    ThreePointAttempts = round(NumberShotsWideOpen * RateOfThree)
    contribution = 0

    i = 0
    x = 0
    
    while(i < TwoPointAttempts):
            if(random.random() < FG2):
                contribution += 2
                i += 1
            else:
                i += 1
                
    while(x < ThreePointAttempts):
            if(random.random() < FG3):
                contribution += 3
                x += 1
            else:
                x += 1

    return contribution

def Uncontested_Shot_Attempt(FG2, FG3, FREQ, Player1_Possessions, FreqTwo, FreqThree):
    NumberShotsWideOpen = Player1_Possessions * FREQ
    RateOfTwo = FreqTwo / FREQ
    RateOfThree = FreqThree / FREQ
    TwoPointAttempts = round((NumberShotsWideOpen * RateOfTwo))
    ThreePointAttempts = round(NumberShotsWideOpen * RateOfThree)
    contribution = 0

    i = 0
    x = 0
    
    while(i < TwoPointAttempts):
            if(random.random() < FG2):
                contribution += 2
                i += 1
            else:
                i += 1
                
    while(x < ThreePointAttempts):
            if(random.random() < FG3):
                contribution += 3
                x += 1
            else:
                x += 1

    return contribution

def Contested_Shot_Attempt(CloseOutfgp, FG3, FREQ, Player1_Possessions, FreqTwo, FreqThree):
    NumberShotsWideOpen = Player1_Possessions * FREQ
    RateOfTwo = FreqTwo / FREQ
    RateOfThree = FreqThree / FREQ
    TwoPointAttempts = round((NumberShotsWideOpen * RateOfTwo) + .5)
    ThreePointAttempts = round(NumberShotsWideOpen * RateOfThree)
    contribution = 0

    i = 0
    x = 0
    
    while(i < TwoPointAttempts):
            if(random.random() < FG2):
                contribution += 2
                i += 1
            else:
                i += 1
                
    while(x < ThreePointAttempts):
            if(random.random() < FG3):
                contribution += 3
                x += 1
            else:
                x += 1

    return contribution

def Generic_Shot_Attempt(Remaining_Player1_Possessions, FGA, P3A, FG2, FG3):
    TotalAttempts = (FGA + P3A)
    NumberOfTwo = FGA / TotalAttempts
    NumberOfThree = P3A / TotalAttempts
    contribution = 0
    
    i = 0
    x = 0

    while(i < FG2):
            if(random.random() < FG2):
                contribution += 2
                i += 1
            else:
                i += 1
                
    while(x < FG3):
            if(random.random() < FG3):
                contribution += 3
                x += 1
            else:
                x += 1

    return contribution    

def tipOff():
    global tip_off_result
    result
    tip_off_result = random.randint(0,1)
    if(tip_off_result == 1):
        result = 1
        return result
    else:
        result = 0
        return result
        
