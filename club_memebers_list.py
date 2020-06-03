import datetime
import json

from db import check_club

now = datetime.datetime.now()

current_users_list = check_club()

members_list = []
for i in range(len(current_users_list)):
    members_list.append(current_users_list[i][1])


def unique_users(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

name_of_the_file = 'club_file_{}_{}.txt'.format(now.date(), now.time())
list_to_write = unique_users(members_list)
with open(name_of_the_file, 'w') as f:
    f.write(json.dumps(list_to_write))


print("file_created")
print(name_of_the_file)