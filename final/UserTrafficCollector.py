from Site_Improve_Page_Looper import Site_Improve_Page_Looper
import threading
import time


def start_looper(command, output_file, error_output_file, error_log_file):
    start_time = time.time()
    looper = Site_Improve_Page_Looper()
    looper.collect_pages(command=command,
                         output_file=output_file,
                         error_output_file=error_output_file,
                         error_log_file=error_log_file)
    print("Finished executing:\t" + command)
    print("Start time:\t" + time.asctime(time.localtime(start_time)))
    print("Finish time:\t" + time.asctime(time.localtime(time.time())))
    print("Execution time:\t" + time.asctime(time.localtime(time.time() - start_time)))


site_id = "1348629560"
url_sites = "https://api.siteimprove.com/v2/sites/"