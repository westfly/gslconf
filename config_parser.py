import sys
class ConfigParser():
    """docstring for ConfigParser"""
    def __init__(self, filename):
        self.filename= filename
        self.key_stack = []
        self.all_dict = {}
        self.level = 0
        self.parse()
    def parse(self):
        """docstring for parse"""
        fp = open(self.filename, "r")
        for line in fp.readlines():
            if len(line) <= 1:
                continue
            if line.startswith('#'):
                continue
            self.parse_one_line(line)
        fp.close()
    def parse_one_line(self, line):
        """docstring for parse_one_line"""
        if line.startswith('['):
            self.handler_section(line)
        else:
            self.handler_keyvalue(line)
    def get_curr_dict_or_list(self, level):
        """docstring for get_curr_dict_or_list"""
        cur = 0
        curr_dict = self.all_dict
        #print "curr_statck %s"%self.key_stack
        while cur < level:
            key = self.key_stack[cur]
            if isinstance(curr_dict, list):
                curr_dict = curr_dict[-1]
            value = curr_dict[key]
            curr_dict = value
            cur += 1
        if isinstance(curr_dict, list):
            return curr_dict[-1]
        return curr_dict


    def handler_keyvalue(self, line):
        """docstring for hander_keyvalue"""
        pos = line.find('=');
        raw_key = line[0 : pos].strip()
        key = self.get_real_key(raw_key)
        value = line[pos + 1 : -1].strip()
        #print "key=%s\tvalue=%s"%(raw_key, value)
        curr_dict_or_list = self.get_curr_dict_or_list(self.level)
        if self.get_level_type(raw_key) == 'Array' :
            if not key in curr_dict_or_list:
                curr_dict_or_list[key] = []
            curr_dict_or_list[key].append(value)
        else:
            curr_dict_or_list[key] = value
    def get_level_count(self, key):
        """docstring for get_level_count"""
        return key.count(".")
    def get_level_type(self, key):
        """docstring for get_level_type"""
        if key.count("@") > 0:
            return 'Array'
        else:
            return 'Type'
    def get_real_key(self, key):
        """docstring for get_real_key"""
        skip = key.count('@')
        skip += key.count('.')
        return key[skip:]

    def handler_section(self, line):
        """docstring for handler_section"""
        key = line[1 : -2]
        level = self.get_level_count(key)
        self.curr_type = self.get_level_type(key)
        key = self.get_real_key(key)
        while level < self.level:
            self.key_stack.pop()
            self.level -= 1
        curr_dict_or_list = self.get_curr_dict_or_list(self.level)
        self.level += 1
        #print "key=%s\tlevel=%d\ttype=%s"%(key, level, self.curr_type)
        #print "cur %s"%curr_dict_or_list
        self.key_stack.append(key)
        if (self.curr_type == 'Array'):
            if not key in curr_dict_or_list:
                curr_dict_or_list[key] = []
            curr_dict_or_list[key].append({})
            print "fix %s\t%s"%(key, self.all_dict)
        else:
            curr_dict_or_list[key] = {}
            print "add %s\t%s"%(key, self.all_dict)
    def __getitem__(self, key):
        return self.all_dict[key]
    def printf(self):
        """docstring for print"""
        print "this %s"%self.all_dict
import sys
if __name__ == '__main__':
    config = ConfigParser(sys.argv[1])
    #config.printf()
    print config["log"]["path"]
    print config["message"]["update_ips"][1]
    print config["ClientConfig_UTS"]["Client"]["Service"][0]["Server"][0]["IP"]
