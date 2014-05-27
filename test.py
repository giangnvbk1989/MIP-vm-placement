import json
from physical_configuration import PhysicalConfig
from MIP_rack_interface import migrate_policy

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

def compute_traffic(num_vms, traffic, placement, test_config):
    link_traffic = [0 for k in range(test_config.num_links)]

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
    test_case = fake_input("test1.in")

    config = test_case['physical_config']

    print 'num_vms', test_case['num_servers']
    print 'num_racks', config.num_racks
    print 'num_servers', config.num_servers

    print compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)

    for k in range(1):
        c = 24
    
        operations = migrate_policy(test_case['num_servers'], test_case['vm_consume'], test_case['vm_matrix'], test_case['original_placement'], config, c, [], cost_migration = [])

        #link_traffic = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)
        #print "before migration:", link_traffic
        new_placement = test_case['original_placement'][:]
        for migration in operations:
            new_placement[migration[0]] = migration[1]
    
        traffic, max_value, index = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], new_placement, config)

        print "c:", c, "migration", len(operations), "max:", max_value, "link", index
        print traffic






def test_1():
    test_case = fake_input("test1.in")

    config = test_case['physical_config']

    print 'num_vms', test_case['num_servers']
    print 'num_racks', config.num_racks
    print 'num_servers', config.num_servers

    print compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)

    for k in range(10):
        c = (k+1)*3
    
        operations = migrate_policy(test_case['num_servers'], test_case['vm_consume'], test_case['vm_matrix'], test_case['original_placement'], config, c, [], cost_migration = [])

        #link_traffic = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], test_case['original_placement'], config)
        #print "before migration:", link_traffic
        new_placement = test_case['original_placement'][:]
        for migration in operations:
            new_placement[migration[0]] = migration[1]
    
        traffic, max_value, index = compute_traffic(test_case['num_servers'], test_case['vm_matrix'], new_placement, config)

        print "c:", c, "migration", len(operations), "max:", max_value, "link", index
        #print traffic


        #print "after migration:", link_traffic
        #print "which rack", config.which_rack
    

if __name__ == '__main__':
    test_0()






g
