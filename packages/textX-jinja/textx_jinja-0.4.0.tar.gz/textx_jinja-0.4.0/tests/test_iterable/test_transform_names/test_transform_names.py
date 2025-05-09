"""
Test tranform_names function generating file names when iterable
variable is in filename.
"""
import os
import shutil
from textxjinja import textx_jinja_generator


def transform_names(var):
    return '.test_{}'.format(var)


def test_iterable():
    this_folder = os.path.dirname(__file__)
    template_folder = os.path.join(this_folder, 'templates')
    output_folder = os.path.join(this_folder, 'output')

    # Remove output folder
    try:
        shutil.rmtree(output_folder)
    except OSError:
        pass

    # Prepare context
    context = {}
    context['vars'] = ['first', 'second']

    # Generate
    textx_jinja_generator(template_folder, output_folder, context,
                          overwrite=True, transform_names=transform_names)

    # Assert both files are present
    first = os.path.join(output_folder, '.test_first.cf')
    second = os.path.join(output_folder, '.test_second.cf')
    assert os.path.exists(first)
    assert os.path.exists(second)

    # Test the content
    with open(first, 'r') as f:
        first_content = f.read()
        assert 'Test file: first' in first_content

    with open(second, 'r') as f:
        second_content = f.read()
        assert 'Test file: second' in second_content
