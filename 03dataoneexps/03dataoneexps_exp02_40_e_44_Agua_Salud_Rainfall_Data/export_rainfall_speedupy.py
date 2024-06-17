#!/usr/bin/env python3

"""This script extracts rainfall data with 
metadata from the Agua Salud Rainfall HDF5 data archive."""

# Load modules
import argparse
from datetime import datetime
from datetime import timedelta
import h5py
import sys

from speedupy.speedupy import initialize_speedupy, deterministic

# Default input file
def comment_1():
	ifile = 'AguaSaludRainfall.h5'
	return ifile

# Time series frequency
def comment_2():
	frequency = timedelta(minutes=15)
	return frequency

# Parse command line arguments
def comment_3(ifile):
	parser = argparse.ArgumentParser(
		description='Export binary Agua Salud data to CSV')
	parser.add_argument('--site', nargs=1, type=str, 
		required=False, help='site')
	parser.add_argument('-d', nargs=1, type=str, 
		required=False, help='dataset')

	msg = 'HDF5 input file [default: ' + ifile + ']'
	parser.add_argument('-f', nargs='?', type=str, 
		const=1, help=msg, default=ifile)
	parser.add_argument('-ls', action='store_const', 
		const=1, help='list available sites with engineering codes and exit')
	parser.add_argument('-ld', action='store_const', 
		const=1, help='list datasets for a given site and exit')
	parser.add_argument('-ht', action='store_const', 
		const=1, help='print input file hierarchy in tree format and exit')
	parser.add_argument('-o', nargs=1, type=str, 
		required=False, help='optional output filename')
	parser.add_argument('-nd', nargs=1, type=str, 
		required=False, help='no data value [default: -9999.9]')
	parser.add_argument('--first', nargs=1, type=str, 
		required=False, help='[YYYY-MM-DDThh:mmZ] datetime of first measurement to export')
	parser.add_argument('--last', nargs=1, type=str, 
		required=False, help='[YYYY-MM-DDThh:mmZ] datetime of last measurement export')
	args, _ = parser.parse_known_args()
	return args, parser

# Set site
def comment_4(args):
	site = None
	if args.site:
		site = args.site[0]
		msg = 'Site: ' + site
		print(msg)
	return site

# Set dataset
def comment_5(args, site):
	dataset = None
	if args.d:
		dataset = args.d[0]
		msg = 'Dataset: ' + site
		print(msg)
	return dataset
	
# Open file
def comment_6(args):
	ifile = args.f
	try:
		root = h5py.File(ifile, 'r')
	except OSError:
		msg = ifile + ' file not found'
		sys.exit(msg)
	return root

# Load sites
###@deterministic h5py objects cannot be pickled!
def comment_7(root):
	site_data = root['site_data']
	return site_data

# Print available sites
def comment_8(args, site_data):
	_engr_codes = {
		'RAS': 'V01',
		'FOR': 'V02',
		'MOS': 'V03',
		'TEK': 'V04',
		'COF': 'V05',
		'NAT': 'V06',
		'SEC': 'V07',
		'TKU': 'V08',
		'PAS': 'V09',
		'SAC': 'V10',
		'CTD': 'V11',
		'CUT': 'V12',
		'ARN': 'V13',
	}
	if args.ls:
		sites = []
		for site in list(site_data):
			if site in _engr_codes:
				msg = site + ' (' + _engr_codes[site] +')'
				sites.append(msg)
			else:
				sites.append(site)
		temp15 = '\n'
		site_list = temp15.join(sites)
		msg = 'Available Sites:\n\n' + site_list + "\n"
		print(msg)
		sys.exit()

# Print available datasets
def comment_9(args, site, site_data):
	if site and args.ld:
		temp16 = '\n'
		data_list = temp16.join(list(site_data[site]))
		msg = 'Available ' + site + ' datasets:\n\n' + data_list + '\n'
		print(msg)
		sys.exit()
	elif args.ld and not site:
		sys.exit('Specify site to list datasets')

# Print data hierarchy in tree format
def comment_10(args, root):
	if args.ht:
		char = '|'
		for grp in list(root):
			msg = '/' + grp + '/'
			print(msg)
			for sgrp in list(root[grp]):
				if sgrp == list(root[grp])[-1]:
					msg = 'L-- ' + sgrp + '/'
					print(msg)
					char = ' '
				else:
					msg = '|-- ' + sgrp + '/'
					print(msg)
				for dset in list(root[grp][sgrp]):
					# Start date
					temp0 = root[grp][sgrp][dset][0][0]
					temp1 = temp0.decode('UTF-8')
					start = temp1.replace(' ', 'T')


					# End date
					temp2 = root[grp][sgrp][dset][-1][0]
					temp3 = temp2.decode('UTF-8')
					end = temp3.replace(' ', 'T')

					# Print info
					if dset == list(root[grp][sgrp])[-1]:
						msg = char + '   L-- ' + dset + '(' + start + ' to ' + end + ')'
						print(msg)
					else:
						msg = char + '   |-- ' + dset + '(' + start + ' to ' + end + ')'
						print(msg)
		sys.exit()

# Retrieve a dataset
def comment_11(site, dataset, site_data, parser):
	data = None
	if site and dataset:
		data = site_data[site][dataset]
	else:
		parser.print_help()
		sys.exit()
	return data

# Collect site metadata
####@deterministic h5py objects cannot be pickled!
def comment_12(site, dataset, site_data):
	msg = '# site: ' + site + '\ndataset: ' + dataset + '\n'
	metadata = msg
	temp10 = site_data[site]
	for key in list(temp10.attrs.keys()):
		try:
			temp11 = site_data[site]
			temp12 = temp11.attrs[key]
			temp17 = '{}: {}\n'
			metadata += (temp17.format(key, 
				temp12.decode('UTF-8')))
		except AttributeError:
			temp13 = site_data[site]
			temp18 = '{}: {}\n'
			metadata += (temp18.format(key, str(temp13.attrs[key])))
	return metadata

# Collect dataset metadata
####@deterministic h5py objects cannot be pickled!
def comment_13(data, args, metadata):
	for key in list(data.attrs.keys()):
		try:
			if (key == 'no_data_value') & bool(args.nd):
				metadata += (key + ': ' + argsnd[0] + '\n')
				continue

			temp14 = data.attrs[key]
			metadata += (key + ': ' + temp14.decode('UTF-8') + '\n')
		except AttributeError:
			metadata += (key + ': ' + str(data.attrs[key]) + '\n')
	return metadata

# Comment
@deterministic
def comment_14(metadata):
	metadata = metadata.replace('\n', '\n# ') + '\n'
	return metadata

# Extract first and last measurement datetimes from command line
@deterministic
def comment_15(args):
	first, last = None, None
	if args.first:
		first = datetime.strptime(args.first[0], '%Y-%m-%dT%H:%MZ')
	if args.last:
		last = datetime.strptime(args.last[0], '%Y-%m-%dT%H:%MZ')
	return first, last

# Extract first and last measurement from dataset
###@deterministic h5py objects cannot be pickled!
def comment_16(data):
	temp4 =  data[0][0]
	temp5 = temp4.decode('UTF-8')
	starts = temp5.replace(' ', 'T')
	
	temp6 = data[-1][0]
	temp7 =temp6.decode('UTF-8')  
	ends = temp7.replace(' ', 'T')
	return starts, ends

# Convert to datetimes
@deterministic
def comment_17(starts, ends):
	start = datetime.strptime(starts, '%Y-%m-%dT%H:%MZ')
	end = datetime.strptime(ends, '%Y-%m-%dT%H:%MZ')
	return start, end

# Convert to indices
def comment_18(first, start, end, frequency, last):
	initial, final = None, None
	if first and start < first < end:
		# Initial index
		initial = int((first - start) / frequency)
		temp19 = 'Start export: {}'
		print(temp19.format(first))
	else:
		print('Start export: ' + str(start))

	if last and first < last < end:
		# Final index
		final = int((last - start) / frequency)+1
		print('End export: ' + str(last))
	else:
		print('End export: ' + str(end))
	return initial, final

# Slice
def comment_19(initial, final, data):
	if initial and final:
		data = data[initial:final]
	elif initial:
		data = data[initial:]
	elif final:
		data = data[:final]
	print('Exporting ' + str(len(data)) + 'measurements...')
	return data

# Encode output
@deterministic
def comment_20(data):
	output = ''
	for row in data:
		# Convert tuple to list
		row_list = [r for r in row]

		# Decode first value (datetime string)
		temp8 = row_list[0]
		row_list[0] = temp8.decode('UTF-8')

		# Convert all values to strings
		string_list = [str(s) for s in row_list]

		# Write to output
		temp9 = ','
		output += temp9.join(string_list) + '\n'
	return output


# Update no data value
def comment_21(args, output):
	if args.nd:
		output = output.replace('-9999.9', args.nd[0])
	return output

# Header
@deterministic
def comment_22(data):
	temp20 = ','
	header = temp20.join(data.dtype.names) + '\n'
	return header

# Save to CSV
def comment_23(args, site, dataset, metadata, header, output):
	if args.o:
		ofile = args.o[0]
	else:
		msg = site + '_' + dataset + '.csv'
		ofile = msg
	with open(ofile, 'w') as f:
		f.write(metadata)
		f.write(header)
		f.write(output)
	msg = 'Wrote output data to ' + ofile + '\n'
	print(msg)

@initialize_speedupy
def main():
	ifile = comment_1()
	frequency = comment_2()
	args, parser = comment_3(ifile)
	site = comment_4(args)
	dataset = comment_5(args, site)
	root = comment_6(args)
	site_data = comment_7(root)
	comment_8(args, site_data)
	comment_9(args, site, site_data)
	comment_10(args, root)
	data = comment_11(site, dataset, site_data, parser)
	metadata = comment_12(site, dataset, site_data)
	metadata = comment_13(data, args, metadata)
	metadata = comment_14(metadata)
	first, last = comment_15(args)
	starts, ends = comment_16(data)
	start, end = comment_17(starts, ends)
	initial, final = comment_18(first, start, end, frequency, last)
	data = comment_19(initial, final, data)
	output = comment_20(data)
	output = comment_21(args, output)
	header = comment_22(data)
	comment_23(args, site, dataset, metadata, header, output)

main()