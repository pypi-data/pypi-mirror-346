import os.path


class SegmentProvider:
    def __init__(self, fpath : str, delimiter : str):
        if not os.path.isfile(fpath):
            raise FileNotFoundError(f'File {fpath} not found')
        with open(fpath, 'r') as f:
            file_content : str = f.read()
        segments = file_content.split(delimiter)

        self.segement_map : dict[str, str] = {}
        for s in segments:
            segment_name = s.split('\n')[0]
            content_lines = s.split('\n')[1:]
            segment_content = '\n'.join(content_lines)
            self.segement_map[segment_name] = segment_content

    def retrieve(self, name : str):
        """Retrieves a prompt from the specified prompt file by name"""
        return self.segement_map[name]

