import os,shutil

# clear cache directory
def clear_cache():
	cache_path =os.path.join(os.getcwd(),'website','__pycache__')
	shutil.rmtree(cache_path,ignore_errors=True)

	return 'Cache directory cleared successfully'

print(clear_cache())