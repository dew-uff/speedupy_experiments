#!/usr/bin/env python3

"""This script extracts rainfall data with 
metadata from the Agua Salud Rainfall HDF5 data archive."""

# Load modules
import argparse
from datetime import datetime
from datetime import timedelta
import h5py
import sys

# Default input file
ifile = 'AguaSaludRainfall.h5'

# Time series frequency
frequency = timedelta(minutes=15)

# Parse command line arguments
parser = argparse.ArgumentParser(
	description='Export binary Agua Salud data to CSV')
parser.add_argument('-s', nargs=1, type=str, 
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
args = parser.parse_args()

# Set site
site = None
if args.s:
	site = args.s[0]
	msg = 'Site: ' + site
	print(msg)

# Set dataset
dataset = None
if args.d:
	dataset = args.d[0]
	msg = 'Dataset: ' + site
	print(msg)
	
# Open file
ifile = args.f
try:
	root = h5py.File(ifile, 'r')
except OSError:
	msg = ifile + ' file not found'
	sys.exit(msg)

# Load sites
site_data = root['site_data']

# Print available sites
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
	site_list = '\n'.join(sites)
	msg = 'Available Sites:\n\n' + site_list + "\n"
	print(msg)
	sys.exit()

# Print available datasets
if site and args.ld:
	data_list = '\n'.join(list(site_data[site]))
	msg = 'Available ' + site + ' datasets:\n\n' + data_list + '\n'
	print(msg)
	sys.exit()
elif args.ld and not site:
	sys.exit('Specify site to list datasets')

# Print data hierarchy in tree format
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
				start = root[grp][sgrp][dset][0][0].decode('UTF-8').replace(' ', 'T')


				# End date
				end = root[grp][sgrp][dset][-1][0].decode('UTF-8').replace(' ', 'T')

				# Print info
				if dset == list(root[grp][sgrp])[-1]:
					msg = char + '   L-- ' + dset + '(' + start + ' to ' + end + ')'
					print(msg)
				else:
					msg = char + '   |-- ' + dset + '(' + start + ' to ' + end + ')'
					print(msg)
	sys.exit()

# Retrieve a dataset
data = None
if site and dataset:
	data = site_data[site][dataset]
else:
	parser.print_help()
	sys.exit()

# Collect site metadata
msg = '# site: ' + site + '\ndataset: ' + dataset + '\n'
metadata = msg
for key in list(site_data[site].attrs.keys()):
	try:
		metadata += ('{}: {}\n'.format(key, 
			site_data[site].attrs[key].decode('UTF-8')))
	except AttributeError:
		metadata += ('{}: {}\n'.format(key, str(site_data[site].attrs[key])))

# Collect dataset metadata
for key in list(data.attrs.keys()):
	try:
		if (key == 'no_data_value') & bool(args.nd):
			metadata += (key + ': ' + argsnd[0] + '\n')
			continue

		metadata += (key + ': ' + data.attrs[key].decode('UTF-8') + '\n')
	except AttributeError:
		metadata += (key + ': ' + str(data.attrs[key]) + '\n')

# Comment
metadata = metadata.replace('\n', '\n# ') + '\n'

# Extract first and last measurement datetimes from command line
first, last = None, None
if args.first:
	first = datetime.strptime(args.first[0], '%Y-%m-%dT%H:%MZ')
if args.last:
	last = datetime.strptime(args.last[0], '%Y-%m-%dT%H:%MZ')

# Extract first and last measurement from dataset
starts = data[0][0].decode('UTF-8').replace(' ', 'T')
ends = data[-1][0].decode('UTF-8').replace(' ', 'T')

# Convert to datetimes
start = datetime.strptime(starts, '%Y-%m-%dT%H:%MZ')
end = datetime.strptime(ends, '%Y-%m-%dT%H:%MZ')

# Convert to indices
initial, final = None, None
if first and start < first < end:
	# Initial index
	initial = int((first - start) / frequency)
	print('Start export: {}'.format(first))
else:
	print('Start export: ' + str(start))

if last and first < last < end:
	# Final index
	final = int((last - start) / frequency)+1
	print('End export: ' + str(last))
else:
	print('End export: ' + str(end))

# Slice
if initial and final:
	data = data[initial:final]
elif initial:
	data = data[initial:]
elif final:
	data = data[:final]
print('Exporting ' + str(len(data)) + 'measurements...')

# Encode output
output = ''
for row in data:
	# Convert tuple to list
	row_list = [r for r in row]

	# Decode first value (datetime string)
	row_list[0] = row_list[0].decode('UTF-8')

	# Convert all values to strings
	string_list = [str(s) for s in row_list]

	# Write to output
	output += ','.join(string_list) + '\n'

# Update no data value
if args.nd:
	output = output.replace('-9999.9', args.nd[0])

# Header
header = ','.join(data.dtype.names) + '\n'

# Save to CSV
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
