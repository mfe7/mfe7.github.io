TODOs:

Software page:
- [ ] perfect grid

Publications page:
- [ ] add bibtex/citations for publications
- [ ] add default publication img

Main page:
- [ ] perfect grid of imgs
- [ ] perfect grid of youtube clips

## To run locally (not on GitHub Pages, to serve on your own computer)

1. Clone the repository and made updates as detailed above
1. Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
1. Run `bundle clean` to clean up the directory (no need to run `--force`)
1. Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
1. Run `bundle exec jekyll liveserve` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.

## To update publications

1. Make sure the google sheet is up-to-date.
1. Run `cd markdown_generator`
1. Run `python publications.py`. It will automatically download the sheet as a `.tsv` and generate/update the markdown files in `_publications/` for each publication.
