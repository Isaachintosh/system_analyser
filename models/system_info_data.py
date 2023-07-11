

def get_general_info_system_data(self, data):
    data.update({
        'system_name': self.name,
        'system_executable_name': self.path.sys.executable,
        'system_copyright': self.path.sys.copyright,
        'system_platform': self.path.sys.platform,
        'system_version': self.path.sys.version
    }) # Adiciona uma linha em branco entre as iterações do loop