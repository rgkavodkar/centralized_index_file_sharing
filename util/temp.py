__author__ = 'rg.kavodkar'


file_name = "D:\\rfcs\\rfc7402.txt"
fileobject = open(file_name, "r")

empty_block = False
empty_block_count = 0

rfc_number = 0
interested_string = ""


for line in fileobject:
    if empty_block_count > 2:
        break
    if line.strip() == "":
        if not empty_block:
            empty_block_count += 1
            empty_block = True
        continue
    else:
        empty_block = False
        if "Request for Comments:" in line:
            print("RFC LINE")
            rfc_number = line.split(" ")[3]

        if empty_block_count == 2:
            interested_string += " " + line.strip()


print("RFC number: ", rfc_number)
print("interested_string: ", interested_string)

