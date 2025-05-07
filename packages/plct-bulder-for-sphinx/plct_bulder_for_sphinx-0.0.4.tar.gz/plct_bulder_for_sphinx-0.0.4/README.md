# Petlja Builder for Sphinx

This custom Sphinx builder, named `PLCTBuilder`, extends the functionality of the `StandaloneHTMLBuilder` to meet specific requirements for packaging content into various formats, such as bare HTML, Moodle backup, or SCORM.

## Key Features

## Content URI and Player

The `content_uri` is used by a small web app called a "player" that allows you to navigate through the course. The builder attempts to remove the sidebar, footer, and nav bar by disabling them using Sphinx theme variables. This streamlined content is then packaged up and served on other platforms inside SCORM packages. The player is aware of the architecture of your Sphinx project and just needs the web address specified in `content_uri` to function correctly.

This allows your students to follow the course on any platform that implements SCORM standard.

### Bare HTML Content

The builder provides the ability to generate HTML content suitable for integrating into an e-learning platform.

### Moodle Backup

The builder supports packaging content in a format suitable for Moodle (provides you with a moodle backup file).

### SCORM

The builder not only facilitates the creation of SCORM-compliant packages, but it also generates two types of packages. One is a holistic package that includes all lectures. The other type is a segmented package, where all the lectures are split up. This allows you to pick and choose which lectures to import, offering flexibility in content selection. When we refer to a "lecture", we are referring to a section that is one level below Sphinx's toc top level.

## Hosting Requirements

For the builder to function correctly and display your content on a CMS or eLMS, you need to host your content online. The builder requires a reachable URL to access and display the content generated.

## Usage

```python 
# conf.py

# Import the Petlja Builder extension
extensions = ['plct-bulder-for-sphinx.builder.plct_builder']

```

To generate content, use the following command:

```bash
sphinx-build -b plct_builder source output
```
## Configuration

Customize the behavior of the builder by updating the Sphinx configuration:

```python
# conf.py

# Set the content URI
content_uri = 'your_content_uri'

# Specify additional build targets (e.g., 'moodle', 'scorm')
additional_build_targets = ['moodle', 'scorm']
```

## License

This custom Sphinx builder is licensed under the [MIT License](LICENSE). Feel free to adapt and extend it based on your specific requirements.