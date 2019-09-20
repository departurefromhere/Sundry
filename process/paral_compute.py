# coding=utf-8

import math
from multiprocessing import Pool
import time


def parallel_compute(call_func, param_list=[], process_num=10, need_return=True):
    """
    批量并行调用某一函数,　每次调用传递参数不同, 返回结果进行合并;
    执行的函数中有DB操作时，注意需要在函数内部重新实例化DB连接实例，否则易出现未知错误
    :param call_func: 待进行的函数
    :param param_list: [(), (), ...], 参数长度（并发的进程数)
    :param process_num: int, 同时并行的子进程数,　默认最大为10
    :param need_return: 是否需要返回计算结果
    :return: {
            1: result2, 2: result2, 3:...
        }
    """
    if not param_list:
        return

    s_time = time.time()
    results = {}
    task_num = len(param_list)
    loop_num = int(math.ceil(task_num/float(process_num)))
    for t in range(0, loop_num):
        real_num = len(param_list[t*process_num:(t+1)*process_num])
        pool = Pool(processes=real_num)
        for i in range(0, real_num):
            results[t*process_num+i] = pool.apply_async(call_func, param_list[t*process_num+i])

        pool.close()
        pool.join()
        e_time = time.time()
        print("parallel_compute {0} {1} tasks took {2}s"
              .format(str(call_func.__name__), process_num, e_time - s_time))

    if not need_return:
        return

    for k, v in results.items():
        results[k] = v.get()

    return results


if __name__ == "__main__":
    def test(id, name, gold):
        time.sleep(1)
        print("test ", id, name, gold)
        return id * 10

    params_list = []
    for i in range(20):
        params_list.append([i, "hello_{0}".format(i), i*100])
    result = parallel_compute(test, params_list, need_return=1, process_num=10)

    print("\nresult=", result)