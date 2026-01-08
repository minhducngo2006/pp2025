import subprocess
import sys
import os
def parse_command(line):
    tokens = line.strip().split()
    if not tokens:
        return [], {}, []

    # Parse redirections
    redirects = {'<': None, '>': None}
    args = []
    i = 0
    while i < len(tokens):
        if tokens[i] in ('<', '>'):
            if i + 1 >= len(tokens):
                raise ValueError(f"Missing file after {tokens[i]}")
            redirects[tokens[i]] = tokens[i + 1]
            i += 2
        else:
            args.append(tokens[i])
            i += 1

    # Split by pipes
    if '|' not in args:
        return [args], redirects, []

    pipe_cmds = []
    current_cmd = []
    for token in args:
        if token == '|':
            if current_cmd:
                pipe_cmds.append(current_cmd)
            current_cmd = []
        else:
            current_cmd.append(token)
    if current_cmd:
        pipe_cmds.append(current_cmd)

    return pipe_cmds, redirects, []


def execute_pipeline(pipe_cmds, input_redirect=None, output_redirect=None):
    """Execute a pipeline of commands"""
    if not pipe_cmds:
        return

    # Prepare input
    input_file = None
    if input_redirect:
        input_file = open(input_redirect, 'r')
        stdin = input_file
    else:
        stdin = sys.stdin

    prev_process = None
    stdin_for_next = None

    for i, cmd in enumerate(pipe_cmds):
        is_last = (i == len(pipe_cmds) - 1)

        # Set up stdout
        if is_last and output_redirect:
            stdout = open(output_redirect, 'w')
        elif is_last:
            stdout = sys.stdout
        else:
            stdin_for_next, stdout_for_next = os.pipe()
            stdout = stdout_for_next

        # Create process
        try:
            if prev_process:
                process = subprocess.Popen(
                    cmd,
                    stdin=prev_process.stdout,
                    stdout=stdout,
                    stderr=subprocess.PIPE,
                    text=True
                )
                prev_process.stdout.close()
            else:
                process = subprocess.Popen(
                    cmd,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=subprocess.PIPE,
                    text=True
                )

            # Clean up file descriptors
            if not is_last:
                os.close(stdout_for_next)

            prev_process = process

        except FileNotFoundError:
            print(f"Command not found: {cmd[0]}", file=sys.stderr)
            if input_file:
                input_file.close()
            return
        except Exception as e:
            print(f"Error executing {cmd[0]}: {e}", file=sys.stderr)
            if input_file:
                input_file.close()
            return

    # Wait for last process and get output
    _, stderr = prev_process.communicate()

    # Print stderr if any
    if stderr:
        print(stderr, file=sys.stderr)

    # Close input file if used
    if input_file:
        input_file.close()


def execute_simple(cmd, input_redirect=None, output_redirect=None):
    """Execute a simple command with optional redirections"""
    try:
        stdin = None
        if input_redirect:
            stdin = open(input_redirect, 'r')

        stdout = None
        if output_redirect:
            stdout = open(output_redirect, 'w')

        result = subprocess.run(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.stderr:
            print(result.stderr, file=sys.stderr)

    except FileNotFoundError:
        print(f"Command not found: {cmd[0]}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        if stdin:
            stdin.close()
        if stdout:
            stdout.close()


def execute_command(line):
    """Execute a command line with pipes and redirections"""
    try:
        pipe_cmds, redirects, _ = parse_command(line)

        if not pipe_cmds:
            return

        input_redirect = redirects.get('<')
        output_redirect = redirects.get('>')

        if len(pipe_cmds) > 1:
            execute_pipeline(pipe_cmds, input_redirect, output_redirect)
        else:
            execute_simple(pipe_cmds[0], input_redirect, output_redirect)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


def main():
    print("Simple Shell - Type 'exit' to quit")
    print("Supported: pipes (|), input redirect (<), output redirect (>)")
    print("-" * 50)

    while True:
        try:
            # Show current directory in prompt
            cwd = os.getcwd()
            home = os.path.expanduser("~")
            if cwd.startswith(home):
                display_cwd = "~" + cwd[len(home):]
            else:
                display_cwd = cwd

            prompt = f"\n[{display_cwd}]$ "
            command = input(prompt)

            if command.strip() == "":
                continue

            if command.strip() in ('exit', 'quit', 'q'):
                print("Goodbye!")
                break

            execute_command(command)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
