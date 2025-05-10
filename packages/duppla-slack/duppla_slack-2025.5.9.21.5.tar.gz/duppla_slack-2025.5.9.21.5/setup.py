import setuptools as st

from datetime import datetime

# Setting up
st.setup(
    name="duppla_slack",
    version=f"{datetime.now():%Y.%m.%d.%H.%M}",
    author="duppla",
    author_email="<>",
    description="Custom implementation for Slack API",
    long_description_content_type="text/markdown",
    long_description="A custom implementation for Slack API using Python, based on the official API + SDK.",
    packages=st.find_packages(),
    package_data={"duppla_slack": ["py.typed"]},
    install_requires=[
        "pydantic>=2.7.0,<3.0.0",
        "requests",
        "shortuuid",
        "slack_sdk>3.30.0,<4.0.0",
        "Unidecode",
    ],
    keywords=["python", "slack", "duppla"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
