# Shane Rivera - Integrated Forensics for first 6 methods.


import os
import pandas as pd 
import numpy as np
import csv 
import time 
from datetime import datetime
import subprocess
import shutil
from git import Repo
from git import exc

# Start of Forensics Integration.

FORENSIC_LOG_FILE = "forensic_log.txt"

def log_forensic_event(event):
    """Log forensic events to a file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(FORENSIC_LOG_FILE, 'a') as log_file:
        log_file.write(f"{timestamp} - {event}\n")

def giveTimeStamp():
    tsObj = time.time()
    strToret = datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
    log_forensic_event(f"Timestamp generated: {strToret}")
    return strToret

def deleteRepo(dirName, type_):
    log_forensic_event(f"Attempting to delete directory: {dirName}, type: {type_}")
    print(':::' + type_ + ':::Deleting ', dirName)
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            log_forensic_event(f"Directory deleted: {dirName}")
        else:
            log_forensic_event(f"Directory does not exist: {dirName}")
    except OSError as e:
        log_forensic_event(f"Failed to delete directory: {dirName}, error: {e}")
        print('Failed deleting, will try manually')

def dumpContentIntoFile(strP, fileP):
    try:
        with open(fileP, 'w') as fileToWrite:
            fileToWrite.write(strP)
        file_size = os.stat(fileP).st_size
        log_forensic_event(f"Content dumped into file: {fileP}, size: {file_size} bytes")
        return str(file_size)
    except Exception as e:
        log_forensic_event(f"Failed to write content into file: {fileP}, error: {e}")
        return "0"

def makeChunks(the_list, size_):
    log_forensic_event(f"Creating chunks of size {size_} for list of length {len(the_list)}")
    try:
        for i in range(0, len(the_list), size_):
            chunk = the_list[i:i+size_]
            log_forensic_event(f"Chunk created: {chunk}")
            yield chunk
    except Exception as e:
        log_forensic_event(f"Failed to create chunks, error: {e}")

def cloneRepo(repo_name, target_dir):
    cmd_ = "git clone " + repo_name + " " + target_dir
    log_forensic_event(f"Attempting to clone repo: {repo_name} into directory: {target_dir}")
    try:
        subprocess.check_output(['bash', '-c', cmd_])
        log_forensic_event(f"Successfully cloned repo: {repo_name}")
    except subprocess.CalledProcessError as e:
        log_forensic_event(f"Failed to clone repo: {repo_name}, error: {e}")
        print('Skipping this repo ... trouble cloning repo:', repo_name)

def checkPythonFile(path2dir):
    usageCount = 0
    patternDict = ['sklearn', 'h5py', 'gym', 'rl', 'tensorflow', 'keras', 'tf', 'stable_baselines', 'tensorforce', 'rl_coach', 'pyqlearning', 'MAMEToolkit', 'chainer', 'torch', 'chainerrl']
    log_forensic_event(f"Checking Python files in directory: {path2dir}")
    try:
        for root_, dirnames, filenames in os.walk(path2dir):
            for file_ in filenames:
                full_path_file = os.path.join(root_, file_)
                if os.path.exists(full_path_file):
                    if file_.endswith(('py', 'ipynb')):
                        with open(full_path_file, 'r', encoding='latin-1') as f:
                            pythonFileContent = f.read().lower().split('\n')
                        for content_ in pythonFileContent:
                            for item_ in patternDict:
                                if item_ in content_:
                                    usageCount += 1
                                    log_forensic_event(f"Pattern match: {item_} in file: {full_path_file}, line: {content_}")
    except Exception as e:
        log_forensic_event(f"Error checking Python files in directory: {path2dir}, error: {e}")
    log_forensic_event(f"Total pattern matches found: {usageCount}")
    return usageCount

def days_between(d1_, d2_):
    try:
        days_diff = abs((d2_ - d1_).days)
        log_forensic_event(f"Days between {d1_} and {d2_}: {days_diff}")
        return days_diff
    except Exception as e:
        log_forensic_event(f"Error calculating days between {d1_} and {d2_}, error: {e}")
        return -1
        


# Forensics Integration Ends Here.



def getDevEmailForCommit(repo_path_param, hash_):
    author_emails = []

    cdCommand         = "cd " + repo_path_param + " ; "
    commitCountCmd    = " git log --format='%ae'" + hash_ + "^!"
    command2Run = cdCommand + commitCountCmd

    author_emails = str(subprocess.check_output(['bash','-c', command2Run]))
    author_emails = author_emails.split('\n')
    # print(type(author_emails)) 
    author_emails = [x_.replace(hash_, '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('^', '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('!', '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('\\n', ',') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    try:
        author_emails = author_emails[0].split(',')
        author_emails = [x_ for x_ in author_emails if len(x_) > 3 ] 
        # print(author_emails) 
        author_emails = list(np.unique(author_emails) )
    except IndexError as e_:
        pass
    return author_emails  
    
def getDevDayCount(full_path_to_repo, branchName='master', explore=1000):
    repo_emails = []
    all_commits = []
    repo_emails = []
    all_time_list = []
    if os.path.exists(full_path_to_repo):
        repo_  = Repo(full_path_to_repo)
        try:
           all_commits = list(repo_.iter_commits(branchName))   
        except exc.GitCommandError:
           print('Skipping this repo ... due to branch name problem', full_path_to_repo )
        # only check commit by commit if less than explore threshold

        for commit_ in all_commits:
            commit_hash = commit_.hexsha

            emails = getDevEmailForCommit(full_path_to_repo, commit_hash)
            repo_emails = repo_emails + emails
            
            timestamp_commit = commit_.committed_datetime
            str_time_commit  = timestamp_commit.strftime('%Y-%m-%d') ## date with time 
            all_time_list.append( str_time_commit )

    all_day_list   = [datetime(int(x_.split('-')[0]), int(x_.split('-')[1]), int(x_.split('-')[2]), 12, 30) for x_ in all_time_list]
    try:
        min_day        = min(all_day_list) 
        max_day        = max(all_day_list) 
        ds_life_days   = days_between(min_day, max_day)
    except (ValueError, TypeError):
        ds_life_days   = 0
    ds_life_months = round(float(ds_life_days)/float(30), 5)
    
    return len(repo_emails) , len(all_commits) , ds_life_days, ds_life_months 
            
  
def getPythonFileCount(path2dir):
    valid_list = [] 
    for _, _, filenames in os.walk(path2dir):
        for file_ in filenames:
            if ((file_.endswith('py')) or (file_.endswith('ipynb'))):
                valid_list.append(file_)
    return len(valid_list)   
    
    

def cloneRepos(repo_list, dev_threshold=3, python_threshold=0.10, commit_threshold = 25): 
    counter = 0     
    str_ = ''
    all_list = []
    for repo_batch in repo_list:
        for repo_ in repo_batch:
            counter += 1 
            print('Cloning ', repo_ )
            dirName = '../FSE2021_REPOS/' + repo_.split('/')[-2] + '@' + repo_.split('/')[-1] ## '/' at the end messes up the index 
            cloneRepo(repo_, dirName )
            ### get all count 
            checkPattern, dev_count, python_count, commit_count, age_months   = 0 , 0, 0, 0, 0 
            flag = True
            all_fil_cnt = sum([len(files) for r_, d_, files in os.walk(dirName)])
            python_count = getPythonFileCount(dirName) 
            if (all_fil_cnt <= 0):
                deleteRepo(dirName, 'NO_FILES')
                flag = False
            elif (python_count < (all_fil_cnt * python_threshold) ):
                deleteRepo(dirName, 'NOT_ENOUGH_PYTHON_FILES')
                flag = False
            else:       
                dev_count, commit_count, age_days, age_months  = getDevDayCount(dirName)
                if (dev_count < dev_threshold):                
                    deleteRepo(dirName, 'LIMITED_DEVS') 
                    flag = False  
                elif (commit_count < commit_threshold):                
                    deleteRepo(dirName, 'LIMITED_COMMITS')  
                    flag = False
            if (flag == True ): 
                checkPattern = checkPythonFile(dirName) 
                if (checkPattern == 0 ):
                    deleteRepo(dirName, 'NO_PATTERN')
                    flag = False        
            print('#'*100 )
            str_ = str_ + str(counter) + ',' +  repo_ + ',' + dirName + ','  + str(checkPattern) + ',' + str(dev_count) + ',' + str(flag) + ',' + '\n'
            tup = ( counter,  dirName, dev_count, all_fil_cnt, python_count , commit_count, age_months, flag)
            all_list.append( tup ) 
            print("So far we have processed {} repos".format(counter) )
            if((counter % 100) == 0):
                dumpContentIntoFile(str_, 'tracker_completed_repos.csv')
                df_ = pd.DataFrame( all_list ) 
                df_.to_csv('PYTHON_BREAKDOWN.csv', header=['INDEX', 'REPO', 'DEVS', 'FILES', 'PYTHON_FILES', 'COMMITS', 'AGE_MONTHS', 'FLAG'] , index=False, encoding='utf-8')    

            if((counter % 1000) == 0):
                print(str_)                
            print('#'*100)
        print('*'*10)
        
   

if __name__=='__main__':
    repos_df = pd.read_csv('PARTIAL_REMAINING_GITHUB.csv', sep='delimiter')
    print(repos_df.head())
    list_    = repos_df['url'].tolist()
    list_ = np.unique(list_)
    
    t1 = time.time()
    print('Started at:', giveTimeStamp() )
    print('*'*100 )

    
    print('Repos to download:', len(list_)) 
    ## need to create chunks as too many repos 
    chunked_list = list(makeChunks(list_, 100))  ### list of lists, at each batch download 1000 repos 
    cloneRepos(chunked_list)


    print('*'*100 )
    print('Ended at:', giveTimeStamp() )
    print('*'*100 )
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print('Duration: {} minutes'.format(time_diff) )
    print( '*'*100  )  
