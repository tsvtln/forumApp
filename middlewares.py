import time

from django.utils.deprecation import MiddlewareMixin


def measure_time_execution(get_response):
    def middleware(request, *args, **kwargs):
        start_time = time.time()
        response = get_response(request, *args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        return response
    return middleware


# class MeasureTimeExecution:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request, *args, **kwargs):
#         start_time = time.time()
#         response = self.get_response(request, *args, **kwargs)
#         end_time = time.time()
#         print(f"Execution time: {end_time - start_time:.4f} seconds")
#         return response

class MeasureTimeExecution(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()

    def process_view(self, request, view, *args, **kwargs):
        print("It's processing the view...")

    def process_template_response(self, request, response):
        print("It's processing the template response...")
        return response

    def process_exception(self, request, exception):
        print(f"An exception occurred: {exception}")
        return None  # Return None to continue processing the exception

    def process_response(self, request, response):
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        print(f"New Class Measure Time: {total_time} seconds.")
        return response
