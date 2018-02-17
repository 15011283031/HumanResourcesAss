import configparser  # 用于读取写入配置文件，并使之生效的类
import os

config = configparser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.

# config your section value
config.add_section('path2')  # config your section
config.set('path2', 'root', r'D:\WORK\HumanResourcesAss')  # config.set(section_name,section_option,section_value)
config.set('path2', 'web', r'D:\WORK\HumanResourcesAss\AssForGaia_Web')
config.set('path2', 'web_assforhr', r'D:\WORK\HumanResourcesAss\AssForGaia_Web\AssForHR')

# get your cfg path
current_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
cfg_path = current_path + r'/resources/conf/web.cfg'

# Writing our configuration file to cfg_path you defined
with open(cfg_path, 'w') as configfile:
    config.write(configfile)

