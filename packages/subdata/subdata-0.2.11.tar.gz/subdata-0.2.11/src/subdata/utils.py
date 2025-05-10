import json
import os
import numpy as np

import importlib.resources

def load_download():
    with importlib.resources.open_text('subdata.resources', 'download_dict.json') as file:
        download_dict = json.load(file)
    return download_dict

def load_instruction():
    with importlib.resources.open_text('subdata.resources', 'instruction_dict.json') as file:
        instruction_dict = json.load(file)
    return instruction_dict

def load_process():
    with importlib.resources.open_text('subdata.resources', 'process_dict.json') as file:
        process_dict = json.load(file)
    return process_dict

def load_overview(overview_name):

    if overview_name == 'original':
        with importlib.resources.open_text('subdata.resources', 'overview_original.json') as file:
            overview_dict = json.load(file)
        print('Loading original overview.')
    else:
        if os.path.exists(f'modified_resources/overview_{overview_name}.json'):
            with open(f'modified_resources/overview_{overview_name}.json') as file:
                overview_dict = json.load(file)
            print(f'Loading {overview_name} overview.')
        else:
            with importlib.resources.open_text('subdata.resources', 'overview_original.json') as file:
                overview_dict = json.load(file)
            print(f'Overview with name {overview_name} does not (yet) exist. Loading original overview.')

    return overview_dict


def load_mapping(mapping_name):

    if mapping_name == 'original':
        with importlib.resources.open_text('subdata.resources', 'mapping_original.json') as file:
            mapping_dict = json.load(file)
        print('Loading original mapping.')
    else:
        if os.path.exists(f'modified_resources/mapping_{mapping_name}.json'):
            with open(f'modified_resources/mapping_{mapping_name}.json') as file:
                mapping_dict = json.load(file)
            print(f'Loading {mapping_name} mapping.')
        else:
            with importlib.resources.open_text('subdata.resources', 'mapping_original.json') as file:
                mapping_dict = json.load(file)
            print(f'Mapping with name {mapping_name} does not (yet) exist. Loading original mapping.')

    return mapping_dict


def load_taxonomy(taxonomy_name):

    if taxonomy_name == 'original':
        with importlib.resources.open_text('subdata.resources', 'taxonomy_original.json') as file:
            taxonomy_dict = json.load(file)
        print('Loading original taxonomy.')
    else:
        if os.path.exists(f'modified_resources/taxonomy_{taxonomy_name}.json'):
            with open(f'modified_resources/taxonomy_{taxonomy_name}.json') as file:
                taxonomy_dict = json.load(file)
            print(f'Loading {taxonomy_name} taxonomy.')
        else:
            with importlib.resources.open_text('subdata.resources', 'taxonomy_original.json') as file:
                taxonomy_dict = json.load(file)
            print(f'Taxonomy with name {taxonomy_name} does not (yet) exist. Loading original taxonomy.')

    return taxonomy_dict


def save_modified_resource(resource, resource_name):

    if not os.path.exists('modified_resources'): # modified resources (mapping, taxonomy, overview) are stored locally
        os.mkdir('modified_resources')

    with open(f'modified_resources/{resource_name}.json', 'w') as f:
        f.write(json.dumps(resource, indent=4))


def save_latex(resource_str, resource_name):
    if not os.path.exists('latex_resources'): # modified resources (mapping, taxonomy, overview) are stored locally
        os.mkdir('latex_resources')

    with open(f'latex_resources/{resource_name}.txt', 'w') as f:
        f.write(resource_str)


def taxonomy_to_latex(resource):
    n_rows = np.max([len(v) for k,v in resource.items()])
    n_cols = len(resource.keys())+1

    start_str = f'\\begin{{table*}}\n\\footnotesize\n\\begin{{tabular}}{{{''.join(['l' for i in range(n_cols)])}}}\n\\toprule\n'
    first_row = 'category & ' + ' & '.join(resource.keys()) + ' \\\\\n\\midrule'

    content_row = ''
    for row in range(n_rows):
        row_str = f'target {row+1}'
        for targets in resource.values():
            row_str += f' & {targets[row]}' if row < len(targets) else ' & '
        row_str += ' \\\\'
        content_row += '\n'+row_str

    end_str = '\n\\bottomrule\n\\end{tabular}\n\\end{table*}'

    full_str = start_str + first_row + content_row + end_str
    return full_str.replace('_','\\_')


def mapping_to_latex(resource):

    start_str = f'\\begin{{table*}}\n\\footnotesize\n\\begin{{tabular}}{{ll}}\n\\toprule\n'
    end_str = '\n\\bottomrule\n\\end{tabular}\n\\end{table*}'
    full_str = ''

    for dataset_name, dataset_mapping in resource.items():

        first_row = f'{dataset_name} & \\\\\nold term & new term\\\\\n\\midrule'

        content_row = ''
        for old_term, new_term in dataset_mapping.items():
            row_str = f'{old_term} & {new_term} \\\\'
            content_row += '\n'+row_str

        mapping_str = start_str + first_row + content_row + end_str
        full_str += mapping_str + '\n\n'

    return full_str.replace('_','\\_')
    
