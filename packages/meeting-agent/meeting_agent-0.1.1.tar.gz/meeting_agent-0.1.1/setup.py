from setuptools import setup, find_packages

setup(
    name="meeting-agent",
    version="0.1.1",
    description="A FastMCP-based smart agent for managing enterprise meeting room reservations.",
    author="rhythmli",
    author_email="rhythmli.scu@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "mcp"
    ],
    entry_points={
        "console_scripts": [
            "meeting-agent-list=meeting_agent.agent:get_meeting_room_list",
            "meeting-agent-reserve=meeting_agent.agent:create_meeting_reservation",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)