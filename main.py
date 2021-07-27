import os
import json
from datetime import date
from github import Github
from crawl_olympic import parsing_bs, crawl_ranking_data, crawl_medalist_data


def gh_update(repo, new_data, file):
    updated = date.today().isoformat()
    contents = repo.get_contents(file)
    repo.update_file(contents.path, f"update crawling data : {updated}", json.dumps(new_data, ensure_ascii=False), contents.sha, branch="main")


if __name__ == '__main__':
    g = Github(os.environ['ACCESS_TOKEN'])
    BASE_URL = 'https://olympics.com/tokyo-2020/olympic-games/ko/results/all-sports/medal-standings.htm'
    soup = parsing_bs(BASE_URL)
    rank_data = crawl_ranking_data(soup)
    repo = g.get_repo("Zih0/olympic-rank")
    gh_update(repo, rank_data, "rank_data.json")
    MEDAL_URL = 'https://olympics.com/tokyo-2020/olympic-games/ko/results/all-sports/zzjm094b.json'
    medalist_data = crawl_medalist_data(MEDAL_URL)
    gh_update(repo, medalist_data, "medalist_data.json")
