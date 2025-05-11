import os
import re
import sys

DEFAULT_TEMPLATE_PATH = os.path.join(os.path.expanduser('~'), '.local/share/cp-tool/template')
DEFAULT_EXTENSION = '.cpp'

def main(args):
    cur_directory = os.getcwd()

    # Check if args contains an extension
    extension = DEFAULT_EXTENSION
    extension_arg = find_arg(args, '-e=', '--extension=')
    if extension_arg is not None:
        extension = '.' + extension_arg.lstrip('.')

    # Check if args contains a template path
    template_path = DEFAULT_TEMPLATE_PATH
    template_path_arg = find_arg(args, '-t=', '--template-path=')
    if template_path_arg is not None:
        template_path = template_path_arg
    
    # Check if template file exists before doing anything
    full_template_path = template_path + extension
    ensure_exists(full_template_path)

    # Remove all the option arguments before proceeding
    args = [arg for arg in args if not arg.startswith('-')]

    # Command for creating contest files
    if 'contest' in args:
        contest_idx = args.index('contest')
        assert_num_args(args, contest_idx + 3, 'contest')
        if not args[contest_idx+1].isdigit():
            crash_with_help('Number of problems must be an integer:')
        num_problems = int(args[contest_idx+1])
        contest_name = ' '.join(args[contest_idx+2:])
        new_dir = create_contest(cur_directory, contest_name, num_problems, extension, template_path)
        print('Contest files created.')
        print_dir(new_dir)
    # Command for creating problem files
    elif 'problem' in args:
        problem_idx = args.index('problem')
        assert_num_args(args, problem_idx + 2, 'problem')
        problem_name = ' '.join(args[problem_idx+1:])
        new_dir = create_problem(cur_directory, problem_name, extension, template_path)
        print('Problem files created.')
        print_dir(new_dir)
    # Command for creating template
    elif 'template' in args:
        template_idx = args.index('template')
        assert_num_args(args, template_idx + 2, 'template')
        add_template(cur_directory, ' '.join(args[template_idx+1:]), extension, template_path, True)
        print('Template file created')
    # Help command
    elif 'help' in args:
        print_help()
    # Unknown command
    else:
        print('Invalid usage:')
        print_help()

def find_arg(args, prefix, alt_prefix=None):
    # Searches args for a string beginning with the prefix
    # and returns everything after the prefix in the string.
    for a in args:
        if a.startswith(prefix) or (alt_prefix is not None and a.startswith(alt_prefix)):
            return a[len(prefix):]
    return None

def create_contest(directory, name, num_problems, extension, template_path):
    # Create directory with problems: "problem1.cpp", "problem2.cpp", ...
    new_path = create_directory(directory, name, extension)
    for i in range(1, num_problems+1):
        problem_name = 'problem' + str(i)
        add_template(new_path, problem_name, extension, template_path)
    return new_path

def create_problem(directory, name, extension, template_path):
    new_path = create_directory(directory, name, extension)
    add_template(new_path, name, extension, template_path)
    return new_path

def add_template(directory, file_name, extension, template_path, override=False):
    # Read template file
    full_template_path = template_path + extension
    template_data = ""
    with open(full_template_path, 'r') as f:
        template_data = f.read()

    formatted_file_name = format_name(file_name, extension)
    new_path = os.path.join(directory, formatted_file_name) + extension

    # Write template file
    if not override:
        ensure_not_exists(new_path)
    with open(new_path, 'w') as f:
        f.write(template_data)

def print_help():
    print('Usage: cpt <commands> [args]')
    print('cpt help')
    print('cpt problem <name>')
    print('cpt contest <num_problems> <name>')
    print('cpt template <name>')
    print('--extension=<ext> or -e=<ext> to specify file extension')
    print('--template-path=<path> or -t=<path> to specify template path')

def create_directory(directory, directory_name, extension):
    formatted_directory_name = format_name(directory_name, extension)
    joined_path = os.path.join(directory, formatted_directory_name)
    ensure_not_exists(joined_path)
    os.mkdir(joined_path)
    return joined_path

def format_name(name, extension):
    # Replace spaces and remove special characters
    formatted = name.replace(' ', '_')
    formatted = re.sub(r'[^\w]', '', formatted)
    formatted = formatted.rstrip(extension)
    return formatted

def print_dir(dir):
    print('dir=' + dir)

def ensure_exists(path):
    if not os.path.exists(path):
        crash_with_error(f'Error: {path} does not exist')

def ensure_not_exists(path):
    if os.path.exists(path):
        crash_with_error(f'Error: {path} exists')

def assert_num_args(args, at_least, command):
    if len(args) < at_least:
        crash_with_help(f'Invalid number/order of arguments to command `{command}`:')

def crash_with_error(message):
    print(message)
    sys.exit(1) # Exit with error

def crash_with_help(message):
    print(message)
    print_help()
    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
