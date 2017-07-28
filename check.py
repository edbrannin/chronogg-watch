import sys
import os
import json

# import pushbullet_cli
# import requests

CACHE_DIR="cache"

def read_cache(name):
    with open(os.path.join(CACHE_DIR, name)) as in_file:
        return json.load(in_file)

def check_json(old_json, new_json):
    return check(json.load(old_json), json.load(new_json))

def check_jsons(old_json, new_json):
    return check(json.loads(old_json), json.loads(new_json))

def check(old, new):
    old_by_url, new_by_url = map(lambda items : { item['url'] : item for item in items if item['url'] }, (old, new))
    new_urls, old_urls = set(new_by_url.keys()), set(old_by_url.keys())
    added_urls = new_urls - old_urls
    removed_urls = old_urls - new_urls

    current_previews = set([tuple(item.items()) for item in new if item['status'] == 'preview'])
    old_previews = set([tuple(item.items()) for item in old if item['status'] == 'preview'])

    return (
            [new_by_url[x] for x in added_urls] + [dict(item) for item in list(current_previews - old_previews)],
            [old_by_url[x] for x in removed_urls] + [dict(item) for item in list(old_previews - current_previews)],
            )

def main():
    added, removed = check(read_cache('result-old.json'), read_cache('result.json'))
    total = len(added) + len(removed)

    if total == 0:
        sys.exit(0)

    title = 'Chrono Store: '

    if added:
        print "Added:"
        for item in added:
            print json.dumps(item, indent=2)
        title += "+{} ".format(len(added))
        print


    if removed:
        print "Removed:"
        for item in removed:
            print json.dumps(item, indent=2)
        title += "-{} ".format(len(removed))
        print

    with open('cache/title.txt', 'w') as out:
        out.write(title.strip())

    sys.exit(total)

if __name__ == '__main__':
    main()
