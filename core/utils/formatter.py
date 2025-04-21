def extract_repo_name(url: str) -> str:
    return url.rstrip('/').split('/')[-1]