import os
from pathspec import PathSpec


def get_patterns(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            patterns = f.readlines()
        patterns = [pattern.strip() for pattern in patterns if pattern.strip() and not pattern.startswith('#')]
    else:
        patterns = []
    return patterns

def get_all_filepaths(gitignore=True):
    if gitignore :
        patterns = get_patterns('./.gitignore')
    else :
        patterns = []

    spec = PathSpec.from_lines('gitwildmatch', patterns)
    all_filepaths = []
    for root, dirs, files in os.walk("./"):
        if '.git' in dirs:
            dirs.remove('.git')

        for name in files:
            filepath = os.path.relpath(os.path.join(root, name), start="./")
            all_filepaths.append(filepath)

    all_filepaths = [f for f in all_filepaths if not spec.match_file(f)]
    return sorted(all_filepaths)


def get_target_filepaths(patterns, ignore):
    all_filepaths = get_all_filepaths()
    patterns = [pattern.strip() for pattern in patterns if pattern.strip()]
    spec = PathSpec.from_lines('gitwildmatch', patterns)
    if ignore :
        return [f for f in all_filepaths if not spec.match_file(f)]
    else :
        return [f for f in all_filepaths if spec.match_file(f)]


def get_chat_filepaths(chatignore_path='./.aicastle/chat/.chatignore'):
    patterns = get_patterns(chatignore_path)
    return get_target_filepaths(patterns, True)


def get_finetuning_filepaths(finetuning_path='./.aicastle/chat/.finetuning'):
    patterns = get_patterns(finetuning_path)
    return get_target_filepaths(patterns, False)

