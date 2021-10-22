import os,shutil
from website import db,app

# reinitialize database tables
def clear_database():

	db.drop_all()
	db.create_all()

	return 'Database cleared successfully'

# clear cache directory
def clear_cache():
	cache_path =os.path.join(os.getcwd(),'website','__pycache__')
	shutil.rmtree(cache_path,ignore_errors=True)

	return 'Cache directory cleared successfully'

print(clear_database(),clear_cache(),sep='\n')