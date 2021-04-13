#%%

import json

dev = False
old_version = "3.13"
new_version = "3.14"


def parse_string(string):
    string = string.replace("\u2019", "'")
    return string


def compare_nodes_name(old_node, new_node):
    return parse_string(old_node["name"]) == parse_string(new_node["name"])


def compare_nodes_stats(old_node, new_node):
    old_stats = old_node["stats"]
    new_stats = new_node["stats"]
    if len(old_stats) != len(new_stats):
        return False

    def loop(stats, other_stats):
        for stat in stats:
            stat = parse_string(stat)
            found = False
            for other_stat in other_stats:
                other_stat = parse_string(other_stat)
                if stat == other_stat:
                    found = True
                    break
            if not found:
                return False
        return True

    if not loop(old_stats, new_stats) or not loop(new_stats, old_stats):
        return False
    return True


def compare_nodes(old_node, new_node):
    if not compare_nodes_name(old_node, new_node):
        return False
    if not compare_nodes_stats(old_node, new_node):
        return False
    return True


def get_node_sprite(node, patch):
    icon = node["icon"]
    filename = "skills-3.jpg"
    if "isNotable" in node:
        cat = "notableActive"
    elif "isKeystone" in node:
        cat = "keystoneActive"
    elif "isMastery" in node:
        cat = "mastery"
        filename = "groups-3.png"
    else:
        cat = "normalActive"
    filecat = next(
        x for x in patch["skillSprites"][cat] if x["filename"].startswith(filename)
    )
    return {"filename": filename, "coords": filecat["coords"][icon]}


def write_node(node, patch):
    parsed = {"node": node["skill"], "name": node["name"], "stats": node["stats"]}
    if "reminderText" in node:
        parsed["reminder"] = node["reminderText"]
    parsed["sprite"] = get_node_sprite(node, patch)
    if "isMastery" in node:
        parsed["mastery"] = True
    if "isKeystone" in node:
        parsed["keystone"] = True
    return parsed


def compare_patches(old_patch, new_patch):
    modified = []
    added = []
    removed = []
    old_nodes = old_patch["nodes"]
    new_nodes = new_patch["nodes"]
    for index, old_node in old_nodes.items():
        if not index in new_nodes:
            removed.append(write_node(old_node, old_patch))
        else:
            new_node = new_nodes[index]
            if not compare_nodes(old_node, new_node):
                modified.append(
                    {
                        "old": write_node(old_node, old_patch),
                        "new": write_node(new_node, new_patch),
                    }
                )
    for index, new_node in new_nodes.items():
        if not index in old_nodes:
            added.append(write_node(new_node, new_patch))
    return {"modified": modified, "added": added, "removed": removed}


def read_patch(version):
    with open(f"data/{version}/data.json") as patch_file:
        patch = json.load(patch_file)
        patch["nodes"].pop("root", None)
        patch["version"] = version
        return patch


def main():
    old_patch = read_patch(old_version)
    new_patch = read_patch(new_version)
    result = compare_patches(old_patch, new_patch)
    result["old"] = old_version
    result["new"] = new_version
    with open("data.js", "w") as parsed_file:
        if dev:
            data = json.dumps(result, indent=4)
        else:
            data = json.dumps(result)
        parsed_file.write(f"const data = {data}")


if __name__ == "__main__":
    main()

# %%
