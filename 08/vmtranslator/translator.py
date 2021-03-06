'''
Translate .vm into .hack
'''

from constants import *
from parser import *
from code_writer import *
import argparse
import os.path
import glob

def main():
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('path', type=str, help='vm file or folder')

    args = argparser.parse_args()
    path = args.path

    if path.endswith('.vm'): # file
        with CodeWriter(path[:-3] + '.asm') as code_writer:
            translate_file(path, code_writer)
        print('translate to %s.asm' % path[:-3])

    else:                   # directory
        if path.endswith('/'):
            filename = path[:-1]
        else:
            filename = path
            path += '/'
        with CodeWriter(path + filename + '.asm') as code_writer:
            files = glob.glob('%s/*' % path)
            for file in files:
                if file.endswith('.vm'):
                    translate_file(file, code_writer)
        print('translate to %s%s.asm' % (path, filename))

def translate_file(file, code_writer):
    filename, _ = os.path.splitext(os.path.basename(file))
    code_writer.set_translating_file_name(filename)
    with Parser(file) as parser:
        parser.advance()
        while parser.curr_cmd != None:

            cmd_type = parser.command_type()
            
            if cmd_type == C_ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            elif cmd_type in [C_PUSH, C_POP]:
                code_writer.write_push_pop(cmd_type, parser.arg1(), parser.arg2())
            elif cmd_type == C_LABEL:
                code_writer.write_label(parser.arg1())

            elif cmd_type == C_GOTO:
                code_writer.write_goto(parser.arg1())

            elif cmd_type == C_IF:
                code_writer.write_if(parser.arg1())

            elif cmd_type == C_FUNCTION:
                code_writer.write_function(parser.arg1(), parser.arg2())

            elif cmd_type == C_RETURN:
                code_writer.write_return()

            elif cmd_type == C_CALL:
                code_writer.write_call(parser.arg1(), parser.arg2())

            parser.advance()

if __name__ == '__main__':
    main()
