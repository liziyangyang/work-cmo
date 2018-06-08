#usr/bin/python
# coding = utf-8

import requests, sys, csv, os, codecs, re

reload(sys)
sys.setdefaultencoding("utf-8")

private_token = "JTj3jwSgxoYJHng36-ag"
project_namespace = sys.argv[1]
url = "http://192.168.31.76/api/v4/projects"
per_page = 20

def get_all_gitlab_data(api_url):
    page = 1
    all_data = []

    while True:
        full_url = api_url + str(page)
        result = requests.get(full_url)
        data = result.json()
        all_data = all_data + data
        if not data:
            break
        page = page + 1
    return all_data

#get all project data
project_url = url + "?private_token=" + private_token + "&per_page=" + str(per_page) + "&" + "page="
project_data = get_all_gitlab_data(project_url)

#get project id
def get_project_id(project_data, project_namespace):
    for i in project_data:
        if i[u'path_with_namespace'] == project_namespace:
            project_id = i[u'id']
            return project_id
    raise RuntimeError("project_id for " + project_namespace + "not found")
    
project_id = get_project_id(project_data, project_namespace)

#get all merge_requests data
merge_url = url + "/" + str(project_id) + "/merge_requests" + "?private_token=" + private_token + "&per_page=" + str(per_page) + "&" + "page="
merge_data = get_all_gitlab_data(merge_url)

def get_merge_data(merge_data):
    merge_dict = {}
    print len(merge_data)
    for i in range(len(merge_data)):
        req_data = {}
        req_data["iid"] = merge_data[i]["iid"]
        req_data["title"] = merge_data[i]["title"]
        req_data["state"] = merge_data[i]["state"]
        req_data["source_branch"] = merge_data[i]["source_branch"]
        req_data["target_branch"] = merge_data[i]["target_branch"]
        req_data["author"] = merge_data[i]["author"]["username"]
        if merge_data[i]["assignee"]:
            req_data["assignee"] = merge_data[i]["assignee"]["username"]
        else:
            req_data["assignee"] = "no one"
        req_data["created_at"] = merge_data[i]["created_at"]
        req_data["updated_at"] = merge_data[i]["updated_at"]
        iid = merge_data[i]["iid"]
        merge_dict[iid] = req_data
    return merge_dict

merge_dict = get_merge_data(merge_data)

    
def get_specific_comments(merge_dict):
    for iid in merge_dict:
    #get comments from specific merge_requests iid
        merge_iid_url = url + "/" + str(project_id) + "/merge_requests" + "/" + str(iid) + "/notes" + "?private_token=" + private_token + "&per_page=" + str(per_page) + "&" + "page="
        merge_iid_data = get_all_gitlab_data(merge_iid_url)

        merge_notes = []
        for i in range(len(merge_iid_data)):
            notes_data = {}
            notes_data["author"] = merge_iid_data[i]["author"]["username"]
            notes_data["comments"] = merge_iid_data[i]["body"]
            comment_str = notes_data["comments"]
            if not re.match("merged", comment_str) and not re.match("closed", comment_str) and not re.match("mentioned in commit", comment_str) and not re.match("added .+ commit", comment_str):
                merge_notes.append(notes_data)
        merge_dict[iid]["notes"] = merge_notes
    return merge_dict

def get_csv_data(new_merge_dict):
    csv_data = []
    for iid in new_merge_dict:
        csv_res = []
        csv_res.append(iid)
        csv_res.append(merge_dict[iid]["title"])
        csv_res.append(merge_dict[iid]["state"])
        csv_res.append(merge_dict[iid]["author"])
        csv_res.append(merge_dict[iid]["assignee"])
        csv_res.append(merge_dict[iid]["source_branch"])
        csv_res.append(merge_dict[iid]["target_branch"])
        notes = merge_dict[iid]["notes"]
        notes_ret = []
        for dic in notes:
            notes_ret.append(dic["author"] + ": " + dic["comments"])
        csv_res.append("\n".join(notes_ret))
        csv_res.append(merge_dict[iid]["created_at"])
        csv_res.append(merge_dict[iid]["updated_at"])
        csv_data.append(csv_res)
    return csv_data

new_merge_dict = get_specific_comments(merge_dict)

csv_data = get_csv_data(new_merge_dict)

print csv_data

def write_into_csv(csv_data):
    csvfile = os.path.join(os.getcwd(), "gitlab_review_report.csv")
    titles = ["merge_request ID", "title", "state", "author", "assignee", "source_branch", "target_branch", "comments", "created_at", "updated_at"]
    with open(csvfile, "wb") as f:
        f.write(codecs.BOM_UTF8)
        writer = csv.writer(f)
        writer.writerow(titles)
        writer.writerows(csv_data)

write_into_csv(csv_data)    
