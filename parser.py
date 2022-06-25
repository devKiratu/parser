# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Date:   2022-02-28 12:25:19
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2022-03-02 11:03:50

import json
import os

from dtone_cdrparser import CDRParserException, parse_file

class Parser:
	def __init__(self):
		pass

	def to_sdp_format(self, data):
		data_info = {}
		delimiter=';'

		if data.get('accountAdjustment',{}):
			adj_record = {
			'recordType':'SDP_ADJUSTMENT',
			'localSequenceNumber': data['accountAdjustment'].get('cdrID',''),
			'originHostName': data['accountAdjustment'].get('originNodeId',''),
			'sdpId': data['accountAdjustment'].get('sdpId',''),
			'accountNumber': data['accountAdjustment'].get('accountNumber',''),
			'timeStamp': data['accountAdjustment'].get('timeStamp',''),
			'originTimestamp': data['accountAdjustment'].get('originTimestamp',''),
			'currentServiceClass': data['accountAdjustment'].get('serviceClassId',''),
			'originNodeType':data['accountAdjustment'].get('originNodeType',''),
			'originTransactionID': data['accountAdjustment'].get('originTransactionID',''),
			'accountCurrency': data['accountAdjustment'].get('accountCurrency',''),
			'transactionAmount': data['accountAdjustment'].get('transactionAmount',''),
			'balanceBefore': data['accountAdjustment'].get('balanceBefore',''),
			'balanceAfter': data['accountAdjustment'].get('balanceAfter',''),
			'transactionType': data['accountAdjustment'].get('transactionType',''),
			'transactionCode': data['accountAdjustment'].get('transactionCode',''),
			'adjustmentAction': data['accountAdjustment'].get('adjustmentAction',[]),
			'adjustmentAmount': data['accountAdjustment'].get('adjustmentAmount',''),
			'accountBalanceBefore': data['accountAdjustment'].get('balanceBefore',''),
			'accountBalanceAfter': data['accountAdjustment'].get('balanceAfter',''),
			}

		
			for item in data['accountAdjustment'].get('adjustmentDedicatedAccounts',[]):
				amount = item.get('adjustmentAmount','')
				after = item.get('accountValueAfter','')
				before = item.get('accountValueAfter','')
				action = item.get('action','')
				uuid = item.get('dedicatedAccountID','')

				data_info[item.get('dedicatedAccountID','')] = {
				'amount': amount,
				'after':after,
				'before':before,
				'action':action,
				}

				adj_record['DA{}_adjustmentAmount'.format(uuid)] = amount
				adj_record['DA{}_accountValueBefore'.format(uuid)] = before
				adj_record['DA{}_accountValueAfter'.format(uuid)] = after
				adj_record['DA{}_action'.format(uuid)] = action

			return f"2{delimiter}1{delimiter}{adj_record['accountNumber']}{delimiter}{adj_record['originNodeType']}{delimiter}{adj_record['originHostName']}{delimiter}{adj_record['originTransactionID']}{delimiter}{adj_record['originTimestamp']}{delimiter}{adj_record['sdpId']}{delimiter}{adj_record['timeStamp']}{delimiter}{adj_record['accountCurrency']}{delimiter}{adj_record['adjustmentAction']}{delimiter}{adj_record['adjustmentAmount']}{delimiter}{adj_record['accountBalanceBefore']}{delimiter}{adj_record['accountBalanceAfter']}{delimiter}{delimiter}{adj_record['currentServiceClass']}{delimiter}{delimiter}{delimiter}{json.dumps(data_info)}\n"
		else:
			return None

	def parse_sdp(self, **kwargs):
		input_file_name = kwargs['input_file_name']
		input_file_path = kwargs['input_file_path']
		output_file_path = kwargs['output_file_path']
		cdr_archive=kwargs['cdr_archive']
		move_files=kwargs['move_files']


		try:
			parsed_data = parse_file(input_file_path)
			with open(output_file_path, "w") as f:
				for data in parsed_data:
					# TODO: consider using variables within object
					formatted_data = self.to_sdp_format(data)
					if formatted_data:
						f.write(formatted_data)
			        
		except CDRParserException as e:
			print(f"File \"{input_file_path}\" could not be parsed with e {e}.")
		else:
			if move_files:
				# move files
				os.rename(input_file_path, cdr_archive)
			print(f"File \"{input_file_path}\" was successfuly processed.") 
			pass