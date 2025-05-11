# neuon
 neuon utils 

Neuon utils contains easy access feature
## 1.0 Debug print
Debug print are meant to take over print feature in Python and turn them into debug printing with following behaviour
 -  When NEUON_DEBUG is set to '1' in environment variable, the print feature activate and print debug info
 -  When NEUON_DEBUG is set to '' in environment variable, the print feature will not print (silent)
 -  When NEUON_DEBUG is set to '' in environment variable, the print with argument force_print will still print the output
 
The environment variable can be set by:
```python
import neuon

neuon.neuon_utils.enable_debug_print()
neuon.neuon_utils.disable_debug_print()
```

Alternatively, the status can be set by default in environment variable as 
```sh
set "NEUON_DEBUG=1"
```

The debug printing usage example:
```python
import neuon

neuon.neuon_utils.print_debug('Test print')
```
The output, date time will be shown follow by the printed content, then the filename (if exists, non-console), lastly the module called the printing
```text
[220627161856] Test print [<module>]
```
For print replacement usage example:
```python
from neuon.neuon_utils import print_debug as print

print('Test print')
```

# New in 0.0.2 
Generally is backward support and nothing needs to be changed. The additional feature will work on background to generate log files at 'logs' folder. Can otherwise be disabled by calling disable_log().

```python
from neuon.neuon_utils import print_debug as print
from neuon.neuon_utils import set_log_suffix
from neuon.neuon_utils import enable_debug_print
from neuon.neuon_utils import disable_log,enable_log

import neuon.neuon_utils as neuon

# call by alias name
neuon.set_log_suffix("neuon-main-6") # decide log suffix instead of generated uid, not entirely encourage since every instance called print_debug need to be set manually.

# call by import module
enable_debug_print() # enable print of console
enable_log() # enable log writing (default is enabled)

print('External call')
```


