## MyFormat is custom search command for Splunk

default value sign is True, if you want to have fields without sign you have to specify it explicitly

### Installation:
copy/update the following files

+ myformat.py --> bin/
+ commands.conf --> local/
+ default.meta --> metadata/


### Usage:
The command can work on many fields during the same call so we can execute that command at the end of the search
piping madness

| diffformat fields=[field1, field4, field2, field3] signs=[False, False]

  -- results in field1:False, field2:True, field3:True, field4:False