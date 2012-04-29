from functools import partial

__author__ = 'jakub.zygmunt'
import re
import sys

try:
    import splunk.Intersplunk
    in_splunk = True
except (NameError, ImportError):
    in_splunk = False

class MyFormat(object):

    def formatDigit(self, digit):
        reversed = digit[::-1]
        reversed_spaces = re.sub("(.{3})", "\\1 ", reversed)
        normal_spaces = reversed_spaces[::-1].strip()
        return normal_spaces

    def format(self, value, sign=False, suffix=''):
        match = re.search("^(-?)([0-9 ]+)(.*)", value)
        ret = value
        if match:
            s = match.group(1)
            ret = self.formatDigit(match.group(2))

            if (sign):
                valueWithSign = int(s + match.group(2))
                signChar = '+' if valueWithSign>0  else '-' if valueWithSign < 0 else ''
                ret = signChar + ret
            value_suffix = match.group(3) if match.group(3) and suffix == '' else suffix
            if not value_suffix == '' :
                ret = ret + ' ' + value_suffix
        return ret

    def format_string(self, str, sign=False, suffix=''):
        def change(matchobj, options):
            return self.format(matchobj.group(1), sign = options['sign'], suffix = options['suffix'])
        options = { 'sign':sign, 'suffix':suffix }
        string_formatted = re.sub("([\-0-9]+)", partial(change, options=options) , str)
        return string_formatted

def log(msg):
    with open( "/opt/splunk/var/log/splunk/myformat.log", "a" ) as f:
        f.write( msg + "\n")

def mapFieldsWithOptions(fields_string, signs_string):
    fields = fields_string.split(',')
    signs = signs_string.split(',')
    # map signs
    signsChar = [''] * len(fields)
    for index, value in enumerate(signs):
        signsChar[index] = value

    #map field to sign
    mappings = []
    for index, value in enumerate(fields):
        sign = False if signsChar[index].lower() in ['false', '0', 'no', 'n'] else True
        mappings.append({'field':value, 'sign':sign})
        # get sign
    return mappings


#log("myformat.py, in_splunk=%s" % in_splunk)

if  in_splunk:
    #log("inside if")
    # try:
    (isgetinfo, sys.argv) = splunk.Intersplunk.isGetInfo(sys.argv)
    args, kwargs = splunk.Intersplunk.getKeywordsAndOptions()

    if isgetinfo:
        # streaming, generating, retevs, reqsop, preop
        splunk.Intersplunk.outputInfo(True, False, False, False, None)


    (results, dummyresults, settings) = splunk.Intersplunk.getOrganizedResults()

    fields_string = kwargs.get("fields", "value")
    signs_string = kwargs.get("signs", "")
    field_suffix = kwargs.get("suffix", "suffix")
    # log("fields_string = %s, signs_string = %s" % ( fields_string, signs_string))
    mappings = mapFieldsWithOptions(fields_string, signs_string)
    # log("mappings %s" % mappings)

    try:
        formatter = MyFormat()
        for result in results:
            for mapping in mappings:
                field_name = mapping['field']
                withSign = mapping['sign']
                try:
                    value = result[field_name]
                except KeyError:
                    # If either field is missing, simply ignore
                    continue
                value_formatted = formatter.format_string(value, sign=withSign, suffix=result[field_suffix])
                # log("value=%s, value_formatted=%s" % (value, value_formatted))
                result[field_name] = value_formatted

        splunk.Intersplunk.outputResults(results)
    except Exception, e:
        log("Unhandled exception:  %s" % e)
        splunk.Intersplunk.generateErrorResults("Unhandled exception:  %s" % (e,))



