import traceback


def traceback_framename(stack_level=-3):
    """
    Mendapatkan frame name dimana fungsi yg memanggil
    fungsi dimana fungsi ini diletakan ini dipanggil.

    ```py
    print(traceback_framename(-1))
    ```
    """
    return traceback.extract_stack()[stack_level].name
