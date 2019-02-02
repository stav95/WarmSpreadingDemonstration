import random

def new_file():
    path = 'table.csv'
    file_table = open(path, 'w')
    file_table.write("ip_address,is_reachable,is_vulnerable,is_infected\n")
    file_table.close()
    generate_table(path)
    print ('Done!')


def generate_table(path):
    file_table = open(path, 'a')

    list_ip.append('1.1.1.1')

    file_list = []
    file_list.append('1.1.1.1,Y,Y,Y')

    for x1 in range(1, 255):
        for x2 in range(1, 3):
            for x3 in range(1, 255):
                for x4 in range(1, 255):
                    if random.randint(0, 1000) == 100:
                        file_list.append(generate_new_row(str.format("{0}.{1}.{2}.{3}", x1, x2, x3, x4)))

    file_table.write('\n'.join(file_list))
    file_table.close()


def generate_new_row(ip):
    is_reachable = is_reachable_random()
    return str.format("{0},{1},{2},N", ip, is_reachable, is_vulnerable_random(is_reachable))


def generate_ip():
    ip = str.format("{0}.{1}.{2}.{3}", r_int(1, 255), r_int(1, 255), r_int(1, 255), r_int(1, 255))

    if list_ip.__contains__(ip):
        return generate_ip()
    else:
        list_ip.append(ip)

    return list_ip[len(list_ip) - 1]


def is_reachable_random():
    if r_int(1, 5) == 1:
        return 'N'
    return 'Y'


def is_vulnerable_random(is_reachable):
    if is_reachable == 'N':
        return 'N'
    if r_int(1, 3) == 1:
        return 'N'
    return 'Y'


def r_int(x, y):
    return random.randint(x, y)


if __name__ == '__main__':
    global list_ip
    list_ip = []
    new_file()
