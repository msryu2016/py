# command.py
!/usr/bin/python
# coding=utf-8 ~


import sys
import os

from optparse import OptionParser

# name, help, action 항목에 대해 값을 설정해준다. action에 count 속성 값을 주면 해당 옵션이 사용된 갯수를 반환한다.
option_0 = { 'name' : ('-m', '--mobile'), 'help' : 'mobile command', 'action' : 'count'}
option_1 = { 'name' : ('-w', '--web'), 'help' : 'web command', 'action' : 'count' }
option_2 = { 'name' : ('-n', '--network'), 'help' : 'network command', 'action' : 'count' }
option_3 = { 'name' : ('-f', '--forensic'), 'help' : 'forensic command' , 'action' : 'count' }
option_4 = { 'name' : ('-a', '--analysis'), 'help' : 'Malware analaysis command', 'action' : 'count' }
option_5 = { 'name' : ('-u', '--util'), 'help' : 'util command', 'action' : 'count' }


options = [option_0, option_1, option_2, option_3, option_4, option_5]



def main(options, arguments):

# 해당하는 옵션에 반환된 값이 0이 아니면 해당하는 명령어 리스트를 출력한다.
    if options.mobile != None:
        os.system('cat "%appie_ROOT%\config\mobile_command.txt"')

    elif options.web != None:
        os.system('cat "%appie_ROOT%\config\web_command.txt"')

    elif options.network != None:
        os.system('cat "%appie_ROOT%\config\\network_command.txt"')

    elif options.forensic != None:
        os.system('cat "%appie_ROOT%\config\\forensic_command.txt"')

    elif options.analysis != None:
        os.system('cat "%appie_ROOT%\config\malware_analysis_command.txt"')

    elif options.util != None:
        os.system('cat "%appie_ROOT%\config\util_command.txt')

# 옵션이 부여되지 않은 경우 help 옵션 부여
    else :
        os.system('python %appie_ROOT%/command.py -h')


if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name'] # name 항목에 대한 값들을 param 변수에 저장
        del option['name'] # 불필요한 리스트 항목 삭제
        parser.add_option(*param, **option) # 옵션 추가

    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)
