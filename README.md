# Semble or SembleLang

*Currently in Open Beta*

### Duck typing. Faster than C.

## DISCLAIMER

The langauge is not finished although it is about a month or so from it’s 1.0

### What is SembleLang?

SembleLang is a low-level simple language that compiles directly down to AT&T syntax x86 Assembly.

The claim “faster than C” is somewhat true as it mostly only competes with C speed as C is very well optimized and writing everything from scratch makes things hard.

It comes with its own big standard library but also with libc functions.

It has the following features (some may be buggy which will be fixed in the 1.0).
+ Variables
+ Functions
+ Structs
+ Arrays
+ Vectors (in the "vectors.smb" library like C++)
+ Strings (both strs and a String in the "strings.smb" library like C++)
+ Standard library
+ Custom operator meanings for Structs
+ Inline Assembly
+ If Statements
+ For and While Loops
+ I/O
+ Libc
+ File Interactions
+ Imports
+ Comments
+ Multiline Comments
+ All the basic types (ints, bools, hex values, chars, etc.)

I plan on adding the following features in time:

+ Networking
+ Multithreading
+ Namespaces
+ Classes
+ Cryptography
+ Package Manager

# Examples

## Recursive Fibbonaci(10)

![Code for it](https://imgur.com/PND6CC0)

## Person Data Structure

![Code for it](https://imgur.com/9bZgGyH)

## Vectors Example

![Code for it](https://imgur.com/0sAZDAC)

# Working with Semble

To start open your text editor of choice, if you decided to install the VSCode extension during the install, you may want to choose VSCode.

Then, create a file in the current directory witn the *.smb* extension.

This can be done with:
```
$ touch *.smb
```

Where `*` is the filename.

Then for a *Hello, World!* program write the following code.

```
#program main
#include io.smb

fn main() => {
  print("Hello, World!");
}
```

To compile, write this command in the directory in which your program is.

```
$ semble *.smb
```

Where `*` is the filename.

To run your code type the following command.

```
$ ./main
```

The reason the output is *main* is because that is what we specified with `#program main`, we could've put any valid filename there and if we dont put a `#program` header it defaults to the name *semble.out*.

# Information

The current deadline for 1.0 is a month and a half.

Comment down below that you want to be pinged on release if you want to be pinged.

The website is almost done and is being developed by @Coder100

Currently, Semble only works on Debian-based systems.

I spent ~3 months on this project.

It is currently in Open Beta with an installer available on the github, soon enough this installer will be available on the website.

The compiler is written in Python with a C++ interface (what I mean is a compiled C++ binary is put in /usr/lib/ and that calls the Python code in a directory like /home/wuru/.semble/)

Semble is currently under the MIT license.

# Special thanks

Although the language was developed by me only, there have been people who helped motivate and guide me.

+ @Coder100 - Web Developer and guiding me
+ @RickMiller - Guiding and encouraging me

And that is just a start, many people whom do not have repl.it helped me as well.

# Conclusion

Semble goes to show that simplicity and speed can both be achieved at the same time.

While it is not as easy as something like Python, it is more like easier than/as easy as C++.

To see a bigger Semble project I would suggest looking at the github and looking in the */libs/* folder as it also gives you a greater understanding of the language.

I will write another post when 1.0 comes out, and ping the people whom ask to be pinged in that post.

If you like the language and ideas behind it, consider upvoting the post as that will help more people see the language.

Have a great day! - @Wuru