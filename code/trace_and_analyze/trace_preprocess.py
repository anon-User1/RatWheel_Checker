import re
from pathlib import Path
import os

#emit error trace
ERROR_KEYWORD = {'EIO'，'EBADMODE'，'ENOENT'，'EADDRINUSE'，'EADDRNOTAVAIL'，'ENETDOWN'， 'EBADF'，'ENOTEMPTY'，'ENOTDLT'，'ENOTWRITE'，'ENOTREAD', 'ECONNABORTED', 'ECONNREFUSED', 'EPIPE'}
SIG_KEYWORD = {'SIGBUS', 'SIGEMT', 'SIGFPE', 'SIGILL', 'SIGSEGV', 'SIGTRAP'}

#file descriptor regular expression
FD_RE = '\<.*\>'

#system call class
class SysCall:
	def __init__(self):
		self.time = ''
		self.type = ''
		self.param = ''


def get_return_val(trace):
	tmp = trace.split(' = ')
	if len(tmp) == 1:
		return 'NULL'
	else:
		return tmp[1].strip()

#caregorize and symplify traces
def trace_categ(trace):

	trace = trace.replace('$','')

	sys_call = SysCall()

	time = trace.split(' ')
	sys_call.time = time[0]
	param_re = '\(.*\)'
	params = re.search(param_re, trace, re.M|re.I)
	param_flag = 0
	if params:
		params = params.group().replace('(','').replace(')','').split(', ')
		param_flag = 1

	for keyword in ERROR_KEYWORD:
		if keyword in trace:
			return None
	try:
	#file management
		if "statfs(" in trace:
			sys_call.type = 'statfs'
			path = ' '
			buf = ' '
			if param_flag:
				path = params[0]
				buf = params[1]
			sys_call.param = path + "$" + buf
		if "open(" in trace:
			sys_call.type = 'open'
			tmp = trace.split('"')
			path_name = tmp[1]
			return_val = get_return_val(trace)
			sys_call.param = path_name + "$" + return_val
		if "dup2(" in trace:
			sys_call.type = 'dup2'
			oldfd = ' '
			newfd = ' '
			if param_flag:
				oldfd = params[0]
				newfd = params[1]
			sys_call.param = oldfd + "$" + newfd
		if "getdents" in trace:
			sys_call.type = 'getdents'
			fd = ' '
			dirp = ' '
			if param_flag:
				fd = params[0]
				dirp = params[1]
			return_val = get_return_val(trace)
			sys_call.param = fd + "$" + dirp + "$" + return_val

		''' currently not considered
		if "lseek(" in trace:
			sys_call.type = 'lseek'
		'''

	#I/O operation
		if "read(" in trace:
			sys_call.type = 'read'
			fd = ' '
			buf = ' '
			if param_flag:
				fd_raw = params[0]
				fd = re.search(FD_RE, fd_raw, re.M|re.I)
				if fd:
					fd = fd.group().replace('<','').replace('>','')
				buf = params[1].strip().replace('"','').replace('"','')
			return_val = get_return_val(trace)
			sys_call.param = fd + "$" + buf + "$" + return_val
		if "write(" in trace:
			sys_call.type = 'write'
			fd = ' '
			buf = ' '
			if param_flag:
				fd_raw = params[0]
				fd = re.search(FD_RE, fd_raw, re.M|re.I)
				if fd:
					fd = fd.group().replace('<','').replace('>','')
				buf = params[1].strip().replace('"','').replace('"','')
			return_val = get_return_val(trace)
			sys_call.param = fd + "$" + buf + "$" + return_val
		if "fsync(" in trace:
			sys_call.type = 'fsync'
			fd = ' '
			if param_flag:
				fd = params[0]
			sys_call.param = fd
		if "ioctl(" in trace:
			sys_call.type = 'ioctl'
			fd = ' '
			request = ' '
			if param_flag:
				fd = params[0]
				request = params[1]
			sys_call.param = fd + "$" + request
		if "eventfd(" in trace:
			sys_call.type = 'eventfd'
			initvalue = ' '
			if param_flag:
				initvalue = params[0]
			sys_call.param = initvalue
		if "epoll_wait(" in trace:
			sys_call.type = 'epoll_wait'
			epoll_fd = ' '
			epoll_event = ' '
			if param_flag:
				epoll_fd = params[0]
				epoll_event = params[1]
			sys_call.param = epoll_fd + "$" + epoll_event
		if "epoll_ctl(" in trace:
			sys_call.type = 'epoll_ctl'
			epoll_fd = ' '
			epoll_event = ' '
			if param_flag:
				epoll_fd = params[0]
				epoll_event = params[1]
			sys_call.param = epoll_fd + "$" + epoll_event


	#memory operation
		if "mmap(" in trace:
			sys_call.type = 'mmap'
			addr = ' '
			length = ' '
			fd = ' '
			if param_flag:
				addr = params[0]
				length = params[1]
				fd = params[4]
			return_val = get_return_val(trace)
			sys_call.param = addr + "$" + length + "$" + fd + "$" + return_val

		if "madvice(" in trace:
			sys_call.type = 'madvice'
			addr = ' '
			length = ' '
			fd = ' '
			if param_flag:
				addr = params[0]
				length = params[1]
				fd = params[4]
			return_val = get_return_val(trace)
			sys_call.param = addr + "$" + length + "$" + fd + "$" + return_val

		if "malloc(" in trace:
			sys_call.type = 'malloc'
			addr = ' '
			length = ' '
			fd = ' '
			if param_flag:
				addr = params[0]
				length = params[1]
				fd = params[4]
			return_val = get_return_val(trace)
			sys_call.param = addr + "$" + length + "$" + fd + "$" + return_val

	#thread operation
		if "clone" in trace:
			sys_call.type = 'clone'
			child_stack = ' '
			parent_tid = ' '
			if param_flag:
				child_stack = params[0]
				parent_tid = get_return_val(trace)
			sys_call.param = child_stack + "$" + parent_tid

		if "kill" in trace:
			sys_call.type = 'kill'
			pid = ' '
			if param_flag:
				pid = params[0]
			sys_call.param = pid

		
		if "futex(" in trace:
			sys_call.type = 'futex'
			params = re.search(param_re, trace, re.M|re.I)
			if params:
				params = params.group().replace('(','').replace(')','').split(',')
				uaddr = params[0]
				futex_op = params[1]
			sys_call.param = uaddr + "$" + futex_op

		if "pipe(" in trace:
			sys_call.type = 'pipe'
			pidfd = ' '
			if param_flag:
				pidfd = params[0]
			sys_call.param = pidfd

		if "socket(" in trace:
			sys_call.type = 'socket'
			domain = ' '
			s_type = ' '
			if param_flag:
				domain = params[0]
				s_type = params[1]
			sys_call.param = domain + "$" + s_type

		if "bind(" in trace:
			sys_call.type = 'bind'
			sockfd = ' '
			addr = ' '
			if param_flag:
				sockfd = params[0]
				addr = params[1]
			sys_call.param = sockfd + "$" + addr		

		if "connect(" in trace:
			sys_call.type = 'connect'
			sockfd = ' '
			addr = ' '
			if param_flag:
				sockfd = params[0]
				addr = params[1]
			sys_call.param = sockfd + "$" + addr	
			
		return sys_call

		''' currently not considered
		if "mprotect(" in trace:
			sys_call.type = 'mprotect'
		'''
	except (Exception) as e:
		raise e

	return None

def get_file_size(file):
	fsize = os.path.getsize(file)
	return fsize/1000

def trace_filter(file, store_path):
	fsize = os.path.getsize(file)
	'''
	filter out small files
	current size = 50kb
	'''
	if (fsize/1000) > 50:
		raw_trace_file = open(file,'r')
		file_name = file.split('/')
		file_name = file_name[-1]
		clean_trace_file = open(store_path + file_name + ".clean" , 'w')

		for line in raw_trace_file:
			line = line.replace('\n','')
			try:
				trace = trace_categ(line)
			except (Exception) as e:
				print (file)
				print (line)
				print (e)
			if trace != None:
#				clean_trace_file.write(trace.time + " " + trace.type + "$" + trace.param + "\n")
				clean_trace_file.write(trace.type + "$" + trace.param + "\n")

		raw_trace_file.close()
		clean_trace_file.close()



def trace_preprocess(trace_file_path):

	g = os.walk(trace_file_path)

	for path,dir_list,file_list in g:
		for file in file_list:
			trace_filter(os.path.join(path, file), "path")


#test
trace_preprocess("path")



	