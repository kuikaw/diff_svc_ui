import os
import glob
import sys

from infer_tools.infer_tool import Svc
from infer import run_clip

def r_dict_gen(project_name, key_shift, pndm_speedup, use_crepe, use_pe, thre, use_gt_mel, add_noise_step):
    return {
        'project_name': project_name,
        'key_shift': key_shift,
        'pndm_speedup': pndm_speedup,
        'use_crepe': use_crepe,
        'use_pe': use_pe,
        'thre': thre,
        'use_gt_mel': use_gt_mel,
        'add_noise_step': add_noise_step,
    }

def model_get(singer_dir):

    model_list = []

    for file in os.listdir(singer_dir):
        if file.endswith('.ckpt'):
            model_list.append(os.path.join(singer_dir, file))
        elif file.endswith('.yaml'):
            singer_cfg = os.path.join(singer_dir, file)
    singer_model = max(model_list, key=os.path.getmtime)

    if singer_model=='' or singer_cfg=='':
        print('Error: Missing either singer model or configuration, check folder!')

    return singer_model, singer_cfg

def diffuse(singer_dir, wav_fn, r_dict, wav_gen):

    singer_model, singer_cfg = model_get(singer_dir)

    if not wav_gen.endswith('.wav'):
        wav_gen += '.wav'

    svc_model = Svc(r_dict['project_name'], singer_cfg, True, singer_model)

    f0_tst, f0_pred, audio = run_clip(svc_model,
                                    file_path=wav_fn, 
                                    key=r_dict['key_shift'], 
                                    acc=r_dict['pndm_speedup'], 
                                    use_crepe=r_dict['use_crepe'], 
                                    use_pe=r_dict['use_pe'], 
                                    thre=r_dict['thre'],
                                    use_gt_mel=r_dict['use_gt_mel'], 
                                    add_noise_step=r_dict['add_noise_step'],
                                    project_name=r_dict['project_name'],
                                    out_path=wav_gen)
