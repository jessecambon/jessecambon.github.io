## README

This is my personal blog. Notes for myself:

* Check for errors: `jekyll doctor`
* Build for deployment: `jekyll build`
* To preview blog with draft posts: `jekyll serve --drafts`


#### Resources
* Quick reference: https://jekyllrb.com/docs/usage/
* Minima Theme: https://github.com/jekyll/minima
* Jekyll-Feed plugin (for RSS) https://github.com/jekyll/jekyll-feed


#### Atom XMLL Feed

For R-Bloggers I needed to create a custom feed that only contained R content. My solution was to make all R posts contain the `tag` "r" and then use jekyll to build an r.xml file. The file in root, [r.xml](r.xml) is what builds the feed. I first tried to use [https://github.com/jekyll/jekyll-feed](jekyll-feed) to build a feed for a specific tag or category, but was unable to get it to work.

* Atom XML Feed Verifier: https://validator.w3.org/feed/
* Can use a RSS aggregator like [feedly](https://feedly.com/) for checking the content.
