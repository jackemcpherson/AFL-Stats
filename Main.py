import pandas as pd

def getFullPlayerStats(year):
  player_stats = pd.read_html(f"https://afltables.com/afl/stats/{year}.html")
  clean_dfs = []
  for x in player_stats[1:]:
    x["team"] = str(x.columns[0][0]).split(" [")[0]
    x.columns = x.columns.droplevel(0)
    x.columns = ['#', 'Player', 'GM', 'KI', 'MK', 'HB', 'DI', 'DA', 'GL', 'BH', 'HO','TK', 'RB', 'IF', 'CL', 'CG', 'FF', 'FA', 'BR', 'CP', 'UP', 'CM', 'MI','1%', 'BO', 'GA', '%P', 'SU', 'Team']
    clean_dfs.append(x[:-1])
  full_player_stats = (pd.concat(clean_dfs)).fillna(0).reset_index(drop=True)
  return full_player_stats

def getPlayerRankings(year, include_full_stats=False):
  FPS = getFullPlayerStats(year)
  FPS["OFF_Score"] = FPS["GL"] * 6 + FPS["BH"] + 0.25 * FPS["HO"] + 3 * FPS["GA"] + FPS["IF"] + FPS["MI"] + (FPS["FF"] - FPS["FA"])
  FPS["MID_Score"] = 15 * FPS["IF"] + 20 * FPS["CL"] + 3 * FPS["TK"] + 1.5 * FPS["HO"] + (FPS["FF"] - FPS["FA"])
  FPS["DEF_Score"] = 20 * FPS["RB"] + 12 * FPS["1%"] + (FPS["MK"] - 4 * FPS["MI"] + 2 * (FPS["FF"] - FPS["FA"])) - 0.66 * FPS["HO"]
  if include_full_stats == False:
    return FPS[["Team", "Player", "OFF_Score", "MID_Score", "DEF_Score"]]
  elif include_full_stats == True:
    return FPS