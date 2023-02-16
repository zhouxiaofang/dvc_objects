import queue
import sys
from concurrent import futures
from itertools import islice
from typing import Any, Callable, Iterable, Iterator, Set, TypeVar

from datetime import datetime
from multiprocessing import Process
import math

_T = TypeVar("_T")

# create by zhoufang 20221205
class ProcessPoolExecutor(futures.ProcessPoolExecutor):
    _max_workers: int

    def __init__(
        self, max_workers: int = None, cancel_on_error: bool = False, **kwargs
    ):
        super().__init__(max_workers=max_workers, **kwargs)
        self._cancel_on_error = cancel_on_error

    @property
    def max_workers(self) -> int:
        return self._max_workers

    def imap_unordered(
        self, fn: Callable[..., _T], *iterables: Iterable[Any]
    ) -> Iterator[_T]:
        """test multi process to transfer"""
                
        time1 = datetime.now()
        it = zip(*iterables)
        src_file_list = list(it)

        print("开启的转储进程数目为：", self.max_workers)
        
        length = len(src_file_list)
        n = self.max_workers
        datas_global_list = []
        for i in range(n):
            one_thread_list = src_file_list[math.floor(i / n * length): math.floor((i + 1) / n * length)]
            datas_global_list.append(one_thread_list)
        print("主进程成功获取所有文件图片，需要转储的文件切片数目：", len(datas_global_list))
        
        process_list = []
        for i in range(self.max_workers):
            t = Process(target=fn, args=(datas_global_list,i, ))
            t.start()
            process_list.append(t)
        for t in process_list:
            t.join()
       
        time2 = datetime.now()
        print("主进程执行的总时间：", time2 - time1)
        
        result_list = [0,0,0,0]
        return result_list
        

    
