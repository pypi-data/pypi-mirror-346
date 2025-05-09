import os
import re
import shutil
import logging
from jinja2 import Environment, FileSystemLoader


__version__ = "0.4.0"

logger = logging.getLogger(__name__)

# Compatibility with Python 2.7
try:
    FileExistsError
except NameError:
    FileExistsError = OSError

placeholder_re = re.compile(r'__[^_]\w+?[^_]__')


class SkipFile(Exception):
    pass


class FileCount:
    def __init__(self):
        self.created = 0
        self.overwritten = 0
        self.skipped = 0

    def __str__(self):
        return '{}/{}/{}'.format(self.created, self.overwritten, self.skipped)


def textx_jinja_generator(templates_path, target_path, context, overwrite=False,
                          filters=None, transform_names=None):
    """
    Generates a set of files using Jinja templates.
    """

    """
    Args:
        templates_path (str): A path to templates.
        target_path (str): The path where files should be generated.
        context (dict): A context contains any data necessary
            for rendering files using Jinja engine.
        overwrite (bool): If the target files should be overwritten.
        filters(dict): Optional Jinja filters.
        transform_names(callable or None): If given, used to transform resolved
            placeholders in file names. The function accepts a single parameter
            and should return a string. It should default to `str(param)` in case
            no other transformation could be provided.

    """
    def eval_file_name(file_name):
        """
        Replaces all `__<var>__` if `var` is in context dict.
        Strips .jinja extension.
        Raises SkipFile if file shouldn't be processed.
        """
        # Replace placeholders in the target file name.
        placeholders = placeholder_re.findall(file_name)
        files = None
        tran_names = str if transform_names is None else transform_names

        for placeholder in placeholders:
            ph_value = context.get(placeholder.strip('_'))
            if ph_value is False:
                raise SkipFile
            elif ph_value is True:
                file_name = file_name.replace(placeholder, '')
            elif ph_value is not None:
                try:
                    iter(ph_value)
                    if isinstance(ph_value, str):
                        raise TypeError
                    files = {}
                    for ph in ph_value:
                        f_name = file_name.replace(placeholder, tran_names(ph))
                        if f_name.endswith('.jinja'):
                            f_name = '.'.join(f_name.split('.')[:-1])
                        files[f_name] = ph
                except TypeError:
                    file_name = file_name.replace(placeholder, tran_names(ph_value))

        if file_name.endswith('.jinja'):
            file_name = '.'.join(file_name.split('.')[:-1])

        if files is not None:
            return files
        return file_name

    def generate_file(src_rel_file, src_file, target_file):
        """
        Generate a single target file from the given source file.
        """
        if overwrite or not os.path.exists(target_file):

            if os.path.exists(target_file):
                logger.info('Overwriting %s', target_file)
                file_count.overwritten += 1
            else:
                logger.info('Creating %s', target_file)
                file_count.created += 1

            if src_file.endswith('.jinja'):
                # Render using Jinja template
                with open(target_file, 'w') as f:
                    f.write(
                        env.get_template(src_rel_file).render(**context))
            else:
                # Just copy
                if not src_file == target_file:
                    shutil.copy(src_file, target_file)

        else:
            logger.info('-- ***NOT*** overwriting: %s', target_file)
            file_count.skipped += 1

    file_count = FileCount()

    if os.path.isfile(templates_path):
        search_path = os.path.dirname(templates_path)
        env = Environment(loader=FileSystemLoader(searchpath=search_path),
                          trim_blocks=True, lstrip_blocks=True)
        if filters:
            env.filters.update(filters)

        src_file = templates_path
        src_rel_file = os.path.basename(templates_path)

        try:
            if not os.path.isdir(target_path):
                target_file = eval_file_name(target_path)
            else:
                target_file = os.path.join(target_path, eval_file_name(src_rel_file))
            generate_file(src_rel_file, src_file, target_file)
        except SkipFile:
            pass
            logger.info("File skipped due to configuration.")
    else:
        search_path = templates_path
        env = Environment(loader=FileSystemLoader(searchpath=search_path),
                          trim_blocks=True, lstrip_blocks=True)
        if filters:
            env.filters.update(filters)

        logger.info("Started generating files in %s", target_path)
        for root, dirs, files in os.walk(templates_path):
            for f in files:
                src_file = os.path.join(root, f)
                src_rel_file = os.path.relpath(src_file, templates_path)
                src_rel_file = src_rel_file.replace('\\', '/')
                target_file = os.path.join(target_path, src_rel_file)

                try:
                    # Replace placeholders in the target file name.
                    target_file = eval_file_name(target_file)
                except SkipFile:
                    continue

                # If target_file is dictionary generate file for each key-value pair.
                if isinstance(target_file, dict):
                    try:
                        os.makedirs(os.path.dirname(list(target_file)[0]))
                    except FileExistsError:
                        pass

                    for f_name in target_file:
                        context['obj'] = target_file[f_name]
                        generate_file(src_rel_file, src_file, f_name)
                else:
                    # Create necessary folders.
                    try:
                        os.makedirs(os.path.dirname(target_file))
                    except FileExistsError:
                        pass

                    generate_file(src_rel_file, src_file, target_file)

    logger.info('Done. Files created/overwritten/skipped = %s', file_count)
