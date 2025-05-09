# Web Content Scraper - README

## Overview

The Web Content Scraper is a comprehensive Python tool for extracting and processing various types of web content including text, images, audio, video, and tabular data. The package is organized into three main classes with distinct functionalities:

- `html`: Web content extraction and parsing
- `run`: Direct content downloading
- `show`: Content display and playback

## Features

### 1. `html` Class

#### Text Extraction

```python
html.txt(mode, url, content_class, next_page_class, content_tag='div', next_page_tag='div', base_url='https:/', link_index=None)
```

- `mode`: Extraction mode ('br' or 'p')
- `url`: Starting URL
- `content_class`: Class of content container
- `next_page_class`: Class of next page link container
- `content_tag`: HTML tag of content (default 'div')
- `next_page_tag`: HTML tag containing next page link (default 'div')
- `base_url`: Base URL for relative links (default 'https:/')
- `link_index`: Index of <a> tag if multiple exist (default None)

#### Image Downloading

```python
html.img(url, container_class=None, url_prefix=None)
```

- `url`: Target webpage URL
- `container_class`: Class of image container (optional)
- `url_prefix`: URL prefix for relative image paths (optional)

#### Audio Downloading

```python
html.audio(url, container_class=None)
```

- `url`: Target webpage URL
- `container_class`: Class of audio container (optional)

#### Table Extraction

```python
html.table(url, sort_order=None, sort_column='')
```

- `url`: Webpage URL containing table
- `sort_order`: None/True/False for no sort/ascending/descending
- `sort_column`: Column name to sort by

### 2. `run` Class

#### Direct Downloads

```python
run.music(url, output_name='1')
run.video(url, output_name='1', url_prefix=None)
run.txt(url, output_name='1')
run.table(url, sort_order=None, sort_column='')
```

- `url`: Direct media URL
- `output_name`: Output filename (without extension)
- `url_prefix`: URL prefix for video fragments (optional)

### 3. `show` Class

#### Content Display

```python
show.txt(mode, filename, start=1, end=1)
show.image(filename)
show.music(filename)
show.video(filename)
```

- `mode`: Display mode ('连续' for sequence or '单个' for single file)
- `filename`: Base filename (without extension)
- `start`: First file in sequence
- `end`: Last file in sequence

## Excel Handling Functions

```python
handle_excel(mode='merge')
```

- `mode`: Operation mode ('merge', 'statistics', or 'duplicate')

## Dependencies

- Core:
  
  - `requests>=2.25.0`
  - `beautifulsoup4>=4.9.0`
  - `lxml>=4.6.0`
  - `Pillow>=8.0.0`

- Media:
  
  - `audioplayer>=0.7`
  - `moviepy>=1.0.0`

- Data:
  
  - `pandas>=1.2.0`
  - `openpyxl>=3.0.0`

## Usage Examples

### Text Extraction

```python
# Extract text from multiple pages
html.txt('br', 'https://example.com/page1', 'article-content', 'pagination', 'div', 'nav', 'https://example.com', 0)
```

### Image Download

```python
# Download all images from a gallery
html.img('https://example.com/gallery', 'gallery-container', 'https://cdn.example.com')
```

### Play Downloaded Content

```python
# Play the first downloaded audio file
show.music('1')
```

## Notes

1. Always check website terms of service before scraping
2. Consider adding delays between requests to avoid overloading servers
3. The User-Agent header mimics Chrome browser to reduce blocking
4. Error handling is basic - consider adding more specific exception handling

For more detailed examples, see the `examples/` directory in the package.
