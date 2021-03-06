## README

This is my personal blog.

#### Operational Notes
* Check for errors: `jekyll doctor`
* Build for deployment: `jekyll build`
* To preview blog with draft posts (posts stored in `_drafts` folder): `jekyll serve --drafts`

#### Code Notes
* `/feed.xml` is generated by the jekyll-feed plugin while `/r.xml` is a feed exclusively for the `r` tag that is generated by the [r.xml](r.xml) script. Both `feed.xml` and `r.xml` are generated when `jekyll build` is run.
* When `jekyll build` is run, scripts such as `r.xml` are run and the resulting data and content is put into the `_site` folder which generates the site.
* Configure `_config.yml` as necessary to configure site-wide variables and settings. Use `exclude:` to exclude files (such as `README.md`) from the jekyll build process. Use `header_pages:` to add additional pages to the site.

#### Atom XML Feed

For R-Bloggers I needed to create a custom feed that only contained R content. My solution was to make all R posts contain the `tag` "r" and then use jekyll to build an r.xml file. The file in root, [r.xml](r.xml) is what builds the feed. I first tried to use [https://github.com/jekyll/jekyll-feed](jekyll-feed) to build a feed for a specific tag or category, but was unable to get it to work.

* Atom XML Feed Verifier: https://validator.w3.org/feed/
* Can use a RSS aggregator like [feedly](https://feedly.com/) for checking the content.

#### Other Modifications

- Post tag pages added per [these instructions](https://longqian.me/2017/02/09/github-jekyll-tag/)
- Leaflet Javascript library added based on [this](https://github.com/dieghernan/dieghernan.github.io/blob/master/_includes/leaflet.html).

##### Other Notes

* Installing jekyll: `gem install jekyll bundler`
* Installing the bundle: `bundle install`
* Updating the bundle: `bundle update`

* Ran into an issue with two versions of jekyll. Had to apt remove jekyll per https://github.com/jekyll/jekyll/issues/7088
* Had to copy 'assets' and '_sass' folders from minima github (release file) into this repo to fix file not found errors

#### Resources
* Quick reference: https://jekyllrb.com/docs/usage/
* Minima Theme: https://github.com/jekyll/minima
* Jekyll-Feed plugin (for RSS) https://github.com/jekyll/jekyll-feed
