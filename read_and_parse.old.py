import linecache

if __name__ == "__main__":
    txt_file = open("./json_results/Androbugs/8657024da129fc6982f9daa7f3775cf6.txt", "r")
    lines = txt_file.readlines()
    line_counter = 1
    critical = []
    warning = []
    notice = []
    info = []
    for line in lines:
        if line.startswith("[Critical]") or line.startswith("[Warning]") or line.startswith("[Notice]") or line.startswith("[Info]"):
            if line.startswith("[Critical]"):
                critical.append(line_counter)
            if line.startswith("[Warning]"):
                warning.append(line_counter)
            if line.startswith("[Notice]"):
                notice.append(line_counter)
            if line.startswith("[Info]"):
                info.append(line_counter)
            line_counter = line_counter + 1
        else:
            line_counter = line_counter + 1

    print(critical)
    print(warning)
    print(notice)
    print(info)

    #now let's try to put everything on a JSON format :-)
    json_file = open("./json_results/Androbugs/8657024da129fc6982f9daa7f3775cf6.json", "w")
    json_file.write("{")
    json_file.write("\"results\": {")
    json_file.write("\"critical_level\": [")
    for critical_line in critical:
        whatline = linecache.getline("./json_results/Androbugs/8657024da129fc6982f9daa7f3775cf6.txt", critical_line)
        json_file.write("{\"critical\": \"" + whatline[:-1] + "\"},")
    json_file.write("]")
    json_file.write("}")
    json_file.write("}")


