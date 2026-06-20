import yaml

class ParamsLoader:
    @staticmethod
    def load_params(file_path: str) -> dict:
        import yaml
        with open(file_path, 'r') as file:
            params = yaml.safe_load(file)
        return params