My attempt at ["Build an AI Agent in Python"](https://www.boot.dev/courses/build-ai-agent-python) - A course from [Boot.dev](https://www.boot.dev).

## What Does the Agent Do?
The program is a CLI tool that:

+ Accepts a coding task
+ Chooses from a set of predefined functions to work on the task, for example:
  + Scan the files in a directory
  + Read a file's contents
  + Overwrite a file's contents
  + Execute the Python interpreter on a file
+ Repeats step 2 until the task is complete (or it fails miserably, which is possible)

**This agent doesn't have all the security and safety features that a production AI agent would have. This is for learning purposes only!**
