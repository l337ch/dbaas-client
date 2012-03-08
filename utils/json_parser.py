__author__ = 'lchang'


class JsonParser():

    def parse_json(self, json_obj):
        keys = json_obj.keys()
        values = []

        for k in keys:
            if isinstance(json_obj[k], dict):
                print
            else:
                values.append(json_obj[k])

        result = [keys] + [values]
        return result


    def parse_json_obj(self, json_object):
        """Recursively search json_obj three levels deep. This is also
       testing for list types. PLEASE REFACTOR"""
        keys = []
        values = []

        for key1 in json_object:
            v = []
            k = []
            #test for value of key1 is a dict
            if isinstance(json_object[key1], dict):
                json_1 = json_object[key1]
                print "json_1: " + str(json_1)
                for key2 in json_1:
                    #test for value of key2 is a dict
                    if isinstance(json_1[key2], dict):
                        for key3 in json_1[key2]:
                            if key3 != 'links':
                                k.insert(len(k), key3)
                                v.insert(len(v), json_1[key2][key3])
                                print key3 + ":" + str(json_1[key2][key3])
                    else:
                        if key2 != 'links':
                            k.insert(len(k), key2)
                            v.insert(len(v), json_1[key2])
                            print key2 + ":" + str(json_1[key2])
                values.append(v)

            #test to see if this is a list
            elif isinstance(json_object[key1], list):
                #iterate through the list
                for index in json_object[key1]:
                    v = []
                    for key2 in index:
                    #test for value of key2 is a dict
                        if isinstance(index[key2], dict):
                            for key3 in index[key2]:
                                if key3 != 'links':
                                    k.insert(len(k), key3)
                        elif key2 != 'links':
                            k.insert(len(k), key2)
                            v.insert(len(v), index[key2])

                    values.append(v)

            else:
                k.insert(len(keys), key1)
                v.insert(len(v), json_object[key1])

        keys = [ x for i,x in enumerate(k) if x not in k[i+1:]]
        result_list = [keys] + values
        return result_list

