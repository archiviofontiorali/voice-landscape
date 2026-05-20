class BlackList(set):
    def load_file(self, path):
        with open(path, "rt") as fp:
            for line in fp.readlines():
                if line.startswith("#"):
                    continue
                self.add(line.strip())
