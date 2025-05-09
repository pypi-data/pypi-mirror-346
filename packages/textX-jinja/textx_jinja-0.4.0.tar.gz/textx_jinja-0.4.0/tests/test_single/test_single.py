"""
Test situation where source path is a single template file.
"""
import pytest
import os
from textxjinja import textx_jinja_generator


class Model:
    first = "This is first"
    second = "This is second"
    some_list = [1, 2, 3]


this_folder = os.path.dirname(__file__)
template_file = os.path.join(this_folder, 'first.txt.jinja')


@pytest.fixture
def config():
    # Prepare config
    config = {}
    config['model'] = Model
    config['root'] = '-root-'
    return config


def test_single(config):

    output_file = os.path.join(this_folder, 'first.txt')
    # Remove output file
    try:
        os.remove(output_file)
    except OSError:
        pass

    assert not os.path.exists(output_file)

    # Generate
    textx_jinja_generator(template_file, this_folder, config, overwrite=True)

    assert os.path.exists(output_file)

    # Test the content
    with open(output_file, 'r') as f:
        first_content = f.read()
        assert 'This is a simple template.' in first_content
        assert 'root = -root-' in first_content
        assert 'first = This is first' in first_content


def test_single_file_output_path(config):
    """
    Test that if output file is not directory but the first before path element
    last is, then the output is treated as output file name.
    """

    output_file = os.path.join(this_folder, 'first_with_filename.txt')
    # Remove output file
    try:
        os.remove(output_file)
    except OSError:
        pass

    assert not os.path.exists(output_file)

    # Generate
    textx_jinja_generator(template_file, output_file, config, overwrite=True)

    assert os.path.exists(output_file)

    # Test the content
    with open(output_file, 'r') as f:
        first_content = f.read()
        assert 'This is a simple template.' in first_content
        assert 'root = -root-' in first_content
        assert 'first = This is first' in first_content
