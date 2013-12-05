import re
import sublime, sublime_plugin

class CssPrimerFromFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.settings().get('syntax') != 'Packages/HTML/HTML.tmLanguage':
      return
    source = self.view.file_name()
    self.view.window().show_input_panel(
      'Output CSS File',
      re.sub('.html', '', source) + '.css',
      lambda target: self.convert(source, target),
      None,
      None)

  def convert(self, source, target):
    if target:
      with open(source, 'r') as f:
        html = f.read()

      css = CSSPrimer.html2css(html)

      with open(target, 'w') as f:
        f.write(css)
      self.view.window().open_file(target)

  def is_enabled(self):
    return True


class CSSPrimer:
  @classmethod
  def html2css(self, html):
    id_attributes = set(re.findall(r'id=["|\']([^"|\']*)["|\']', html))
    class_attributes = set(re.findall(r'class=["|\']([^"|\']*)["|\']', html))

    stylesheet = ''
    if id_attributes:
      for id_attribute in id_attributes:
        id_string = "#" + id_attribute + " {\n\n}\n\n"
        stylesheet = stylesheet + id_string

    if class_attributes:
      for class_attribute in [classes for segments in class_attributes for classes in segments.split()]:
        class_string = "." + class_attribute + " {\n\n}\n\n"
        if class_string not in stylesheet:
          stylesheet = stylesheet + class_string

    return stylesheet
