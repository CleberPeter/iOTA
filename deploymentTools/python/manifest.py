class _manifest:
    def __init__(self, _uuidProject, _version, _type, _dateExpiration, _filesNames, _filesSizes):
        self.uuidProject = _uuidProject
        self.version = _version
        self.type = _type
        self.dateExpiration = _dateExpiration

        self.files = []
        for index in range(0, len(_filesNames)):
            self.files.append({'name': _filesNames[index], 'size': _filesSizes[index]})