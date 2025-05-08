# -*- coding: utf-8 -*-

import os
from xml.etree import ElementTree as ET

from .table import Table, Column, Reference, ReferenceJoin, Diagram


def get_pdm_root(pdm_path):
    """获取pdm文件的root根元素"""
    if not os.path.exists(pdm_path):
        raise IOError('pdm文件%s不存在' % pdm_path)

    tree = ET.parse(pdm_path)  # 类ElementTree
    ET.register_namespace('a', "attribute")
    ET.register_namespace('c', "collection")
    ET.register_namespace('o', "object")
    # 获取namespace
    """
    for i in tree.iter():
        print(f'namespace:{i.tag}')
    """
    root = tree.getroot()
    return root


def read(pdm_path):
    root = get_pdm_root(pdm_path)

    # PhysicalDiagram
    diagrams = []
    diagram_node_lst = root.iterfind(
        './{object}RootObject/{collection}Children/{object}Model/{collection}PhysicalDiagrams/{object}PhysicalDiagram')
    for d in diagram_node_lst:
        diagram_id = d.attrib.get('Id')
        diagram_name_node = d.find('{attribute}Name')
        diagram_code_node = d.find('{attribute}Code')

        diagram = Diagram(diagram_id, diagram_name_node.text, diagram_code_node.text)
        diagrams.append(diagram)

        ref_table_nodes = d.iterfind('{collection}Symbols/{object}TableSymbol/{collection}Object/{object}Table')
        if ref_table_nodes is None:
            continue
        for table_node in ref_table_nodes:
            diagram.add_ref_table_id(table_node.attrib.get('Ref'))

    # 表关联信息
    references = []
    reference_node_lst = root.iterfind(
        './{object}RootObject/{collection}Children/{object}Model/{collection}References/{object}Reference')
    for ref in reference_node_lst:
        ref_id = ref.attrib.get('Id')
        ptable_id = ref.find('{collection}ParentTable/{object}Table').attrib.get('Ref')
        ctable_id = ref.find('{collection}ChildTable/{object}Table').attrib.get('Ref')
        if ref.find('{collection}ParentKey/{object}Key') is None:
            continue
        parent_keyid = ref.find('{collection}ParentKey/{object}Key').attrib.get('Ref', None)
        ele_joins = ref.findall('{collection}Joins/{object}ReferenceJoin')
        joins = []
        for ele_join in ele_joins:
            join_id = ele_join.attrib.get('Id')
            ptable_column_id = ele_join.find(
                '{collection}Object1/{object}Column').attrib.get('Ref')
            ctable_column_id = ele_join.find(
                '{collection}Object2/{object}Column').attrib.get('Ref')
            joins.append(
                ReferenceJoin(join_id, ptable_column_id, ctable_column_id))
        references.append(
            Reference(ref_id, ptable_id, ctable_id, parent_keyid, joins))

    # 表数据
    tables = []
    table_node_lst = root.iterfind(
        './{object}RootObject/{collection}Children/{object}Model/{collection}Tables/{object}Table')
    for t in table_node_lst:
        table_id = t.attrib.get('Id')
        # table_object_id_node = t.find('{attribute}ObjectID')
        table_name_node = t.find('{attribute}Name')
        table_code_node = t.find('{attribute}Code')
        table_comment_node = t.find('{attribute}Comment')
        table_creation_date_node = t.find('{attribute}CreationDate')
        table_creator_node = t.find('{attribute}Creator')
        table = Table(table_id, table_name_node.text,
                      table_code_node.text, table_comment_node.text if table_comment_node is not None else None,
                      table_creator_node.text, table_creation_date_node.text)

        # 获取表的Keys，Key与列之间的引用关系
        keys = []
        for key in t.iterfind('{collection}Keys/{object}Key'):
            key_id = key.attrib.get('Id')
            key_col_ref = [col.attrib.get('Ref') for col in key.iterfind('{collection}Key.Columns/{object}Column')]
            for ref in key_col_ref:
                keys.append({'key_id': key_id, 'key_col_ref': ref})

        # 主键对Key的引用关系
        ele_pk_key = t.find('{collection}PrimaryKey/{object}Key')
        if ele_pk_key is None:
            pk_key_ref = None
        else:
            pk_key_ref = ele_pk_key.attrib.get('Ref')

        # 在这里假定Keys不是主键(PK)就是唯一键(AK)
        pks = []
        aks = []
        for key in keys:
            if key['key_id'] == pk_key_ref:
                pks.append(key['key_col_ref'])
            else:
                aks.append(key['key_col_ref'])

        # 获取当前表包含的列
        columns = []
        for c in t.iterfind('{collection}Columns/{object}Column'):
            column_id = c.attrib.get('Id')
            column_name = c.find('{attribute}Name').text
            column_code = c.find('{attribute}Code').text
            column_data_type_node = c.find('{attribute}DataType')
            column_length_node = c.find('{attribute}Length')
            column_precision_node = c.find('{attribute}Precision')

            column_data_type = column_data_type_node.text if column_data_type_node is not None else None
            column_length = column_length_node.text if column_length_node is not None else None
            column_precision = column_precision_node.text if column_precision_node is not None else None
            is_pk = column_id in pks
            is_ak = column_id in aks
            is_fk = len([ref for ref in references if ref.ctable_id ==
                         table.id and column_id in ref.ctable_column_ids]) > 0
            is_mandatory = c.find('{attribute}Column.Mandatory') is not None
            is_identity = c.find('{attribute}Identity') is not None

            column = Column(column_id, column_name, column_code, column_data_type,
                            column_length, column_precision, is_pk, is_ak, is_fk,
                            is_mandatory, is_identity)
            columns.append(column)
        table.columns = columns
        tables.append(table)

    # 完善FnReference对象的属性，因为在前面只是获得了表和列的id，通过这个步骤将引用（FnReference）的父子表、
    # join的键对应关系表实例化为FnTable，FnColumn对象
    for ref in references:
        for table in tables:
            if table.id == ref.ptable_id:
                ref.ptable = table
            if table.id == ref.ctable_id:
                ref.ctable = table

        for join in ref.joins:
            join.ptable_column = [
                column for column in ref.ptable.columns if column.obj_id == join.ptable_column_id][0]
            join.ctable_column = [
                column for column in ref.ctable.columns if column.obj_id == join.ctable_column_id][0]

    # 完善Table的父引用和子引用属性
    for table in tables:
        table.parent_refs = [ref for ref in references if ref.ctable_id == table.id]
        table.child_refs = [ref for ref in references if ref.ptable_id == table.id]
        table.diagrams = [diagram for diagram in diagrams if table.id in diagram.ref_table_ids]
    return tables
