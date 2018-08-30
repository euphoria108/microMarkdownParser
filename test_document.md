# Test Document

テスト用のドキュメントです。

## Block elements
This is *emphasized*.

<p> this is *not emphasized*. </p>

## Automatic escaping for special characters
&copy;
AT&T
4 < 5

## Inline elements
In inline elements, <span>*emphasizing* is enabled.</span>

## Paragraphs and Line Breaks
This is a first paragraph.
Rest of first paragraph.

Second Paragraph

## Headers
This is an H1.
=============
This is an H2.
-------------

# h1
## h2
### h3
#### h4
##### h5
### sharp after the title is ignored ###

## Block quote
> this is a blockquote.
>
> foo
> bar

> this is a single
blockquote paragraph.

> This is the first level of quoting.
>
>> Nested level of quoting.
>
> Back to the first level of quoting.

> ## This is a header.
>
> 1. This is the first list item.
> 2. This is the second list item.
>
> Here's some example code:
>
>     return shell_exec("echo $input | $markdown_script");

## Lists
* item
- item
+ item

* 1st level
    * 2nd level
        * 3rd level
    * 2nd level
        * 3rd level
 * 1 space
  * 2 space
   * 3 space
    * 4 space
    

## ordered list
1. item
1. item
1000. item

* Indented Paragraph
  Ignore spaces before indent.

1.  This is a list item with two paragraphs. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit. Aliquam hendrerit
    mi posuere lectus.

    Vestibulum enim wisi, viverra nec, fringilla in, laoreet
    vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
    sit amet velit.

2.  Suspendisse id sem consectetuer libero luctus adipiscing.

*   A list item with a blockquote:

    > This is a blockquote
    > inside a list item.

*   A list item with a code block:

        <code goes here>

## Escaping listing
1986\. What a great season.

## Automatically convert escape codes in code block.
    <div> &

### Horizontal rules
***
* * *
---
- - -
___
_ _ _

## Links
This is [an example](http://example.com/ "Title") inline link.

This is [an example][id] reference-style link.

This is [an example] [id] reference-style link.

[id]: http://example.com/  "Optional Title Here"

[id]: <http://example.com/>  "Optional Title Here"

[Google][]

[Google]: http://google.com/

I get 10 times more traffic from [Google][1] than from
[Yahoo][2] or [MSN][3].

[1]: http://google.com/        "Google"
[2]: http://search.yahoo.com/  "Yahoo Search"
[3]: http://search.msn.com/    "MSN Search"

## Emphasis
*single asterisks* -> <em>single asterisks</em>

_single underscores_ -> <em>single underscores</em>

**double asterisks** -> <strong>double asterisks</strong>

__double underscores__ -> <strong>double underscores</strong>

un*fucking*believable -> un<em>fucking</em>believable

You're f\*\*king crazy.

## Inline code block
Use the `printf()` function.

``files = `ls`.split``

`` `ps` ``

``` ``double-back-quote`` ```

Please don't use any `<blink>` tags.

## Images
![代替文字列](URL)

![代替文字列](URL "タイトル")

![Alt text][id]

[id]: url/to/image  "Optional title attribute"

# Automatic Link
<http://example.com/>

<address@example.com>

converted into:

    <a href="&#x6D;&#x61;i&#x6C;&#x74;&#x6F;:&#x61;&#x64;&#x64;&#x72;&#x65;
    &#115;&#115;&#64;&#101;&#120;&#x61;&#109;&#x70;&#x6C;e&#x2E;&#99;&#111;
    &#109;">&#x61;&#x64;&#x64;&#x72;&#x65;&#115;&#115;&#64;&#101;&#120;&#x61;
    &#109;&#x70;&#x6C;e&#x2E;&#99;&#111;&#109;</a>

# Backslash Escapes
\\ \` \* \_ \{ \} \[ \] \( \) \# \+ \- \. \!

# Tables

|  TH  |  TH  |
| ---- | ---- |
|  TD  |  TD  |
|  TD  |  TD  |

  TH  |  TH  
 ---- | ---- 
  TD  |  TD  
  TD  |  TD  

alignment

 left | center | right
:---- |:------:| -----:
  L   |   C    |   R

