import re
from webscraper.model.optionfilter import OptionFilter
from webscraper.model.webfilter import WebFilter
from webscraper.view.consoleview import ConsoleView


class WebData(OptionFilter):
    CONSOLIDATE_DATA_PARAM_COUNT = 2
    CONSOLIDATE_ERROR_MSG = 'Error consolidating data, please try again...'

    def __init__(self, web_request, web_object_factory, data_handler):
        super(OptionFilter).__init__()
        self.web_request = web_request
        self.web_filter = WebFilter()
        self.web_object_factory = web_object_factory
        self.data_handler = data_handler
        self.filtered_data = []
        self.filtered_data_keywords = []
        self.filtered_recursive_data = []
        self.filtered_recursive_data_keywords = []
        self.web_data_objects = []
        self.view = ConsoleView()

    def handle_command(self, args):
        return self.command(args, web_data_options)

    def get_data(self):
        return self.web_data_objects

    def clear_filtered_data(self, *args):
        self.view.display_item('clearing filtered data.....')
        del self.filtered_data[:]
        del self.filtered_data_keywords[:]
        del self.filtered_recursive_data[:]
        del self.filtered_recursive_data_keywords[:]
        del self.web_data_objects[:]

    def print_data(self, *args):
        attr = self.method_options(args[self.COMMAND_OPTION],
                                   web_data_print_options)
        if attr is not None:
            if not isinstance(attr, list):
                self.view.display_item(args[self.COMMAND_OPTION] + ': ' +
                                       str(attr))
            else:
                self.view.display_items(attr)

    def print_web_data_object(self, *args):
        self.view.display_item('displaying web data objects.....')
        self.view.display_item('---------------------------------'
                               '-------------------------------')
        for wo in self.web_data_objects:
            wo.func_display_data(wo, self.view)
            self.view.display_item('-----------------------------'
                                   '-----------------------------------')

    def display_saves(self, *args):
        self.data_handler.display_save_list()

    def load_saved_data(self, *args):
        self.view.display_item('loading saved data.....')
        loaded_objs = self.data_handler.load_objects(args[self.PARAMETER_ONE])
        self.web_data_objects = loaded_objs

    def save_data(self, *args):
        self.view.display_item('saving data to disk.....')
        self.data_handler.save_objects(self.web_data_objects,
                                       args[self.PARAMETER_ONE])

    def remove_data(self, *args):
        self.data_handler.remove_objects(args[self.PARAMETER_ONE])

    def get_request_data(self, *args):
        data_options = self.check_second_level_args(args)[self
                                                          .COMMAND_OPTION]
        request_data = self.web_request.get_request_data()
        self.filtered_data = self.web_filter.filter_request_data(data_options,
                                                                 request_data)

    def get_recursive_request_data(self, *args):
            data_options = self.check_second_level_args(args)[self
                                                              .COMMAND_OPTION]
            recursive_data = self.web_request.get_recursive_request_data()
            self.filtered_recursive_data = self.web_filter.\
                filter_recursive_request_data(data_options, recursive_data)

    def filter_urls(self, *args):
        data_options = self.check_second_level_args(args)[self
                                                          .COMMAND_OPTION]
        urls = self.web_filter.filter_urls(data_options, self.filtered_data)
        for url in urls:
            self.web_request.add_recursive_url(url)

    def set_data_keywords(self, *args):
        kw_pairs = self.check_second_level_args(args)
        if kw_pairs is not None:
            for kw_pair in kw_pairs:
                keywords = [kw_pair[0], kw_pair[1], kw_pair[2]]
                self.view.display_item('adding tag, class pair: ' +
                                       str(keywords))
                self.filtered_data_keywords.append(keywords)

    def set_recursive_data_keywords(self, *args):
        kw_pairs = self.check_second_level_args(args)
        if kw_pairs is not None:
            for kw_pair in kw_pairs:
                r_keywords = [kw_pair[0], kw_pair[1], kw_pair[2]]
                self.view.display_item('adding tag, class pair: ' +
                                       str(r_keywords))
                self.filtered_recursive_data_keywords.append(r_keywords)

    def consolidate_data(self, *args):
        params = self.check_second_level_args(args)
        if params is not None and self.check_second_level_param_count(
                params, self.CONSOLIDATE_DATA_PARAM_COUNT):
            func_one = self.method_options(
                params[self.PARAMETER_ONE][self.PARAMETER_ONE],
                web_data_consolidate_options)
            func_two = self.method_options(
                params[self.PARAMETER_TWO][self.PARAMETER_ONE],
                web_data_consolidate_options)
            try:
                attr_one = func_one(self.filtered_data,
                                    self.filtered_data_keywords,
                                    params[self.PARAMETER_ONE]
                                    [self.PARAMETER_TWO],
                                    params[self.PARAMETER_ONE]
                                    [self.PARAMETER_THREE])
                attr_two = func_two(self.filtered_recursive_data,
                                    self.filtered_recursive_data_keywords,
                                    params[self.PARAMETER_TWO]
                                    [self.PARAMETER_TWO],
                                    params[self.PARAMETER_TWO]
                                    [self.PARAMETER_THREE])
                self.create_web_data_object(attr_one, attr_two)
            except TypeError:
                self.view.display_item(self.CONSOLIDATE_ERROR_MSG)

    def filter_by_children(self, *args):
        data = args[0]
        return self.web_filter.filter_by_children(data)

    def filter_by_keywords(self, *args):
        data = args[self.PARAMETER_ONE]
        data_kw = args[self.PARAMETER_TWO]
        return self.web_filter.filter_by_keywords(data_kw, data)

    def create_web_data_object(self, attr_one, attr_two, obj_name='product'):
        if len(attr_two) > 0:
            for attr_one, attr_two in zip(attr_one, attr_two):
                self.view.display_item('creating object.....')
                attr_one.update(attr_two)
                new_obj = self.web_object_factory.build_object(obj_name,
                                                               attr_one)
                self.web_data_objects.append(new_obj)
        else:
            for attr_one in attr_one:
                self.view.display_item('creating object.....')
                new_obj = self.web_object_factory.build_object(obj_name,
                                                               attr_one)
                self.web_data_objects.append(new_obj)


# possible web data options and parameter count
web_data_options = {'wo': ['print_web_data_object', 1], 'p': ['print_data', 2],
                    'l': ['load_saved_data', 2], 's': ['save_data', 2],
                    'g': ['get_request_data', 2],
                    'gr': ['get_recursive_request_data', 2],
                    'cf': ['clear_filtered_data', 1], 'fu': ['filter_urls', 2],
                    'dk': ['set_data_keywords', 2],
                    'rdk': ['set_recursive_data_keywords', 2],
                    'cd': ['consolidate_data', 2], 'ds': ['display_saves', 1],
                    'rs': ['remove_data', 2]}

web_data_print_options = {'fdata': 'filtered_data',
                          'rdata': 'filtered_recursive_data',
                          'fdkeywords': 'filtered_data_keywords',
                          'rfdkeywords': 'filtered_recursive_data_keywords'}

web_data_consolidate_options = {'kw': 'filter_by_keywords',
                                'child': 'filter_by_children'}
