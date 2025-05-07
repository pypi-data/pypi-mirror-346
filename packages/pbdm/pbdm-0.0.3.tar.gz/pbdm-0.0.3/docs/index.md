# Heading

Text about the package

**_NOTE:_**
***Thanks George for setting this up!***

## Subheading, emphasis and links

More text, *italic text*, **bold text**, ***bold and italic text***.  

Link to a page: [Text to Display](tutorials.md)

## Lists

### A numbered list

1. First thing
2. Second thing
3. Third thing

### A list

- Something
- Something else
- Something else

## Quotes and code

### Quotes

Single quote: 

> A quote

Multiline quote:

> A multiline
> quote
> 
> with space

### Code

The package `pbdm` is for...

The function `DayDegrees` is for...

Code block:

``` py title="example_function.py"
def add(n,m):
    return n+m
```

A code block with line numbers:

``` py title="example_function_2.py" linenums="1"
def difference(n,m):
    if n>m:
        return n-m
    else:
        return m-n
```

A code block with highlighted lines:

``` py title="example_function_3.py: the highlighted lines ensure we don't get an error" hl_lines="2-3" linenums="1"
def exp(base=a, power=b):
    if a==0 and b==0:
        print("Error: the exponential 0^0 is not defined")
    else:
        return a**b
```

## Special features

All of the plugins available are [here](https://squidfunk.github.io/mkdocs-material/reference/). These are the ones we've currently installed.

### Admonition

!!! note

    This is an admonition. It is of type 'note'. All content inside must be indented.

This text is not indented and appears outside. 

!!! info "Custom Heading"

    This is an admonition with a heading. It is of type 'info'.

Different types and more information of admonitions is [here](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

### Maths

This is a sentence with the equation $y=\frac{3}{2} x$ inline.

This is a sentence with the equation
$$
y = \frac{3}{2} x
$$
in a display environment.

### Annotations

Annotations (1) are very powerful features which allow you to insert descriptions almost anywhere in a document. Just click on the symbol to see the description. 
{ .annotate }

1. This is where I enter the description (1) 
    { .annotate }

    1. This is an annotation inside another one!

More information [here](https://squidfunk.github.io/mkdocs-material/reference/annotations/).

### Abbreviations

PBDM is a mechanistic modelling paradigm which provides an alternative to CSDM in invasive species assessment. Hover over the abbreviations for the full definition.

*[PBDM]: Physiologically based demographic model
*[CSDM]: Correlative species distribution model