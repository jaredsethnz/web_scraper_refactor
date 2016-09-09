

class WebFilter(object):

    def get_request_data(self, *args):
        try:
            data_options = self.check_second_level_args(args)[self
                                                              .COMMAND_OPTION]
            data = self.web_request.get_request_data()
            req_data = BeautifulSoup(data, 'html.parser') \
                .findAll(data_options[self.TAG_TYPE],
                         attrs={data_options[self.CLASS_ID]: data_options
                         [self.CLASS_ID_NAME]})
            for data in req_data:
                self.filtered_data.append(data)
                self.view.display_item('filtering data.....')
        except TypeError:
            self.view.display_item(self.COMMAND_ERROR_MSG)
            return

    def get_recursive_request_data(self, *args):
        try:
            data_options = self.check_second_level_args(args)[self
                                                              .COMMAND_OPTION]
            for data in self.web_request.get_recursive_request_data():
                self.view.display_item('filtering recursive data.....')
                rec_data = BeautifulSoup(data, 'html.parser') \
                    .find(data_options[self.TAG_TYPE],
                          attrs={data_options[self.CLASS_ID]: data_options
                          [self.CLASS_ID_NAME]})
                self.filtered_recursive_data.append(rec_data)
        except TypeError:
            self.view.display_item(self.COMMAND_ERROR_MSG)
            return

    def filter_urls(self, *args):
        try:
            data_options = self.check_second_level_args(args)[self
                                                              .COMMAND_OPTION]
            self.view.display_item('filtering urls.....')
            for data in self.filtered_data:
                tag_depth = self.check_data_int(data_options[self.CLASS_ID])
                if tag_depth is not None:
                    url = data.find_all(data_options[self.TAG_TYPE])
                    self.web_request.add_recursive_url(url[tag_depth]['href'])
                else:
                    url = data.find(data_options[self.TAG_TYPE], attrs={
                        data_options[self.CLASS_ID]:
                            data_options[self.CLASS_ID_NAME]})
                    self.web_request.add_recursive_url(url['href'])
        except (TypeError, KeyError, IndexError):
            self.view.display_item(self.COMMAND_ERROR_MSG)
            return

    def filter_by_children(self, *args):
        obj_attrs = []
        data = args[0]
        for d in data:
            names = OrderedSet()
            attrs = {}
            try:
                for dc in d.find_all('div'):
                    name = dc.find('span')
                    value = dc.find('div')
                    if value and name is not None:
                        if name.text not in names:
                            names.add(name.text)
                            attrs[name.text] = value.text
                obj_attrs.append(attrs)
            except AttributeError:
                self.view.display_item('Error filtering data '
                                       'from children.....')
        web_objs = self.sanitise_attributes(obj_attrs)
        return web_objs

    def filter_by_keywords(self, *args):
        data = args[self.PARAMETER_ONE]
        data_kw = args[self.PARAMETER_TWO]
        obj_attr = []
        for d in data:
            try:
                attrs = {}
                for kw_pair in data_kw:
                    tag_depth = self.check_data_int(
                        kw_pair[self.PARAMETER_TWO])
                    if tag_depth is not None:
                        value = d.find_all(kw_pair[self.PARAMETER_ONE])
                        value = value[tag_depth].string
                        value = self.check_data_type(value) if \
                            value else 'unknown'
                        attrs[kw_pair[self.PARAMETER_THREE]] = value
                    else:
                        value = d.find(kw_pair[self.PARAMETER_ONE],
                                       {kw_pair[self.PARAMETER_TWO]: kw_pair
                                       [self.PARAMETER_THREE]}).string
                        value = self.check_data_type(value) if \
                            value else 'unknown'
                        attrs[kw_pair[self.PARAMETER_THREE]] = value
                obj_attr.append(attrs)
            except (TypeError, KeyError, IndexError):
                self.view.display_item(self.CONSOLIDATE_ERROR_MSG)
        return obj_attr

    def sanitise_attributes(self, obj_attrs):
        sanitised_obj_attrs = []
        for dict in obj_attrs:
            attrs = {}
            for key, value in dict.items():
                value = value.replace(key, '')
                key = key.replace(value, '')
                sanitized_key = key.replace('\n', '').replace(' ', '').lower()
                sanitized_value = re.sub('[ ]+', ' ',
                                         value.replace('\n', '')).strip()
                sanitized_value = self.check_data_type(sanitized_value)
                attrs[sanitized_key] = sanitized_value
            sanitised_obj_attrs.append(attrs)
        return sanitised_obj_attrs