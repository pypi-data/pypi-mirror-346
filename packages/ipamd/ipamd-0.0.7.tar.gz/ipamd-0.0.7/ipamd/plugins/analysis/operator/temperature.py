from ipamd.public.constant import *
import numpy as np
def func(frame):
    prop = frame.properties(ignoring_image=False)
    molecules = prop['molecules']
    ek = 0
    freedom = 0
    for molecule in molecules:
        mass_list = molecule['mass']
        vel_list = molecule['velocity']
        n_atoms = len(mass_list)

        rigid_of_last_atom = -1
        for i in range(n_atoms):
            mass_kg = mass_list[i] / na / 1000
            velocity_m_s = [v * 1000 for v in vel_list[i]]

            ek += 0.5 * mass_kg * (velocity_m_s[0] ** 2 + velocity_m_s[1] ** 2 + velocity_m_s[2] ** 2)
            rigid = molecule['rigid_body'][i]
            if rigid == 0:
                if rigid_of_last_atom == -1:
                    freedom += 3
                    rigid_of_last_atom = 0
            else:
                if rigid_of_last_atom == 0:
                    freedom += 3
                    rigid_of_last_atom = -1
                freedom += 3


    temperature = 2 * ek / (freedom * kb)
    return temperature
#import os
#
#from ipamd.public.utils.output import error
#
#configure = {
#    "schema": "io"
#}
#def func(frame, working_dir, simulation):
#    frame_no = frame.no
#    simulation_name = simulation.job_name
#    log_file = os.path.join(working_dir, simulation_name + '.log')
#    with open(log_file, 'r') as f:
#        lines = f.readlines()[1:]
#    time_step = frame_no * simulation.period
#    data = {}
#    for line in lines:
#        time_step_of_line = float(line.split()[0])
#        if time_step_of_line == time_step:
#            data = float(line.split()[3])
#    if data == {}:
#        error('simulation should be run first')
#        raise NotImplementedError
#    return data