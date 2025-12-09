import sys,os, subprocess


def find_exec(cmd: str, *_) -> tuple:
    ''' return (where_exist?, path_to_the_file) in the system path'''

    paths = os.environ.get('PATH', '').split(os.pathsep)

    for path in paths:
        if not path:
            continue

        cmd_path = os.path.join(path,cmd)

        if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
            return f"{cmd} is {cmd_path}", cmd_path
    return f"{cmd}: not found", None


def run_exec(user_input: list) -> int: #has side effects, prints the result
    '''runs an executable located in system path'''
    message, where_exist = find_exec(user_input[0])

    if where_exist is not None:


        output = subprocess.run(user_input, capture_output=True, text=True)
        print(output.stdout, end='')

        if output.stderr:
            print(output.stderr, end='', file=sys.stderr)
        return output.returncode

    print(message)


def cd_builtin(args=None):
    try:
        if args[0] == '~':
            os.chdir(os.getenv('HOME'))
            return
        os.chdir(args[0])
    except IndexError:
        os.chdir(os.getenv('HOME'))
    except:
        print(f"cd: {args[0]}: No such file or directory")





BUILTINS = {
        'exit': lambda *_: sys.exit(),
        'echo': lambda args: print(' '.join(args)),
        'pwd' : lambda *_: print(os.getcwd()),
        'cd'  : cd_builtin,
        'type': lambda cmd: print(f"{cmd[0]} is a shell builtin" if cmd[0] in BUILTINS
                                  else find_exec(cmd[0])[0]),
        }



def main():
    global BUILTINS




    while True:

        sys.stdout.write("$ ")

        prompted = input().strip().split()
        if not prompted:
            continue

        cmd = prompted[0]
        args = prompted[1:]


        if cmd in BUILTINS:
            BUILTINS[cmd](args)
            continue
        run_exec(prompted)




if __name__ == "__main__":
    main()
