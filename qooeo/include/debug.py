import json

#===============================================================================
# save_tmp_file
#===============================================================================
def save_tmp_file(file_name, result):
    output_file = open(file_name, "w")
    if type(result) == list:
        for row in result:
            output_file.write(str(row) + "\n")
    else:
        keys = sorted(result.keys())
        for key in keys:
            if type(result[key]) == "int":
                tmp_line = "%s,%s\n" % (str(key), str(result[key]))
            if type(result[key]) == "str":
                tmp_line = "%s,%s\n" % (str(key), str(result[key]))
            else:
                tmp_line = str(key) + json.dumps(result[key]) + "\n"
            output_file.write(tmp_line)
        output_file.close()

