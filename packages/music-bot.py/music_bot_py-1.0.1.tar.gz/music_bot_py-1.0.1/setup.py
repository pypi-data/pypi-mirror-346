from setuptools import setup, find_packages

setup(
    name='music-bot.py',  # PyPI에 등록될 이름
    version='1.0.1',
    description='A Discord music bot using discord.py and yt-dlp',
    author='앙 기모찌',
    author_email='igm12345677a@gmail.com',
    packages=find_packages(),
    install_requires=[
        'discord.py==2.5.2',
        'yt-dlp==2025.4.30',
        'aiohttp==3.11.18',
        'PyNacl==1.5.0',
    ],
    entry_points={
        'console_scripts': [
            'yourbot=ic:main'  # ic.py 파일에 main() 함수가 있을 경우
        ]
    },
    python_requires='>=3.8',
)
