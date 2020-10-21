# -*- coding: utf-8 -*- 

import unittest
from includes import *
from common import getConnectionByEnv, waitForIndex, sortedResults, toSortedFlatList
from time import sleep, time
from RLTest import Env
import random


def testNewUnionIteratorRead(env):
  num_num_per_index = 1000
  num_diff_num = 10000
  num_docs = num_num_per_index * num_diff_num
  num_queries = 1
  pipe_batch = 100000
  pl = env.getConnection().pipeline()
  #env.expect('FLUSHALL').ok()
  #env.expect('SAVE').ok()

  start_time = time()
  for i in range(num_docs):
    pl.execute_command('HSET','doc%d' % i, 'n', (i / (num_diff_num)) + 0.1)
    if i % pipe_batch == 0:
      pl.execute()
  pl.execute()
  print 'adding docs for ' + str(time() - start_time)
  
  start_time = time()
  env.expect('FT.CREATE idx SCHEMA n NUMERIC').ok()
  waitForIndex(env, 'idx')
  print 'indexing for ' + str(time() - start_time)
  
  print '\n' + env.execute_command('ft.info idx') + '\n'

  start_time = time()
  for i in range(num_queries):
    pl.execute_command('FT.SEARCH','idx', '@n:[%d %d]' % (-1, 40000000))
    if i % pipe_batch == 0:
      pl.execute()
  pl.execute()
  print 'quering for ' + str(time() - start_time)
#18) "2.841949462890625" 2.5724830627441406
#18) "11.604504585266113" 11.590058326721191 120.70540618896484
