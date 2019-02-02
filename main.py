import csv
import random
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from enum import Enum


class MachineRow:
    ip_address = None
    is_reachable = None
    is_vulnerable = None
    is_infected = None
    state = None
    timer = None
    target = None

    def __init__(self, row):
        self.ip_address = row[0]
        self.is_reachable = row[1]
        self.is_vulnerable = row[2]
        self.is_infected = row[3]
        self.state = State.idle
        self.timer = 0
        self.target = 0

        if self.is_vulnerable == 'Y':
            global vulnerable_counter
            vulnerable_counter += 1

    def move_forward_with_attack(self, tar):
        global b, c
        if tar.state == State.access:
            if tar.is_reachable == 'N':
                tar.state = State.idle
                self.state = State.idle
                self.target = -1
                self.timer = 0
            elif tar.is_reachable == 'Y':
                tar.state = State.vulnerable
                self.timer = b
        elif tar.state == State.vulnerable:
            if tar.is_vulnerable == 'N':
                tar.state = State.idle
                self.state = State.idle
                self.target = -1
                self.timer = 0
            elif tar.is_vulnerable == 'Y':
                tar.state = State.infected
                self.timer = c
        elif tar.state == State.infected:
            tar.state = State.idle
            self.state = State.idle
            self.timer = 0
            if tar.is_infected == 'N':
                tar.is_infected = 'Y'
                return True

        return False

    def print_all(self):
        print str.format('ip: {0},reach: {1},vulner: {2},infe: {3},state: {4},timer: {5},target: {6}',
                         self.ip_address,
                         self.is_reachable,
                         self.is_vulnerable,
                         self.is_infected,
                         self.state,
                         self.timer,
                         self.target)


class State(Enum):
    idle = 1
    access = 2
    vulnerable = 3
    infected = 4
    attacking = 5


def main():
    global a, b, c, time, vulnerable_counter, infected_counter, infected_list
    time = 0
    vulnerable_counter = 0
    infected_counter = 0
    infected_list = []

    parser = ArgumentParser()
    parser.add_argument('--f', type=str, help="File Name, (e.g ips.cvs)")
    parser.add_argument('--a', type=int, help="a Value")
    parser.add_argument('--b', type=int, help="b Value")
    parser.add_argument('--c', type=int, help="c Value")
    args = parser.parse_args()

    file_csv = args.f
    a = args.a
    b = args.b
    c = args.c

    load_machine_state(file_csv)
    start_attack()
    create_graph()


def load_machine_state(file_csv):
    global table, vulnerable_counter
    table = []
    read_csv(file_csv)
    infected_list.append(0)
    vulnerable_counter -= 1


def read_csv(file_csv):
    with open(file_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                table.append(MachineRow(row))
                line_count += 1


def start_attack():
    global table, time, vulnerable_counter, infected_counter, a, b, c, graph_x, graph_y
    graph_x = []
    graph_y = []

    while vulnerable_counter != infected_counter:
        time += 1
        print str.format('{0}, {1}/{2}', time, infected_counter, vulnerable_counter)
        for x in infected_list:
            if table[x].state == State.attacking:
                if table[x].timer == 0:
                    if table[x].move_forward_with_attack(table[table[x].target]):
                        graph_y.append(infected_counter)
                        graph_x.append(time)
                        add_n = int(table[x].target)
                        infected_list.append(add_n)
                        infected_counter += 1
                    continue
                table[x].timer -= 1
                continue

            n = get_random_machine(x, len(table))

            if table[n].state == State.idle:
                table[n].state = State.access
                table[x].state = State.attacking
                table[x].timer = a
                table[x].target = n
    print str.format('vulnerable_counter: {0}/{1}, {2}', vulnerable_counter, infected_counter, time)


def get_random_machine(current, len_table):
    n = r_int(0, len_table - 1)
    while n == current:
        n = r_int(0, len_table - 1)
    return n


def r_int(x, y):
    return random.randint(x, y)


def create_graph():
    global a, b, c, time, vulnerable_counter, infected_counter
    fig, ax = plt.subplots()
    ax.plot(graph_x, graph_y)

    ax.set(xlabel='Time', ylabel='Infected',
           title=str.format('Total Machines: {0}, Vulnerable: {1}, Infected: {2}'
                            '\na: {3}, b: {4}, c: {5}, Total time: {6}',
                            len(table),
                            vulnerable_counter,
                            infected_counter,
                            a, b, c,
                            time))
    ax.grid()

    fig.savefig(str.format('a{0}_b{1}_c{2}.png', a, b, c))
    plt.show()


if __name__ == '__main__':
    main()
