from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.in'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='groupdocs-redaction-net',
      version='25.5',
      python_requires='>=3.9,<3.13',
      description='GroupDocs.Redaction for Python via .NET provides a reliable solution for redacting sensitive and confidential information across a wide range of document formats.',
      url='https://products.groupdocs.com/redaction',
      author='GroupDocs',
      license='Other/Proprietary License',
      classifiers=['Operating System :: Microsoft :: Windows','Operating System :: Unix','License :: Other/Proprietary License','Programming Language :: Python :: 3','Programming Language :: Python :: 3 :: Only','Programming Language :: Python :: 3.9','Topic :: Text Processing','Topic :: Security','Topic :: Software Development :: Libraries','Topic :: Utilities'],
      keywords=['redactor,redact,file,document','pdf,docx,xlsx,pptx,html,png,word,excel,powerpoint'],
      platforms=['win_amd64,win32,macos_x86_64,macos_arm64'],
      long_description=long_description,
      long_description_content_type='text/markdown')
