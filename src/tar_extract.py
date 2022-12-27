import os
import tarfile


def unpack_tar(arc_path):

    mode = "r:"
    if arc_path.endswith("tar.gz"):
        mode = "r:gz"

    f = open(arc_path, 'rb')
    tar = tarfile.open(fileobj=f, mode=mode)
    # for item in tar:
    return tar


def extract_arcive_files(arc_path, filter_extensions):
    tar = unpack_tar(arc_path)

    extracted_data = {}
    for item in tar:
        fname = os.path.basename(item.name)

        if filter_extensions:
            if not os.path.splitext(fname)[1] in filter_extensions:
                continue

        extracted_data[fname] = tar.extractfile(item.path).read()
        print(item)
    return extracted_data
