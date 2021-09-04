import pandas as pd


def getAllResults(full_historical_data: bool = False):
    # Returns a dataframe containing all AFL match results for all time.
    # Defaults to debuts after 2000 unless overridden using the full_historical_data flag.

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

    full_results = df[
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
    if full_historical_data == True:
        return full_results
    else:
        full_results = full_results[full_results["Year"] >= 2000].reset_index(drop=True)
        return full_results


# Working on returning full team stats for above function


def getMatchTeamStats(url: str):
    team_stats = pd.read_html(url, attrs={"class": "sortable"})

    home = team_stats[0]
    away = team_stats[1]
    home_team = home.columns[0][0].split(" Match")[0]
    away_team = away.columns[0][0].split(" Match")[0]
    home.columns = home.columns.droplevel()
    away.columns = away.columns.droplevel()
    home["Player"] = home_team
    away["Player"] = away_team

    a = home[home["#"].isin(["Totals"])]
    b = home[home["#"].isin(["Opposition"])]

    home_stats = pd.merge(a, b, on="Player", suffixes=("", "_Opp"))

    a = away[away["#"].isin(["Totals"])]
    b = away[away["#"].isin(["Opposition"])]

    away_stats = pd.merge(a, b, on="Player", suffixes=("", "_Opp"))

    home_stats = home_stats.drop(["#", "#_Opp"], axis="columns")
    away_stats = away_stats.drop(["#", "#_Opp"], axis="columns")

    return home_stats, away_stats
