from setuptools import setup, find_packages

setup(
    name='KishouScrapeDraw',  # パッケージ名（PyPI上での名前）
    version='0.1.0',  # バージョン番号（SemVer推奨：例 0.1.0, 1.0.0 など）
    author='S.Kishida',  # あなたの名前
    author_email='s.kishida98@gmail.com',  # メールアドレス（任意）
    description='気象庁(JMA)の天気データを取得・可視化・PDF化する教育向けツール',
    long_description=open('README.md', encoding='utf-8').read(),  # READMEを長文説明に使用
    long_description_content_type='text/markdown',  # Markdownを使用していることを明記
    url='https://github.com/s-kishida/KishouScrapeDraw.git',  # GitHubリポジトリURL
    license='MIT',
    packages=find_packages(),  # __init__.py を含むすべてのパッケージを自動検出
    install_requires=[
        'matplotlib',
        'japanize_matplotlib',
        'pandas',
        'numpy',
        'fpdf',
        'requests',
        'pdf2image',
        'opencv-python-headless',
        'PyPDF2',
        'qrcode[pil]'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Natural Language :: Japanese'
    ],
    python_requires='>=3.8',
    include_package_data=True,  # MANIFEST.in を使う場合に有効（現時点ではなくてもOK）
)
