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
all_page_command = url_sites + site_id + "/analytics/content/all_pages"
entry_point_command = url_sites + site_id + "/analytics/content/entry_pages"
exit_point_command = url_sites + site_id + "/analytics/content/exit_pages"
least_popular_pages_command = url_sites + site_id + "/analytics/content/least_popular_pages"
most_popular_pages_command = url_sites + site_id + "/analytics/content/most_popular_pages"
pages_without_visit_command = url_sites + site_id + "/analytics/content/pages_without_visits"

all_page_thread = threading.Thread(target=start_looper, args=(all_page_command,
                                                              "all_pages.json",
                                                              "all_pages_error_output.json",
                                                              "all_pages_error_log.txt"))

entry_point_thread = threading.Thread(target=start_looper, args=(entry_point_command,
                                                                 "entrypoints2.json",
                                                                 "entrypoints2_error_output.json",
                                                                 "entrypoints2_error_log.txt"))

exit_point_thread = threading.Thread(target=start_looper, args=(exit_point_command,
                                                                "exitpoints.json",
                                                                "exitpoints_error_output.json",
                                                                "exitpoints_error_log.txt"))

least_popular_pages_thread = threading.Thread(target=start_looper, args=(least_popular_pages_command,
                                                                         "least_popular_pages.json",
                                                                         "least_popular_pages_error_output.json",
                                                                         "least_popular_pages_error_log.txt"))

most_popular_pages_thread = threading.Thread(target=start_looper, args=(most_popular_pages_command,
                                                                        "most_popular_pages.json",
                                                                        "most_popular_pages_error_output.json",
                                                                        "most_popular_pages_error_log.txt"))

pages_without_visit_thread = threading.Thread(target=start_looper, args=(pages_without_visit_command,
                                                                         "pages_without_visit.json",
                                                                         "pages_without_visit_error_output.json",
                                                                         "pages_without_visit_error_log.txt"))

all_page_thread.start()
entry_point_thread.start()
exit_point_thread.start()
least_popular_pages_thread.start()
most_popular_pages_thread.start()
pages_without_visit_thread.start()