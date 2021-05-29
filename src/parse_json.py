#!/usr/bin/python3
import json
#parse a string to json list and print error message if the input is not a valid
# json list


def parse_to_json(sample):
    sample = sample.replace("\n","");
    #format the string
    output = [];
    final_out = [];
    current = "";
    m = 0;
    l = 0;
    q = 1;
    # mark up the brackets and big parantheses
    for s in sample:
        #remove all unecessary blanks
        if s == "\"" and m == 0 and l == 0:
            q = q * -1
        if q == -1:
            current += s;
        else:
            if s ==" ":
                #check for numbers/string after numbers/string
                if current != "" and l ==0 and m == 0:
                    output.append(current);
                    current ="";
            elif s == '{':
                #check if we are going into a new json
                if l == 0 and m == 0 and current != "":
                    output.append(current);
                    current = "";
                l -= 1;
                current += s;
            elif s == '[':
                #check if we are going into a new json
                if l == 0 and m == 0 and current != "":
                    output.append(current);
                    current = "";
                m -= 1;
                current += s;
            elif s == '}':
                l += 1;
                current += s;
                #check whether the current json ends
                if l == 0 and m == 0:
                    output.append(current);
                    current = "";
            elif s == ']':
                m += 1;
                current += s;
                #check whether the current json ends
                if l == 0 and m == 0:
                    output.append(current);
                    current = "";
            else:
                current += s;
    #check for unclosing brackets or big parantheses
    if l != 0 or m != 0:
        final_out = None
    #add the remaining string
    elif current != "":
        output.append(current);
    try:
        #string list to json list
        for i in output:
            jsons = json.loads(i);
            final_out.append(jsons);
    except:
        final_out = None
    return final_out
