import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import add_script_run_ctx
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from threading import Lock
import random

__global_lock = Lock()


def show_container(i: int, container: DeltaGenerator):
    time.sleep(random.random() * 2)
    with __global_lock:
        container.write("before" + str(i))
        container.write("after2" + str(i))


def main():
    bar = st.progress(0)
    _container = st.container()
    _container.write("tesrt2")
    # containers = [st.container() for _ in range(30)]
    # with ThreadPoolExecutor(max_workers=4,initializer=lambda:time.sleep(10)) as executor:
    with ThreadPoolExecutor(max_workers=12) as executor:
        # タスクを実行
        # futures = [executor.submit(show_container, i,_container) for i in range(30)]
        futures = executor.map(lambda i: show_container(i, _container), range(30))

        for t in executor._threads:
            add_script_run_ctx(t)

        # for f in futures:
        #     f.result()
        # タスクの完了を待つ
        # concurrent.futures.wait(futures)
        for idx, future in enumerate(as_completed(futures), start=1):
            # count, result = future.result()
            # results.append((count, result))
            progress = idx / len(futures)
            # placeholder.text(f"{int(progress * 100)}%")
            # update progress bar
            bar.progress(progress, f"{idx}の処理が完了したよ？({idx}/{len(futures)})")


if __name__ == "__main__":
    main()
