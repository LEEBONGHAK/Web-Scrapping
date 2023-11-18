from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_so_jobs
from save import save_to_file

# 인디드에서 채용공고를 긁어 오는 함수
indeed_jobs = get_indeed_jobs()

# 스택오버플로우에서 채용공고를 긁어 오는 함수
so_jobs = get_so_jobs()

jobs = indeed_jobs + so_jobs

# 긁어온 데이터를 csv로 저장하는 함수
save_to_file(jobs)