[<img height="23" src="https://github.com/lh9171338/Outline/blob/master/icon.jpg"/>](https://github.com/lh9171338/Outline) lh-webtool
===

This is a web tool package.

# Updates

 - [x] 2024.11.06: Add `hf_download` module
 - [x] 2024.03.24: Add `Crawler` and `play_image_web` modules

# Tools

* crawler
    * Crawler
* play_image_web
* hf_download

# Install

* Installing from source
```shell
git clone https://github.com/lh9171338/lh-webtool.git

cd lh-webtool

python -m build

pip install dist/lh_webtool-1.3.3-py3-none-any.whl
```

* Install from the Python Package Index (PyPI)
```shell
# install base
pip install lh_webtool

# install with specific dependencies, support: [huggingface]
pip install lh_webtool[huggingface]

# install with all dependencies
pip install lh_webtool[all]
```
