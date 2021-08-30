import pandas as pd


def getAllResults():
    # Returns a dataframe containing all AFL match results for all time.
    df = pd.read_fwf(
        "https://afltables.com/afl/stats/biglists/bg3.txt",
        widths=[7, 17, 5, 18, 17, 18, 18, 18],
        skiprows=1,
    )
    df.columns = [
        "Key",
        "Date",
        "Round",
        "Home",
        "Home_Score",
        "Away",
        "Away_Score",
        "Venue",
    ]
    df = df.drop(columns="Key")

    df["Home_G"] = [int(x.split(".")[0]) for x in df["Home_Score"]]
    df["Home_B"] = [int(x.split(".")[1]) for x in df["Home_Score"]]
    df["Home_Score"] = [int(x.split(".")[2]) for x in df["Home_Score"]]

    df["Away_G"] = [int(x.split(".")[0]) for x in df["Away_Score"]]
    df["Away_B"] = [int(x.split(".")[1]) for x in df["Away_Score"]]
    df["Away_Score"] = [int(x.split(".")[2]) for x in df["Away_Score"]]

    df["Year"] = [pd.to_datetime(x).date().year for x in df["Date"]]

    df = df[
        [
            "Date",
            "Year",
            "Round",
            "Home",
            "Home_G",
            "Home_B",
            "Home_Score",
            "Away",
            "Away_G",
            "Away_B",
            "Away_Score",
            "Venue",
        ]
    ]
    return full_results


def getFullPlayerStats(year: int):
    player_stats = pd.read_html(f"https://afltables.com/afl/stats/{year}.html")
    clean_dfs = []
    for x in player_stats[1:]:
        x["team"] = str(x.columns[0][0]).split(" [")[0]
        x.columns = x.columns.droplevel(0)
        x = x.rename(columns={"": "Team"})[:-1]
        clean_dfs.append(x)
    full_player_stats = (pd.concat(clean_dfs)).fillna(0).reset_index(drop=True)
    return full_player_stats


def getPlayerRankings(year: int, include_full_stats: bool = False):
    FPS = getFullPlayerStats(year)
    FPS["OFF_Score"] = (
        FPS["GL"] * 6
        + FPS["BH"]
        + 0.25 * FPS["HO"]
        + 3 * FPS["GA"]
        + FPS["IF"]
        + FPS["MI"]
        + (FPS["FF"] - FPS["FA"])
    )
    FPS["MID_Score"] = (
        15 * FPS["IF"]
        + 20 * FPS["CL"]
        + 3 * FPS["TK"]
        + 1.5 * FPS["HO"]
        + (FPS["FF"] - FPS["FA"])
    )
    FPS["DEF_Score"] = (
        20 * FPS["RB"]
        + 12 * FPS["1%"]
        + (FPS["MK"] - 4 * FPS["MI"] + 2 * (FPS["FF"] - FPS["FA"]))
        - 0.66 * FPS["HO"]
    )
    if include_full_stats == False:
        return FPS[["Team", "Player", "OFF_Score", "MID_Score", "DEF_Score"]]
    elif include_full_stats == True:
        return FPS
