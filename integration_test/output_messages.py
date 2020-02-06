"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

messages = [
    "INFO - Admin: Initialized empty ml-git repository in",  # 0
    "INFO - Admin: You already are in a ml-git repository",  # 1
    "INFO - Admin: Add remote repository [%s] for [dataset]",  # 2
    "INFO - Admin: Add remote repository [%s] for [labels]",  # 3
    "INFO - Admin: Add remote repository [%s] for [model]",  # 4
    "INFO - Admin: Changing remote from [%s]  to [%s] for  [dataset]",  # 5
    "ERROR - Admin: You are not in an initialized ml-git repository.",  # 6
    "INFO - Admin: Add store [s3h://%s] in region [us-east-1] with creds from profile [%s]",  # 7
    "INFO - Metadata Manager: Metadata init [%s] @ [%s]",  # 8
    "ERROR - Repository: The path [%s] already exists and is not an empty directory.",  # 9
    "ERROR - Repository: Unable to find %s. Check the remote repository used.",  # 10
    "ERROR - Repository: Unable to find remote repository. Add the remote first.",  # 11
    "INFO - Admin: Add remote repository [%s] for [model]",  # 12
    "INFO - Repository: dataset adding path",  # 13
    "INFO - Repository: model adding path",  # 14
    "INFO - Repository: labels adding path",  # 15
    "ERROR - Repository: The entity name passed is wrong. Please check again",  # 16
    "INFO - Metadata Manager: Commit repo[%s] --- file[%s]",  # 17
    "INFO - Local Repository: No blobs to push at this time.",  # 18
    "INFO - Repository: dataset adding path [%s] to ml-git index",  # 19
    "INFO - Metadata Manager: Pull [%s]",  # 20
    "ERROR - Local Repository: The amount parameter should be smaller than the group size.",  # 21
    "ERROR - Local Repository: The group size parameter should be smaller than the file list size.",  # 22
    "ERROR - Local Repository: The start parameter should be smaller than the stop.",  # 23
    "ERROR - Local Repository: The stop parameter should be smaller than or equal to the file list size.",  # 24
    "ERROR - Local Repository: The start parameter should be greater than or equal to zero.",  # 25
    "ERROR - Local Repository: The step parameter should be smaller than the stop.",  # 26
    "INFO - Repository: There is no new data to add",  # 27
    "ERROR - Local Repository: The group size parameter should be greater than zero.",  # 28
    "ERROR - Local Repository: The frequency  parameter should be greater than zero.",  # 29
    "ERROR - Local Repository: The amount parameter should be smaller than the frequency.",  # 30
    "ERROR - Local Repository: The frequency  parameter should be smaller than the file list size.",  # 31
    "ERROR - Local Repository: Requires positive integer values.",  # 32
    "ERROR - Admin: Permission denied. You need write permission to initialize ml-git in this directory.",  # 33
    "ERROR - Repository: You are not in an initialized ml-git repository.",  # 34
    "INFO - MLGit: remote-fsck -- fixed   : ipld[%d] / blob[%d]",  # 35
    "Total of corrupted files: %d",  # 36
    "INFO - Metadata Manager: Pull [%s]",  # 37
    "Project Created.",  # 38
    "Successfully loaded configuration files!",  # 39
    "ERROR - Local Repository: The --random-sample=<amount:frequency> --seed=<seed>: requires positive integer values.", #40
    "ERROR - Local Repository: The --group-sample=<amount:group-size> --seed=<seed>: requires positive integer values.", #41
    "ERROR - Local Repository: The --range-sample=<start:stop:step> or  --range-sample=<start:stop>: requires positive integer values." ,#42
    "ERROR - Local Repository: The amount parameter should be greater than zero.", # 43
    " Could not read from remote repository.", # 44
    "The path [%s] is not an empty directory. Consider using --folder to create an empty folder.", # 45
    "Permission denied", # 46
    "2.00/2.00",  # 47
    "ERROR - Repository: No current tag for [%s]. commit first.",  # 48
    "tag '%s' already exists",  # 49
    "ERROR - Local Repository: Fatal downloading error [Unable to locate credentials]",  # 50
    "ERROR - Local Repository: Fatal downloading error [An error occurred (403) when calling the HeadObject operation: Forbidden",  # 51
    "ERROR - Store Factory: The config profile (%s) could not be found",  # 52
    "INFO - Repository: Create Tag Successfull",  # 53
    "The AWS Access Key Id you provided does not exist in our records.",  # 54
    "No current tag for [%s]. commit first",  # 55
    "ML dataset\n|-- computer-vision\n|   |-- images\n|   |   |-- dataset-ex\n",  # 56
    "-- dataset : dataset-ex --\ncategories:\n- computer-vision\n- images\nmanifest:\n  files: MANIFEST.yaml\n  store: s3h://mlgit\nname: dataset-ex\nversion: 12\n\n",  # 57
    "%d missing descriptor files. Consider using the --thorough option.",  # 58
    "%d missing descriptor files. Download:",  # 59
    "Corruption detected for chunk [%s]",  # 60
]
