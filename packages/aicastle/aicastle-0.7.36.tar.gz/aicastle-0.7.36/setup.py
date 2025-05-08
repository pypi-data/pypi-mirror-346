from setuptools import setup, find_packages
from get_version import read_version

setup(
    name='aicastle',
    version=read_version(),
    packages=find_packages(include=['aicastle', 'aicastle.*']),
    include_package_data=True,
    package_data={
        'aicastle': ['package_data/*'],
    },
    
    # 의존성 필수
    install_requires=[
        'tqdm', 
        "click",
        'pillow',
        'python-dotenv',
        "pyyaml",
    ],

    # 의존성 선택
    extras_require={
        'chat': [
            "streamlit",
            'openai',
            'tiktoken',
            'pathspec',
            'pymupdf',  # fiz
        ],
        'deepracer-vehicle': [
            'tensorflow',
            'opencv-python',
            'requests-toolbelt',
            'beautifulsoup4',
            'lxml',
            'pynput',
            'paramiko',
            # 'ipykernel',
            # 'openai',
            # 'ollama',
        ],
        'deepracer-drfc': [
            "boto3",
            "paramiko",
            'pandas',
            # 'ipykernel',
        ],
    },

    entry_points={
        "console_scripts": [
            "aicastle=aicastle.cli:main",  # aicastle 명령어 실행 엔트리포인트
        ],
    },

    author='aicastle',
    author_email='dev@aicastle.io',
    description='AI Castle Package',
    url='https://github.com/ai-castle/aicastle',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    zip_safe=False,
)
