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

#### Other Notes

* Installing jekyll: `gem install jekyll bundler`
* Installing the bundle: `bundle install`
* Updating the bundle: `bundle update`

* Ran into an issue with two versions of jekyll. Had to apt remove jekyll per https://github.com/jekyll/jekyll/issues/7088 (ie. only install the gem)
* Had to copy 'assets' and '_sass' folders from minima github (release file) into this repo to fix file not found errors

#### Blogging with Jupyter Notebooks

Steps for using jupyter notebooks to create a blog post:

- Add the desired YAML header to the beginning of the jupyter notebook in a raw cell. Include the beginning and trailing `---`. For example:

```
---
layout: post
title: "Test Jupyter Post"
date: 2021-10-17
author: Jesse Cambon
tags: [python, data]
image: "/images/tidygeocoder_hex_dark2021.png"
---
```

- Next convert the jupyter notebook to markdown using nbconvert with this terminal command: `jupyter nbconvert --to markdown <filename.ipynb>`. This creates a markdown (.md) file and a folder that will contain all images from the notebook. For example, if the command is executed from the project root directory and you working with a file in the `_drafts` folder you could do this:

```shell
jupyter nbconvert --to markdown _drafts/sklearn_skopt_pipeline.ipynb
```

- Move the folder `<filename_files>` to [jupyter_files](jupyter_files) (this is where the notebook images were saved by nbconvert).
- Open the Markdown (`.md`) file that was created by nbconvert (in the same directory as the jupyter notebook) and modify all image paths to refer to the correct folder (given where we moved the image folder to). The image references should begin with `![png]`. For example you would want to change this image path:

`![png](sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)`

To this:

`![png](/jupyter_files/sklearn_skopt_pipeline_files/sklearn_skopt_pipeline_15_1.png)`

In the future this process could be automated:

- https://www.linode.com/docs/guides/jupyter-notebook-on-jekyll/
- https://jaketae.github.io/blog/jupyter-automation/
- https://cduvallet.github.io/posts/2018/03/ipython-notebooks-jekyll 

#### Resources
* Quick reference: https://jekyllrb.com/docs/usage/
* Minima Theme: https://github.com/jekyll/minima
* Jekyll-Feed plugin (for RSS) https://github.com/jekyll/jekyll-feed
