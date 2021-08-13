import configparser

def setopt(var, val):
    cfg = configparser.ConfigParser(allow_no_value=True, comment_prefixes="")
    cfg.optionxform = str
    cfg.read("../vars.conf")
    cfg.set("DEFAULT", var, val)
    with open("../vars.conf", 'w') as config:
        cfg.write(config)



def parse(var):
    cfg = configparser.ConfigParser()
    cfg.read('../vars.conf')
    return cfg['DEFAULT'][var]


def parse_path(path,header, var):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    return cfg[header][var]


# if __name__ == '__main__':
#     print(parse('GRAPH_MAX_VALUE'))
