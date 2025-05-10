import yaml
import dataload.utils.logger as l
import dataload.model.dataStorageConnectionFactory as f

class Config:
    def __init__(self):
        self.logger = l.Logger()
        self.logger.debug(f"Chargement des fichiers de configuration ")
        self.logger.debug(f"Emplacement : conf/*.yaml ")
        self.raw_config = None

    def load_conf(self, config_file_path):
        with open(config_file_path, 'r') as file:
            self.raw_config = yaml.safe_load(file)
        return self

    def load_all_sources(self):
        sources={}
        for by_type in self.raw_config['TYPE'].items():
            if not by_type[1] is None:
                for source in by_type[1]:
                    self.logger.debug(f"Source definition building for {source['ALIAS']} .....")
                    sources[source['ALIAS']] = f.Connection.create(by_type[0], source)
        return sources

    def search_source(self, source_type, source_alias):
        for elt in self.raw_config['TYPE'].items():
            if elt[0] == source_type:
                for elt_2 in elt[1]:
                    if elt_2['ALIAS'] == source_alias:
                        return elt_2
                    else:
                        pass
            else:
                pass
        print("No source identify")


