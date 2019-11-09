---
layout: post
title:  "Welcome to Jekyll!"
date:   2019-11-08 22:47:40 -0500
categories: jekyll update
---
You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

To add new posts, simply add a file in the `_posts` directory that follows the convention `YYYY-MM-DD-name-of-post.ext` and includes the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}



{% highlight r %}
library(dplyr)
library(tidygeocoder)

# Make a tibble of addresses in DC
dc_addresses <- tribble( ~name,~addr,
       "White House", "1600 Pennsylvania Ave Washington, DC",
       "National Academy of Sciences", "2101 Constitution Ave NW, Washington, DC 20418",
       "Department of Justice", "950 Pennsylvania Ave NW, Washington, DC 20530",
       "Supreme Court", "1 1st St NE, Washington, DC 20543",
       "Washington Monument", "2 15th St NW, Washington, DC 20024"
                           )

# Geocode the addresses with the US Census geocoder
coordinates <- dc_addresses %>%
  geocode(addr)
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
