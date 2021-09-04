from Main import *


def buildFullCleanDataframe(year: int):
    df = getPlayerRankings(year, include_full_stats=True)
    df = df[
        [
            "Team",
            "#",
            "Name",
            "GM",
            "KI",
            "MK",
            "HB",
            "DI",
            "DA",
            "GL",
            "BH",
            "HO",
            "TK",
            "RB",
            "IF",
            "CL",
            "CG",
            "FF",
            "FA",
            "BR",
            "CP",
            "UP",
            "CM",
            "MI",
            "1%",
            "BO",
            "GA",
            "%P",
            "SU",
            "DOB",
            "Debut",
            "Age",
            "Career_Age",
            "OFF_Score",
            "MID_Score",
            "DEF_Score",
        ]
    ]
    return df


if __name__ == "__main__":
    season = input("Year: ")
    df = buildFullCleanDataframe(season)
    df.to_csv(f"Season {season}.csv")
