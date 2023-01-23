import os
import sys
import yaml

sys.path.append('')

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

import ttkbootstrap as ttkB
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.themes import user
from ttkbootstrap.tooltip import ToolTip as hinty

from ftfy import fix_text as fxy

from neu_tools.nttkb_util import *
from neu_tools.neudiff import *

def verify_setup():
	if os.path.exists('checkpoints'):
		print('Checkpoints OK!')
	else:
		print('Checkpoints are missing. Please check checkpoints folder!')
		sys.exit()

class diff_inf():

	def __init__(self):
		super().__init__()

		verify_setup()

		lang_dict = yaml_dict('lang_str') #Loads the nested dictionary of strings for the program
		cfg_dict = yaml_dict('gui_cfg')

		root = ttkB.Window(themename='diff-dark')
		main_window(root, lang_dict, cfg_dict)

def info_window(sgr_dir_var, d_, l_):

	infr = ttkB.Toplevel()
	infr.iconbitmap('img/neu.ico')
	infr.title(fxy(d_[l_]['info_title']))

	if os.path.exists(sgr_dir_var):
		for file in os.listdir(sgr_dir_var):
			if file.endswith('.ckpt'):
				pass
			elif file.endswith('.yaml'):
				x, singer_cfg = model_get(sgr_dir_var)
				with open(singer_cfg, 'r') as cfg:
					info_d = yaml.safe_load(cfg)
			else:
				infr.destroy()
				Messagebox.show_error(
					message=fxy(d_[l_]['model_load_error']),
					title=fxy(d_[l_]['model_load_error_title']),
					alert=True)
				break
	

		i_ = ttkB.Frame(master=infr, pad=5)
		i_.pack()

		data = [
			(fxy(d_[l_]['info_hz']), fxy(str(info_d['audio_sample_rate'])))
			]

		tv = ttkB.Treeview(
			master=i_, columns=[0, 1], show=HEADINGS, height=1)

		for row in data:
			tv.insert('', END, values=row)

		tv.selection_set('I001')
		tv.heading(0, text=fxy(d_[l_]['info_lbl']))
		tv.heading(1, text=fxy(info_d['speaker_id']))
		tv.column(0, width=100, anchor='center')
		tv.column(1, width=100, anchor='center')
		tv.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
	else:
		infr.destroy()
		Messagebox.show_error(
			message=fxy(d_[l_]['model_load_error']),
			title=fxy(d_[l_]['model_load_error_title']),
			alert=True)


def main_window(root, d_, cfg_dict):

	#priority variables

	l_ = cfg_dict['display_language']

	def open_model_dir():
		sgr_dir_var.set(askdirectory(
			title=fxy(d_[l_]['directory_ask']),
			initialdir=os.getcwd()
			))

	def open_wav_file():
		wav_dir_var.set(askopenfilename(
			title=fxy(d_[l_]['wav_file_ask']), 
			initialdir=os.getcwd(),
			filetypes={('wav files', '*.wav', 'WAVE')}
			))

	def export_wav_file():
		wav_gen_var.set(asksaveasfilename(
			title=fxy(d_[l_]['wav_save_ask']),
			initialdir=os.getcwd(),
			filetypes={('wav files', '*.wav', 'WAVE')}
			))

	def run_svc():
		r_dict = r_dict_gen('null',
							key_var.get(),
							pndm_var.get(),
							crepe_var.get(),
							pe_var.get(),
							thre_var.get(),
							gt_mel_var.get(),
							noise_var.get())

		diffuse(sgr_dir_var.get(),
				wav_dir_var.get(),
				r_dict,
				wav_gen_var.get()
				)
		
	#root.geometry(center(root, 525, 300))
	root.eval('tk::PlaceWindow . center')
	root.iconbitmap('img/neu.ico')
	root.title(fxy(d_[l_]['title']))

	##           ##
	## VARIABLES ##
	##			 ##

	key_var = IntVar() #Variable for Keyshift (Default: 0)
	pndm_var = IntVar() #Variable for pndm_speedup. 0-20 (Default: 20? I have it set to 0)
	crepe_var = BooleanVar() #Variable for use_crepe (Default: True)
	pe_var = BooleanVar() #Variable for use_pe (Default: True)
	thre_var = DoubleVar() #variable for thre (Default: 0.05)
	gt_mel_var = BooleanVar() #variable for use_gt_mel (Default: False)
	noise_var = IntVar() #Variable for add_noise_step (Default: 500)

	key_var.set(0)
	pndm_var.set(0)
	crepe_var.set(True)
	pe_var.set(True)
	thre_var.set(0.05)
	gt_mel_var.set(False)
	noise_var.set(500)

	##						   ##
	##	BEGIN UI - MAIN FRAME  ##
	##						   ##

	m_ = ttkB.Frame(master=root, pad=5, width=525, height=275)
	m_.pack(fill=Y, expand=False)

	##	  		      ##
	##	Entry Layout  ##
	##			      ##

	#singer selection

	#label for singer directory
	sgr_dir_lbl = ttkB.Label(
		master=m_, text=fxy(d_[l_]['sgr_dir'])
		)
	sgr_dir_lbl.grid(row=0, column=0, padx=5, pady=5, sticky='e')

	#Entry line for singer directory
	sgr_dir_var = StringVar()
	sgr_dir_var.set(fxy(d_[l_]['sgr_dir_des']))

	sgr_dir_sel = ttkB.Entry(
		master=m_, textvariable=sgr_dir_var, width=39, state='disabled'
		)
	sgr_dir_sel.grid(row=0, column=1, padx=5, pady=5, sticky='e')

	#singer directory browse button
	sgr_dir_btn = ttkB.Button(
		master=m_, text=fxy(d_[l_]['browse']), width=9, command=open_model_dir
		)
	sgr_dir_btn.grid(row=0, column=2, padx=5, pady=5, sticky='w')

	#audio selection

	#audio selection label
	wav_dir_lbl = ttkB.Label(
		master=m_, text=(fxy(d_[l_]['wav_dir']))
		)
	wav_dir_lbl.grid(row=1, column=0, padx=5, pady=5, sticky='e')

	#audio selection entry field
	wav_dir_var = StringVar()
	wav_dir_var.set(fxy(d_[l_]['wav_dir_des']))

	wav_dir_sel = ttkB.Entry(
		master=m_, textvariable=wav_dir_var, width=39, state='disabled'
		)
	wav_dir_sel.grid(row=1, column=1, padx=5, pady=5, sticky='e')

	#audio selection browse button
	wav_dir_btn = ttkB.Button(
		master=m_, text=fxy(d_[l_]['browse']), width=9, command=open_wav_file
		)
	wav_dir_btn.grid(row=1, column=2, padx=5, pady=5, sticky='w')

	#audio export

	#audio export label
	wav_gen_lbl = ttkB.Label(
		master=m_, text=(fxy(d_[l_]['wav_exp']))
		)
	wav_gen_lbl.grid(row=2, column=0, padx=5, pady=5, sticky='e')

	#audio export entry field
	wav_gen_var = StringVar()
	wav_gen_var.set(fxy(d_[l_]['wav_exp_hint']))

	wav_gen_sel = ttkB.Entry(
		master=m_, textvariable=wav_gen_var, width=39, state='disabled'
		)
	wav_gen_sel.grid(row=2, column=1, padx=5, pady=5, sticky='e')

	#audio export browse button
	wav_gen_btn = ttkB.Button(
		master=m_, text=fxy(d_[l_]['browse']), width=9, command=export_wav_file
		)
	wav_gen_btn.grid(row=2, column=2, padx=5, pady=5, sticky='w')

	##	  		         ##
	##	Parameter Frame  ##
	##			         ##

	nb_ = ttkB.Notebook(
		master=m_, padding=5
		)
	nb_.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

	param_fr_m = ttkB.Frame(
		master=nb_)
	nb_.add(param_fr_m, text=fxy(d_[l_]['parameter']))

	adv_param_fr = ttkB.Frame(
		master=nb_)
	nb_.add(adv_param_fr, text=fxy(d_[l_]['adv_parameter']))

	#keyshift label
	key_sh_lbl = ttkB.Label(
		master=param_fr_m, text=fxy(d_[l_]['keyshift'])
		)
	key_sh_lbl.pack(padx=5, pady=5, side=LEFT)
	
	#keyshift spinbox. variable=key_var
	key_sh_spin = ttkB.Spinbox(
		master=param_fr_m, textvariable=key_var, from_=-24, to=24, width=4
		)
	key_sh_spin.bind('<Key>', verify_int)
	key_sh_spin.pack(padx=5, pady=5, side=LEFT)

	#keyshift tooltip loop
	key_sh_tlist = [key_sh_lbl, key_sh_spin]
	for x in key_sh_tlist:
		hinty(x, text=fxy(d_[l_]['keyshift_hint']), delay=350, bootstyle=PRIMARY)

	#pndmspeedup label
	pndm_lbl = ttkB.Label(
		master=param_fr_m, text=fxy(d_[l_]['pndm_lbl'])
		)
	pndm_lbl.pack(padx=5, pady=5, side=LEFT)

	#pndm_speedup spinbox. variable=pndm_var
	pndm_spin = ttkB.Spinbox(
		master=param_fr_m, textvariable=pndm_var, from_=0, to=20, width=4
		)
	pndm_spin.bind('<Key>', verify_int)
	pndm_spin.pack(padx=5, pady=5, side=LEFT)

	#pndm_speedup tooltip loop
	pndm_tlist = [pndm_lbl, pndm_spin]
	for x in pndm_tlist:
		hinty(x, text=fxy(d_[l_]['pndm_hint']), delay=350, bootstyle=PRIMARY)

	#use_crepe check. variable=crepe_var
	crepe_ch = ttkB.Checkbutton(
		param_fr_m, text=fxy(d_[l_]['crepe_lbl']), style='Roundtoggle.Toolbutton',
		variable=crepe_var, onvalue=True, offvalue=False)
	crepe_ch.pack(padx=5, pady=5, side=LEFT)

	hinty(crepe_ch, text=fxy(d_[l_]['crepe_hint']), delay=350, bootstyle=PRIMARY)

	###						###
	### Advanced Parameters ###
	###						###

	#thre label
	thre_lbl = ttkB.Label(
		master=adv_param_fr, text=fxy(d_[l_]['thre_lbl'])
		)
	thre_lbl.pack(padx=5, pady=5, side=LEFT)
	
	#thre spinbox. variable=thre_var
	thre_spin = ttkB.Spinbox(
		master=adv_param_fr, textvariable=thre_var, from_=0.00, to=1.00, 
		width=4, format='%.2f', increment=0.01
		)
	thre_spin.bind('<Key>', verify_float)
	thre_spin.pack(padx=5, pady=5, side=LEFT)

	#thre tooltip loop
	thre_tlist = [thre_lbl, thre_spin]
	for x in thre_tlist:
		hinty(x, text=fxy(d_[l_]['thre_hint']), delay=350, bootstyle=PRIMARY)

	#use_pe
	pe_ch = ttkB.Checkbutton(
		adv_param_fr, text=fxy(d_[l_]['pe_lbl']), style='Roundtoggle.Toolbutton',
		variable=pe_var, onvalue=True, offvalue=False)
	pe_ch.pack(padx=5, pady=5, side=LEFT)

	#use_pe tooltip
	hinty(pe_ch, text=fxy(d_[l_]['pe_hint']), delay=350, bootstyle=PRIMARY)

	#use_gt_mel
	gt_ch = ttkB.Checkbutton(
		adv_param_fr, text=fxy(d_[l_]['gtm_lbl']), style='Roundtoggle.Toolbutton',
		variable=gt_mel_var, onvalue=True, offvalue=False)
	gt_ch.pack(padx=5, pady=5, side=LEFT)

	#use_gt_mel tooltip
	hinty(gt_ch, text=fxy(d_[l_]['gtm_hint']), delay=350, bootstyle=PRIMARY)

	#add_noise_step label
	noise_lbl = ttkB.Label(
		master=adv_param_fr, text=fxy(d_[l_]['noise_lbl'])
		)
	noise_lbl.pack(padx=5, pady=5, side=LEFT)

	#add_noise_step. variable=noise_var
	noise_spin = ttkB.Spinbox(
		master=adv_param_fr, textvariable=noise_var, from_=1, to=1000, width=4
		)
	noise_spin.bind('<Key>', verify_int)
	noise_spin.pack(padx=5, pady=5, side=LEFT)

	#add_noise_step tooltip loop
	noise_tlist = [noise_lbl, noise_spin]
	for x in noise_tlist:
		hinty(x, text=fxy(d_[l_]['noise_hint']), delay=350, bootstyle=PRIMARY)

	###								  ###
	### Bottom Choices/Render Buttons ###
	###								  ###

	#model info window button
	abt_model_btn = ttkB.Button(
		master=m_, text=fxy(d_[l_]['model_info']), width=12, command=lambda: info_window(sgr_dir_var.get(), d_, l_)
		)
	abt_model_btn.grid(row=4, column=0, padx=5, pady=5, sticky='e')

	#render button
	render_btn = ttkB.Button(
		master=m_, text=fxy(d_[l_]['render']), width=9, command=run_svc
		)
	render_btn.grid(row=4, column=2, padx=5, pady=5, sticky='w')

	root.resizable(False, False)
	root.mainloop()

def run_app():
	app = diff_inf()

if __name__ == '__main__':
	run_app()