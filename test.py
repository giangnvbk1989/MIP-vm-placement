import json
from physical_configuration import PhysicalConfig
from naive_strategy import migrate_policy
import copy
import time

def fake_input(file_name):
    # input
    file = open(file_name, "r")
    input = file.read().split('\n')
    fake_input = {}
    fake_input['num_servers'] = int(json.loads(input[0]))
    fake_input['vm_consume'] = json.loads(input[1])
    fake_input['vm_matrix'] = json.loads(input[2])
    fake_input['original_placement'] = json.loads(input[3])
    for i in range(fake_input['num_servers']):
        for j in range(3):
            fake_input['vm_consume'][i][j] = int(fake_input['vm_consume'][i][j])
    
    fake_input['original_placement'][i] = int(fake_input['original_placement'][i])
    for j in range(fake_input['num_servers']):
        fake_input['vm_matrix'][i][j] = long(fake_input['vm_matrix'][i][j])

    num_hosts = int(json.loads(input[4]))
    num_racks = int(json.loads(input[5]))
    num_links = int(json.loads(input[6]))
    host_to_rack = json.loads(input[7])
    cpu_constraint = json.loads(input[8])
    memory_constraint = json.loads(input[9])
    disk_constraint = json.loads(input[10])
    link_capacity = json.loads(input[11])
    for i in range(num_hosts):
        host_to_rack[i] = int(host_to_rack[i])
        cpu_constraint[i] = int(cpu_constraint[i])
        memory_constraint[i] = int(memory_constraint[i])
        disk_constraint[i] = int(disk_constraint[i])
    for i in range(num_links):
        link_capacity[i] = long(link_capacity[i])

    fake_input['physical_config'] = PhysicalConfig(num_servers = num_hosts, num_racks = num_racks, num_links = num_links,
    which_rack = host_to_rack,
    constraint_cpu = cpu_constraint,
    constraint_memory = memory_constraint,
    constraint_disk = disk_constraint,
    link_capacity = link_capacity)
    return fake_input


def compute_traffic(num_vms, traffic_matrix, placement, test_config):
    link_traffic = [0 for k in range(test_config.num_links)]

    traffic = [[0 for i in range(num_vms)] for k in range(num_vms)]
    
    for k in range(num_vms):
        for i in range(num_vms):
            traffic[k][i] = traffic_matrix[k][i] + traffic_matrix[i][k]

    for p in range(num_vms):
        for q in range(p+1, num_vms):
            rack_p, rack_q = test_config.which_rack[placement[p]], test_config.which_rack[placement[q]]
            if rack_p == rack_q:
                continue
            link_traffic[rack_p] += traffic[p][q]
            link_traffic[rack_q] += traffic[q][p]

    maximum = max(link_traffic)
    
    return link_traffic, maximum, link_traffic.index(maximum)


def test_0():
    test_case = fake_input("test3.in")

    config = test_case['physical_config']

    print 'num_vms', test_case['num_servers']
    print 'num_racks', config.num_racks
    print 'num_servers', config.num_servers

    matrix = copy.deepcopy(test_case['vm_matrix'])


    print compute_traffic(test_case['num_servers'], matrix, test_case['original_placement'], config)

    timer = 0

    for k in range(3):
        c = 18
    
        cost = [1 for k in range(test_case['num_servers'])]
        
        time_point = time.clock()
        print "clock1:%s" % time_point
        operations = migrate_policy(test_case['num_servers'], test_case['vm_consume'], test_case['vm_matrix'], test_case['original_placement'], config, c, [], cost_migration = cost)
        how_long = time.clock()
        print "clock2:%s" % how_long
        timer += how_long - time_point
        



        link_traffic, aaa, bbb = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)
        print "before migration:", sorted(link_traffic, reverse = True)
        new_placement = test_case['original_placement'][:]
        for migration in operations:
            new_placement[migration[0]] = migration[1]
    
        traffic, max_value, index = compute_traffic(test_case['num_servers'], matrix, new_placement, config)

        print "c:", c, "migration", len(operations), "max:", max_value, "link", index
        print sorted(traffic, reverse = True)

        print (aaa-max_value)*1.0/aaa

    print timer/3.0



def test_naive():
    test_case = fake_input("test3.in")

    config = test_case['physical_config']

    c = 18

    operations = migrate_policy(test_case['num_servers'], test_case['vm_consume'], test_case['vm_matrix'], test_case['original_placement'], config, c, [], cost_migration = [], steady_ratio = 0.02)




def test_1():
    test_case = fake_input("test3.in")

    config = test_case['physical_config']

    print 'num_vms', test_case['num_servers']
    print 'num_racks', config.num_racks
    print 'num_servers', config.num_servers

    print compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)

    new_placement = test_case['original_placement'][:]

    for k in range(7):
        c = 18

        cost = [100 for k in range(test_case['num_servers'])]
    
        operations = migrate_policy(test_case['num_servers'], test_case['vm_consume'], test_case['vm_matrix'], new_placement, config, c, [], cost_migration = [], steady_ratio = 0.02)

        #link_traffic = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)
        #print "before migration:", link_traffic
        for migration in operations:
            new_placement[migration[0]] = migration[1]
    
        traffic, max_value, index = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], new_placement, config)

        print "c:", c, "migration", len(operations), "max:", max_value, "link", index
        #print traffic


        #print "after migration:", link_traffic
        #print "which rack", config.which_rack
    

if __name__ == '__main__':
    test_naive()
