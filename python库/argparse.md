一个命令行解析库

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-n','--name', default=' Li ')
    parser.add_argument('-y','--year', default='20')
    args = parser.parse_args()
    print(args)
    name = args.name
    year = args.year
    print('Hello {}  {}'.format(name,year))

if __name__ == '__main__':
    main()

```

线创建一个argparse的对象，可以进行描述

****

`add_argument()`添加想要输入的东西

- [name or flags](https://devdocs.io/python~3.9/library/argparse#name-or-flags) - Either a name or a list of option strings, e.g. `foo` or `-f, --foo`.
- [action](https://devdocs.io/python~3.9/library/argparse#action) - The basic type of action to be taken when this argument is encountered at the command line.
- [nargs](https://devdocs.io/python~3.9/library/argparse#nargs) - The number of command-line arguments that should be consumed.
- [const](https://devdocs.io/python~3.9/library/argparse#const) - A constant value required by some [action](https://devdocs.io/python~3.9/library/argparse#action) and [nargs](https://devdocs.io/python~3.9/library/argparse#nargs) selections.
- [default](https://devdocs.io/python~3.9/library/argparse#default) - The value produced if the argument is absent from the command line and if it is absent from the namespace object.
- [type](https://devdocs.io/python~3.9/library/argparse#type) - The type to which the command-line argument should be converted.
- [choices](https://devdocs.io/python~3.9/library/argparse#choices) - A container of the allowable values for the argument.
- [required](https://devdocs.io/python~3.9/library/argparse#required) - Whether or not the command-line option may be omitted (optionals only).
- [help](https://devdocs.io/python~3.9/library/argparse#help) - A brief description of what the argument does.
- [metavar](https://devdocs.io/python~3.9/library/argparse#metavar) - A name for the argument in usage messages.
- [dest](https://devdocs.io/python~3.9/library/argparse#dest) - The name of the attribute to be added to the object returned by [`parse_args()`](https://devdocs.io/python~3.9/library/argparse#argparse.ArgumentParser.parse_args).

****

`parse_args()`获得输入的参数，如果没有输入则获得全部

Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace.

Previous calls to [`add_argument()`](https://devdocs.io/python~3.9/library/argparse#argparse.ArgumentParser.add_argument) determine exactly what objects are created and how they are assigned. See the documentation for [`add_argument()`](https://devdocs.io/python~3.9/library/argparse#argparse.ArgumentParser.add_argument) for details.

- [args](https://devdocs.io/python~3.9/library/argparse#args) - List of strings to parse. The default is taken from [`sys.argv`](https://devdocs.io/python~3.9/library/sys#sys.argv).
- [namespace](https://devdocs.io/python~3.9/library/argparse#namespace) - An object to take the attributes. The default is a new empty [`Namespace`](https://devdocs.io/python~3.9/library/argparse#argparse.Namespace) object.

****

最后得到一个对象通过`.<name>`来获取对象