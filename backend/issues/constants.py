#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
BUG = 1
TASK = 2
STORY = 3
EPIC = 4

ROLE_CHOICES = (
    (BUG, 'Bug'),
    (TASK, 'Task'),
    (STORY, 'Story'),
    (EPIC, "Epic")
)
OPEN = 1
IN_PROGRESS = 2
IN_REVIEW = 3
CODE_COMPLETE = 4
DONE = 5

STATUS_CHOICES = (
    (OPEN, 'Open'),
    (IN_PROGRESS, 'In Progress'),
    (IN_REVIEW, 'In Review'),
    (CODE_COMPLETE, 'Code Complete'),
    (DONE, 'Done')
)