from setuptools import setup

from pixelwall import VERSION

setup(
    name = "Pixelwall",
    version = VERSION,
    author = "Michael Fladischer",
    author_email = "michael@fladi.at",
    description = ("Kiosk-mode frontend browser for the Pixelwall server"),
    license = "BSD",
    keywords = "webkit gtk avahi",
    url = "http://www.openservices.at/pixelwall",
    packages=['pixelwall'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'gui_scripts': [
            'pixelwall = pixelwall:run_display',
        ]
    }
)
