# PyAV-Video

[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]

PyAV-Video converts videos to image frames and vice versa!



## Installation

Install PyAV-Video and its dependencies

```bash
pip install av-video
```



## Quickstart

Convert a video to image frames

```bash
from av_video import Video

with Video.open("example.mp4") as v:
    v.to_images()
```



## License

PyAV-Video has a MIT license, as found in the [LICENSE](https://github.com/imyizhang/PyAV-Video/blob/main/LICENSE) file.



## Contributing

Thanks for your interest in contributing to PyAV-Video! Please feel free to create a pull request.



## Changelog

**PyAV-Video 0.0.1**

* First release



[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/imyizhang/PyAV-Video



[pypi_badge]: https://badgen.net/pypi/v/av-video?icon=pypi&color=black&label
[pypi_link]: https://www.pypi.org/project/av-video