broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
enable_utc = True
worker_hijack_root_logger = False
imports = ('tasks.thumbnail',)