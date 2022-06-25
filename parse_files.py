# -*- coding: utf-8 -*-
# @Author: Meshack Mwaura
# @Date:   2022-02-28 09:44:11
# @Last Modified by:   Meshack Mwaura
# @Last Modified time: 2022-03-02 11:01:14

import os
from datetime import datetime
from local import *
# Ignore reading variables from .env
# TODO: looking for alternative installations on Debian 10.2
# from dotenv import load_dotenv
# # Load environment settings 

# load_dotenv()

# cdr_incoming = os.getenv('cdr.incoming')
# cdr_csv = os.getenv('cdr.csv')
# cdr_archive = os.getenv('cdr.archive')
# cdr_failed = os.getenv('cdr.failed')
# cdr_temp = os.getenv('cdr.temp')
# delimiter = os.getenv('output.format.csv.delimiter')
delimiter=output_format_csv_delimiter


move_files = True

from parser import Parser

print(f"Start processing \"{datetime.now()}\" ...")
for input_file_name in os.listdir(cdr_incoming):
	try:
		input_file_path = os.path.join(cdr_incoming, input_file_name)
		if not os.path.isfile(input_file_path):
			print(f"{input_file_path} is not file.")
			continue

		# move incoming file to the new path 
		cdr_archive = os.path.join(cdr_archive, ".".join([input_file_name, "parsed"]))
		# where to store processed file
		output_file_path = os.path.join(cdr_csv, input_file_name)
		
		if input_file_name.startswith('SDPOUTPUTCDR'):
			# Parse SDP files only
			parser = Parser()
			parser.parse_sdp(
				input_file_name=input_file_name,
				input_file_path=input_file_path,
				output_file_path=output_file_path,
				delimiter=delimiter,
				cdr_archive=cdr_archive,
				move_files=move_files
				) 
		print(f"Processing done successfully \"{datetime.now()}\" ...")
	except Exception as e:
		print(f"Processing done -- with error \"{datetime.now()}\" ...")

print(f"Processing done \"{datetime.now()}\" ...")


