import inspect
from arguments.arguments import args
from colors.colors import c, fg
import os


# call function
if __name__ == "__main__":
    try: 
        # get function
        func = args.func
    except AttributeError as ex:
        print(f"{fg.red}usage{c.reset}: {fg.lightgreen}python {os.path.basename(__file__)} -h{c.reset}")
        exit(0)
    except NameError as ne:
        print(f"{fg.red}usage{c.reset}: python {os.path.basename(__file__)} -h{c.reset}")
        exit(0)
    
    # get the signature of the function and parameters
    signature = inspect.signature(func)
    parameters = signature.parameters
    
    # dictionary for the arguments
    func_args = {}
    
    # get the arguments from parsed args and add them to the func_args dict
    for param_name, param in parameters.items():
        if param_name in args:
            func_args[param_name] = getattr(args, param_name)

    # call the function and pass the args dynamically
    func(**func_args)