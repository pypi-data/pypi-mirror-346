from ipamd.public.utils.output import error, warning
import random
import numpy as np
import math

configure = {
    'attr': {
        'target': 'multi'
    }
}
def func(frames, type_='', sub=1):
    if type(frames) is not list:
        frames = [frames]

    n_frames = len(frames)
    if n_frames <= 5:
        warning("Small number of frames may lead to inaccurate results.")
    n_list = []
    r_list = []
    molecule_length = 0

    for frame in frames:
        prop = frame.properties(ignoring_image=True)
        molecules = prop['molecules']
        if type_ == '':
            type_ = molecules[0]['molecule_type']
        for molecule in molecules:
            if molecule['molecule_type'] == type_:
                molecule_length = molecule['n_atoms']
                if molecule_length < 30:
                    error('Molecule too small')
                    return -1
                max_length = molecule_length
                sampling_times = int(math.pow(math.log(molecule_length), 2)  * sub)
                for j in range(sampling_times):
                    nums = np.arange(10, max_length + 1)
                    weight = np.linspace(10, max_length + 1, max_length - 9)
                    weight = np.divide(1, weight)
                    target_length = np.random.choice(nums, p=weight / np.sum(weight))
                    start_index = random.randint(0, molecule_length - target_length)
                    end_index = start_index + target_length - 1
                    total_mass = 0
                    p_m = np.array([0, 0, 0], dtype=float)
                    for i in range(start_index, end_index + 1):
                        total_mass += molecule['mass'][i]
                        p_m += molecule['mass'][i] * np.array(molecule['position'][i])
                    p_m /= total_mass

                    r2_m = 0
                    for i in range(start_index, end_index + 1):
                        distance2 = np.linalg.norm(np.array(molecule['position'][i]) - p_m) ** 2
                        r2_m += distance2 * molecule['mass'][i]
                    rg2 = r2_m / total_mass
                    n_list.append(math.log(target_length))
                    r_list.append(math.log(rg2)/2)
    sorted_index = np.argsort(n_list)
    n_list = np.array(n_list)[sorted_index]
    r_list = np.array(r_list)[sorted_index]
    max_log_length = math.log(molecule_length)
    t = max_log_length * 2 / 3
    split_index = np.searchsorted(n_list, t, side='right')
    sub_n_list = n_list[:int(split_index)]
    sub_r_list = r_list[:int(split_index)]
    A = np.vstack([sub_n_list, np.ones(len(sub_n_list))]).T
    m, b = np.linalg.lstsq(A, sub_r_list, rcond=None)[0]
    ln_kuhn_length = b
    A = np.vstack([n_list, np.ones(len(n_list))]).T
    m, b = np.linalg.lstsq(A, r_list, rcond=None)[0]
    if m > 0.53:
        return m
    else:
        end_points_ln_r = r_list[-5:]
        ln_r_full_molecule = np.average(end_points_ln_r)
        v = (ln_r_full_molecule - ln_kuhn_length) / max_log_length
        return v
