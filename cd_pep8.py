''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on github.com)
    Alexey Torgashin (CudaText)
Version:
    '0.8.3 2019-05-06'
PyCodeStyle docs:
    http://pycodestyle.pycqa.org/en/stable/
ToDo: (see end of file)
'''

import  re, os, json, collections, configparser
import  cudatext            as app
from    cudatext        import ed
from    cudax_lib       import log
from    .cd_plug_lib    import *
OrdDict = collections.OrderedDict

FROM_API_VERSION= '1.0.146'

# I18N
_       = get_translation(__file__)

pass;                           # Logging
pass;                          #from pprint import pformat
pass;                          #pfrm15=lambda d:pformat(d,width=15)
pass;                           LOG = (-2==-2)  # Do or dont logging.
pass;                           ##!! waits correction

CONFIG_NAME = os.path.expanduser(r'~\.pycodestyle') \
              if os.name == 'nt' else \
              os.path.join(
                os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'),
                'pycodestyle'
              )
CIPHS   = {
    # Indentation
     'E101':'indentation contains mixed spaces and tabs'  # 'if a == 0:\n        a = 1\n\tb = 1'
    ,'E111':'indentation is not a multiple of four'  # '  a = 1'
    ,'E112':'expected an indented block'  # 'for item in items:\npass'
    ,'E113':'unexpected indentation'  # 'a = 1\n    b = 2'
    ,'E114':'indentation is not a multiple of four (comment)'  # '  # a = 1'
    ,'E115':'expected an indented block (comment)'  # 'for item in items:\n# Hi\n    pass'
    ,'E116':'unexpected indentation (comment)'  # 'a = 1\n    # b = 2'
    ,'E117':'over-indented'

    ,'E121':'continuation line under-indented for hanging indent'  # 'a = (\n   42)'
    ,'E122':'continuation line missing indentation or outdented'  # 'a = (\n42)'
    ,'E123':'closing bracket does not match indentation of opening bracket’s line'  # 'a = (\n    )'
    ,'E124':'closing bracket does not match visual indentation'  # 'a = (24,\n     42\n)'
    ,'E125':'continuation line with same indent as next logical line'  # 'if (\n    b):\n    pass'
    ,'E126':'continuation line over-indented for hanging indent'  # 'a = (\n        42)'
    ,'E127':'continuation line over-indented for visual indent'  # 'a = (24,\n      42)'
    ,'E128':'continuation line under-indented for visual indent'  # 'a = (24,\n    42)'
    ,'E129':'visually indented line with same indent as next logical line'  # 'if (a or\n    b):\n    pass'
    ,'E131':'continuation line unaligned for hanging indent'  # 'a = (\n    42\n 24)'
    ,'E133':'closing bracket is missing indentation'

    # Whitespace
    ,'E201':'whitespace after ‘(‘'  # 'spam( ham[1], {eggs: 2})'
    ,'E202':'whitespace before ‘)’'  # 'spam(ham[1 ], {eggs: 2})'
    ,'E203':'whitespace before ‘:’'  # 'if x == 4 : print x, y; x, y = y, x'
    ,'E211':'whitespace before ‘(‘'  # 'dict ['key'] = list[index]'
    ,'E221':'multiple spaces before operator'  # 'a = 4  + 5'
    ,'E222':'multiple spaces after operator'  # 'a = 4 +  5'
    ,'E223':'tab before operator'  # 'a = 4\t+ 5'
    ,'E224':'tab after operator'  # 'a = 4 +\t5'
    ,'E225':'missing whitespace around operator'  # 'i=i+1'
    ,'E226':'missing whitespace around arithmetic operator'  # 'c = (a+b) * (a-b)'
    ,'E227':'missing whitespace around bitwise or shift operator'  # 'c = a|b'
    ,'E228':'missing whitespace around modulo operator'  # 'msg = fmt%(errno, errmsg)'
    ,'E231':'missing whitespace after ‘,’, ‘;’, or ‘:’'  # '['a','b']'
    ,'E241':'multiple spaces after ‘,’'  # 'a = (1,  2)'
    ,'E242':'tab after ‘,’'  # 'a = (1,\t2)'
    ,'E251':'unexpected spaces around keyword / parameter equals'  # 'def complex(real, imag = 0.0):'
    ,'E261':'at least two spaces before inline comment'  # 'x = x + 1 # Increment x'
    ,'E262':'inline comment should start with ‘# ‘'  # 'x = x + 1  #  Increment x'
    ,'E265':'block comment should start with ‘# ‘'  # '#Block comment'
    ,'E266':'too many leading ‘#‘ for block comment'  # '### Block comment'
    ,'E271':'multiple spaces after keyword'  # 'True and  False'
    ,'E272':'multiple spaces before keyword'  # 'True  and False'
    ,'E273':'tab after keyword'  # 'True and\tFalse'
    ,'E274':'tab before keyword'  # 'True\tand False'
    ,'E275':'missing whitespace after keyword'

    # Blank line
    ,'E301':'expected 1 blank line, found 0'  # 'class Foo:\n    b = 0\n    def bar():\n        pass'
    ,'E302':'expected 2 blank lines, found 0'  # 'def a():\n    pass\n\ndef b(n):\n    pass'
    ,'E303':'too many blank lines (3)'  # 'def a():\n    pass\n\n\n\ndef b(n):\n    pass'
    ,'E304':'blank lines found after function decorator'  # '@decorator\n\ndef a():\n    pass'
    ,'E305':'expected 2 blank lines after end of function or class'
    ,'E306':'expected 1 blank line before a nested definition'

    # Import
    ,'E401':'multiple imports on one line'  # 'import sys, os'
    ,'E402':'module level import not at top of file'  # ''One string'\n"Two string"\nimport os'

    # Line length
    ,'E501':'line too long (82 > 79 characters)'
    ,'E502':'the backslash is redundant between brackets'  # 'aaa = ("bbb " \\n       "ccc")'

    # Statement
    ,'E701':'multiple statements on one line (colon)'  # 'else: do_non_blah_thing()'
    ,'E702':'multiple statements on one line (semicolon)'  # 'do_one(); do_two(); do_three()'
    ,'E703':'statement ends with a semicolon'  # 'do_four();  # useless semicolon'
    ,'E704':'multiple statements on one line (def)'  # 'def f(x): return 2*x'
    ,'E711':'comparison to None should be ‘if cond is None:'  # 'if None == arg:'
    ,'E712':'comparison to True should be ‘if cond is True:’ or ‘if cond:’'  # 'if False == arg:'
    ,'E713':'test for membership should be ‘not in’'  # 'Z = not X in Y'
    ,'E714':'test for object identity should be ‘is not’'  # 'Z = not X.B is Y'
    ,'E721':'do not compare types, use ‘isinstance()’'  # 'if type(obj) is type(1):'
    ,'E722':'do not use bare except, specify exception instead'
    ,'E731':'do not assign a lambda expression, use a def'  # 'f = lambda x: 2*x'
    ,'E741':'do not use variables named ‘l’, ‘O’, or ‘I’'
    ,'E742':'do not define classes named ‘l’, ‘O’, or ‘I’'
    ,'E743':'do not define functions named ‘l’, ‘O’, or ‘I’'

    # Runtime
    ,'E901':'SyntaxError or IndentationError'
    ,'E902':'IOError'

    # Indentation warning
    ,'W191':'indentation contains tabs'  # 'if True:\n\treturn'

    # Whitespace warning
    ,'W291':'trailing whitespace'  # 'spam(1) \n#'
    ,'W292':'no newline at end of file'
    ,'W293':'blank line contains whitespace'  # 'class Foo(object):\n    \n    bang = 12'

    # Blank line warning
    ,'W391':'blank line at end of file'  # 'spam(1)\n'

    # Line length
    ,'W503':'line break before binary operator'  # '(width == 0\n + height == 0)'
    ,'W504':'line break after binary operator'
    ,'W505':'doc line too long (82 > 79 characters)'

    # Deprecation warning
    ,'W601':'.has_key() is deprecated, use ‘in’'  # 'assert d.has_key('alph')'
    ,'W602':'deprecated form of raising exception'  # 'raise DummyError, "Message"'
    ,'W603':'‘<>’ is deprecated, use ‘!=’'  # 'if a <> 'no':'
    ,'W604':'backticks are deprecated, use ‘repr()’'  # 'val = `1 + 2`'
    ,'W605':'invalid escape sequence ‘x’'
    ,'W606':'‘async’ and ‘await’ are reserved keywords starting with Python 3.7'
}
DEF_IGNORE  = ['E121', 'E123', 'E126', 'E226', 'E241', 'E242', 'E704']
CIPHS   = OrdDict(sorted(CIPHS.items(), key=lambda t: t[0]))
GROUPS  = { 0:'Indentation'
          , 1:'Whitespace'
          , 2:'Blank line'
          , 3:'Import'
          , 4:'Line length'
          , 5:'Deprecation'
          , 6:'Statement'
          , 8:'Runtime'
            }
grciphs = {gr:[ciph+' '+nm for (ciph, nm) in CIPHS.items() if ciph[:2] in ['E'+str(1+gr), 'W'+str(1+gr)]] for gr in GROUPS}

class Command:
    
    def dlg(self):
        pepdata = get_data()
        igns    = pepdata.get('ignore', DEF_IGNORE)
        pass;                  #LOG and log('igns={}',(igns))
        maxl    = pepdata.get('max-line-length', 80)
#       maxl    = 80
        while True:
            aid,vals,chds   = dlg_wrapper(_('Configure PyCodeStyle'), 860+10,645+10,
                 [
                  dict(           tp='lb'       ,t=5            ,l=5        ,w=450      ,cap  =f(_('Ignore in "{}"'), GROUPS[0])    )
                 ,dict(cid='wht1',tp='ch-lbx'   ,t=25    ,h=270 ,l=5        ,w=450      ,items=grciphs[0]                           )
                 ,dict(           tp='lb'       ,t=30+275       ,l=5        ,w=450      ,cap  =f(_('Ignore in "{}"'), GROUPS[1])    )
                 ,dict(cid='wht2',tp='ch-lbx'   ,t=50+275,h=315 ,l=5        ,w=450      ,items=grciphs[1]                           )
                 ,dict(           tp='lb'       ,t=5            ,l=450+15   ,w=400      ,cap  =f(_('Ignore in "{}"'), GROUPS[2])    )
                 ,dict(cid='wht3',tp='ch-lbx'   ,t=25    ,h=105 ,l=450+15   ,w=400      ,items=grciphs[2]                           )
                 ,dict(           tp='lb'       ,t=135          ,l=450+15   ,w=200      ,cap  =f(_('Ignore in "{}"'), GROUPS[3])    )
                 ,dict(cid='wht4',tp='ch-lbx'   ,t=155   ,h= 50 ,l=450+15   ,w=400      ,items=grciphs[3]                           )
                 ,dict(           tp='lb'       ,tid='maxl'     ,l=450+15   ,w=400      ,cap  =f(_('Ignore in "{}"'), GROUPS[4])    )
                 ,dict(           tp='lb'       ,tid='maxl'     ,l=450+255  ,w=100      ,cap  =_('Max length:')                     )
                 ,dict(cid='maxl',tp='sp-ed'    ,t=210          ,l=450+350  ,w= 65      ,props='70,200,1'                           )
                 ,dict(cid='wht5',tp='ch-lbx'   ,t=235   ,h= 60 ,l=450+15   ,w=400      ,items=grciphs[4]                           )
                 ,dict(           tp='lb'       ,t=305          ,l=450+15   ,w=400      ,cap  =f(_('Ignore in "{}"'), GROUPS[5])    )
                 ,dict(cid='wht6',tp='ch-lbx'   ,t=325   ,h= 75 ,l=450+15   ,w=400      ,items=grciphs[5]                           )
                 ,dict(           tp='lb'       ,t=410          ,l=450+15   ,w=400      ,cap  =f(_('Ignore in "{}"'), GROUPS[6])    )
                 ,dict(cid='wht7',tp='ch-lbx'   ,t=430   ,h= 90 ,l=450+15   ,w=400      ,items=grciphs[6]                           )
                 ,dict(           tp='lb'       ,t=530          ,l=450+15   ,w=400      ,cap  =f(_('Ignore in "{}"'), GROUPS[8])    )
                 ,dict(cid='wht7',tp='ch-lbx'   ,t=550   ,h= 60 ,l=450+15   ,w=400      ,items=grciphs[8]                           )
                 ,dict(cid='defs',tp='bt'       ,t=5+645-28     ,l=5+860-250,w=80       ,cap=_('Defaults')                                )
                 ,dict(cid='!'   ,tp='bt'       ,t=5+645-28     ,l=5+860-165,w=80       ,cap=_('OK')        ,props='1'              ) # default
                 ,dict(cid='-'   ,tp='bt'       ,t=5+645-28     ,l=5+860-80 ,w=80       ,cap=_('Cancel')                            )
                 ]
                 ,     dict(wht1=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[0]])
                           ,wht2=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[1]])
                           ,wht3=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[2]])
                           ,wht4=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[3]])
                           ,wht5=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[4]])
                           ,wht6=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[5]])
                           ,wht7=(-1,[('1' if nm[:4] in igns else '0') for nm in grciphs[6]])
                           ,maxl=maxl
                           ), focus_cid='wht1')
            if aid is None or aid=='-': return None
            if aid=='defs':
                igns    = DEF_IGNORE
                maxl    = 80
                continue#while
            if aid=='!':
                maxl    = vals['maxl']
                igns    = []
                igns   += [grciphs[0][n][:4] for (n, ch) in enumerate(vals['wht1'][1]) if ch=='1']
                igns   += [grciphs[1][n][:4] for (n, ch) in enumerate(vals['wht2'][1]) if ch=='1']
                igns   += [grciphs[2][n][:4] for (n, ch) in enumerate(vals['wht3'][1]) if ch=='1']
                igns   += [grciphs[3][n][:4] for (n, ch) in enumerate(vals['wht4'][1]) if ch=='1']
                igns   += [grciphs[4][n][:4] for (n, ch) in enumerate(vals['wht5'][1]) if ch=='1']
                igns   += [grciphs[5][n][:4] for (n, ch) in enumerate(vals['wht6'][1]) if ch=='1']
                igns   += [grciphs[6][n][:4] for (n, ch) in enumerate(vals['wht7'][1]) if ch=='1']
                save_data({'ignore':igns
                               ,'max-line-length':maxl})
                break#while
           #while
       #def dlg
   #class Command

def get_data():
    if not os.path.isfile(CONFIG_NAME):
        return {}
    config  = configparser.ConfigParser()
    config.read(CONFIG_NAME)
    pass;                      #LOG and log('config["pycodestyle"]["ignore"]={}',(config['pycodestyle']['ignore']))
    rsp     = {}
    if config['pycodestyle']['max-line-length']:
        rsp['max-line-length']  = int(config['pycodestyle']['max-line-length'])
    raw_ignore  = config['pycodestyle']['ignore']
    if raw_ignore:
        raw_ignore  = raw_ignore.replace(' ', '')
        rsp['ignore']           = raw_ignore
    pass;                      #LOG and log('rsp={}',(rsp))
    return rsp

def save_data(fvdata):
    pass;                      #LOG and log('fvdata={}',(fvdata))
    svd     = {'max-line-length': fvdata['max-line-length']
              ,'ignore':', '.join(fvdata['ignore'])}
    pass;                      #LOG and log('svd={}',(svd))
    config  = configparser.ConfigParser()
    config['pycodestyle']  = svd
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)


'''
ToDo
[+][kv-kv][06jul16] Init
'''
