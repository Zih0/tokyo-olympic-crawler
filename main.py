import os
import json
from datetime import date
from github import Github
from crawl_olympic import parsing_bs, crawl_ranking_data

def gh_create(repo,new):
    updated = date.today().isoformat()
    repo.create_file("crawling_data.json", f"update crawling data : {updated}", json.dumps(new, ensure_ascii=False), branch="main")

def gh_update(repo,new):
    updated = date.today().isoformat()
    contents = repo.get_contents('crawling_data.json')
    repo.update_file(contents.path, f"update crawling data : {updated}", json.dumps(new, ensure_ascii=False), contents.sha, branch="main")


if __name__ == '__main__':
    g = Github(os.environ['MY_GITHUB_TOKEN'])
    BASE_URL = 'https://olympics.com/tokyo-2020/olympic-games/ko/results/all-sports/medal-standings.htm'
    soup = parsing_bs(BASE_URL)
    data = crawl_ranking_data(soup)
    repo = g.get_repo("Zih0/github-action-python")
    gh_update(repo,data)

