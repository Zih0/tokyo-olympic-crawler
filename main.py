import json
from crawl_olympic import parsing_bs, crawl_ranking_data, crawl_medalist_data


def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == "__main__":
    BASE_URL = "https://olympics.com/tokyo-2020/olympic-games/ko/results/all-sports/medal-standings.htm"
    soup = parsing_bs(BASE_URL)
    rank_data = crawl_ranking_data(soup)
    MEDAL_URL = "https://olympics.com/tokyo-2020/olympic-games/ko/results/all-sports/zzjm094b.json"
    (
        medalists_result,
        gold_result,
        silver_result,
        bronze_result,
        kr_result,
    ) = crawl_medalist_data(MEDAL_URL)

    write_json(rank_data, "data/rank_data.json")
    write_json(medalists_result, "data/medalist_data.json")
    write_json(gold_result, "data/gold_data.json")
    write_json(silver_result, "data/silver_data.json")
    write_json(bronze_result, "data/bronze_data.json")
    write_json(kr_result, "data/kr_data.json")
