# -*- coding: utf-8 -*-

import os

from jinja2 import Environment, FileSystemLoader

from pdmparse.parsers import read


class PdmParse(object):

    def __init__(self, pdm_path: str, template_dir: str, filters: dict = None):
        if not os.path.exists(pdm_path) or not os.path.isfile(pdm_path):
            raise IOError('pdm文件路径:%s,路径不存在,或者不是文件' % pdm_path)

        if not os.path.exists(template_dir) or not os.path.isdir(template_dir):
            raise IOError('template_dir文件目录:%s,目录不存在,或者不是目录' % template_dir)

        filters = filters or {}
        loader = FileSystemLoader(template_dir)
        env = Environment(loader=loader)
        env.filters.update(filters.copy())
        self.env = env
        self.pdm_path = pdm_path

    def get_template(self, template_name):
        template = self.env.get_template(template_name)
        return template

    def gen_template_file(self, out_dir, template_name, table_filter_func,
                          out_file_rename_func=None, **kwargs):
        t = self.get_template(template_name)
        pdm_tables = read(self.pdm_path)
        for pdm_table in pdm_tables:
            if table_filter_func(pdm_table):
                d = {'table': pdm_table}
                d.update(**kwargs)
                if out_file_rename_func:
                    out_file_name = out_file_rename_func(pdm_table)
                else:
                    out_file_name = '%s%s' % (pdm_table.code, '.txt')

                out_file = os.path.join(out_dir, out_file_name)
                out_file_dir = os.path.dirname(out_file)
                if not os.path.exists(out_file_dir):
                    os.makedirs(out_file_dir)

                with open(out_file, 'w') as f:
                    f.write(t.render(d))

    def gen_single_template_file(self, out_dir, template_name, out_file_name, table_filter_func, **kwargs):
        t = self.get_template(template_name)
        pdm_tables = read(self.pdm_path)
        pdm_tables = [pdm_table for pdm_table in pdm_tables if table_filter_func(pdm_table)]

        d = {'tables': pdm_tables}
        d.update(**kwargs)

        out_file = os.path.join(out_dir, out_file_name)
        out_file_dir = os.path.dirname(out_file)
        if not os.path.exists(out_file_dir):
            os.makedirs(out_file_dir)

        with open(out_file, 'w') as f:
            f.write(t.render(d))
