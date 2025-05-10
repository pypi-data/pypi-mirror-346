import os
import natsort

def iter_dir(directory: str, ext: str=None, nat=True, exclude: set=None):
    """Obtain files/folders in the <root>/<rel_path>/<folder>
    
    ext: types of files to return
        - None: yield all file types
        - '/': yield directories only
        - '.png': yield only png.
    
    """
    exclude = set(exclude) if exclude is not None else set()

    files = os.listdir(directory)
    if nat:
        files = natsort.natsorted(files)

    for file in files:

        if file in exclude:  continue

        abs_path = os.path.join(directory, file)
        is_dir = os.path.isdir(abs_path)

        if ext=='/':  # Dirs only
            if not is_dir:  continue

        elif ext is not None:
            if ext=='*':  # Files only
                if is_dir:  continue
            
            else:  # .ext files only
                path_ext = os.path.splitext(abs_path)[1]
                if ext.lstrip('.')!=path_ext.lstrip('.'):  continue

        elif ext is None:  # All dirs all files
            ...

        yield file


def list_dir(directory: str, ext: str=None, nat=True, exclude: set=None, **kwargs):
    return list(iter_dir(directory, ext, nat, exclude, **kwargs))