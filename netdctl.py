from app.args import Arguments
from app.invoker import Invoker


def main():    
    arguments = Arguments()
    
    invoke = Invoker(arguments.get_args)
    invoke.register(arguments.get_args.func)
    invoke.execute(arguments.get_args.func)


if __name__ == '__main__':
    main()
