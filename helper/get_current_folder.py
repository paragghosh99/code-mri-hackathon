def get_current_folder(page_url):
    if "tree/" not in page_url:
        return "root"

    path = page_url.split("tree/")[1]
    parts = path.split("/")[1:]   # remove branch name
    return "/".join(parts)